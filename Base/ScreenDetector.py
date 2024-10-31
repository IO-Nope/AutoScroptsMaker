import cv2
import numpy as np
from Base.GUIPoint import GUIPoint
from PIL import Image
from Base.KeyMouseMu import KeyMouseMu
import xml.etree.ElementTree as ET
import os
class ScreenDetector:
    __aimImg=[]
    __regionLT:GUIPoint
    __regionRB:GUIPoint
    __isDebug=False
    __relatefactor = 0.8
    def __init__(self,*aImgs:Image.Image,regionLT:GUIPoint,regionRB:GUIPoint,relatefactor:float=-1):
        self.__regionLT = regionLT
        self.__regionRB = regionRB
        if relatefactor > 0:
            self.__relatefactor = relatefactor
        for img in aImgs:
            if isinstance(img,Image.Image):
                self.__aimImg.append(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
            else:
                raise TypeError("The input image should be PIL.Image.Image type")
        return
    @classmethod
    def default(cls)->"ScreenDetector":
        return cls(regionLT=GUIPoint.default(),regionRB=GUIPoint.default())
    def Match_template(self,screenshot:np.ndarray)->bool:
        max_res = 0
        for template in self.__aimImg:
            result = cv2.matchTemplate(screenshot,template,cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > max_res:
                max_res = max_val  
        if self.__isDebug:
            print(f"match : max_val is {max_res}")
        return max_res >= self.__relatefactor
    def Set_Debug(self,isDebug:bool):
        self.__isDebug = isDebug
        return
    def Set_relatefactor(self,relatefactor:float):
        self.__relatefactor = relatefactor
        return
    def Check(self)->bool:
        KMMins =KeyMouseMu.Get_instance()
        tempLT = self.__regionLT.Get_point()
        tempRB = self.__regionRB.Get_point()
        region = (tempLT.x,tempLT.y,tempRB.x-tempLT.x,tempRB.y-tempLT.y)
        sceenshot = KMMins.Screenshot(region=region)
        cvscreenshot = cv2.cvtColor(np.array(sceenshot), cv2.COLOR_RGB2BGR)
        return self.Match_template(cvscreenshot)
    def to_xml_element(self,name:str,path:str)->ET.Element:
        elem = ET.Element("ScreenDetector")
        elem.set("relatefactor", str(self.__relatefactor))
        LTelem = ET.Element("RegionLT")
        LTelem.append(self.__regionLT.to_xml_element())
        elem.append(LTelem)
        RBelem = ET.Element("RegionRB")
        RBelem.append(self.__regionRB.to_xml_element())
        elem.append(RBelem)
        #swith to PIL.Image.Image path! because this is not a good way to save image data
        ImgsElem = ET.Element("Images")
        for i,cvimg in self.__aimImg:
            img = Image.fromarray(cvimg)
            path = os.path.join(path,f"{name}_{i}.png")
            img.save(path)
            pathElem = ET.Element("Path")
            pathElem.text = path
            ImgsElem.append(pathElem)
        elem.append(ImgsElem)
        return elem
    @classmethod
    def from_xml_element(cls,elem:ET.Element)->"ScreenDetector":
        rfstr = elem.get("relatefactor")
        rf= float(rfstr) if rfstr is not None else 0.8
        LTelem = elem.find("RegionLT")
        LT = GUIPoint.default()
        if LTelem is not None:
            LT = GUIPoint.from_xml_element(LTelem)
        RBelem = elem.find("RegionRB")
        RB = GUIPoint.default()
        if RBelem is not None:
            RB = GUIPoint.from_xml_element(RBelem)
        paths = elem.findall("Images/Path")
        cvimgs = []
        for path in paths:
            if path.text is None:
                continue
            img = Image.open(path.text)
            cvimgs.append(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
        return cls(*cvimgs,regionLT=LT,regionRB=RB,relatefactor=rf)
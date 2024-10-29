import cv2
import numpy as np
import GUIPoint
from PIL import Image
import KeyMouseMu
class ScreenDetector:
    __aimImg=[]
    __regionLT:GUIPoint.GUIPoint
    __regionRB:GUIPoint.GUIPoint
    __isDebug=False
    __relatefactor = 0.8
    def __init__(self,*aImgs:Image.Image,regionLT:GUIPoint.GUIPoint,regionRB:GUIPoint.GUIPoint):
        self.__regionLT = regionLT
        self.__regionRB = regionRB
        for img in aImgs:
            if isinstance(img,Image.Image):
                self.__aimImg.append(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
            else:
                raise TypeError("The input image should be PIL.Image.Image type")
        return
    def match_template(self,screenshot:np.ndarray)->bool:
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
    def Check(self,img:Image.Image)->bool:
        KMMins =KeyMouseMu.KeyMouseMu.get_instance()
        tempLT = self.__regionLT.get_point()
        tempRB = self.__regionRB.get_point()
        region = (tempLT.x,tempLT.y,tempRB.x-tempLT.x,tempRB.y-tempLT.y)
        sceenshot = KMMins.screenshot(region=region)
        cvscreenshot = cv2.cvtColor(np.array(sceenshot), cv2.COLOR_RGB2BGR)
        return self.match_template(cvscreenshot)
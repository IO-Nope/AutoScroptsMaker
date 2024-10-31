from Base.Vector2 import Vector2
from Base.ScreenDetector import ScreenDetector
from Base.GUIPoint import GUIPoint
from PIL import Image
from tkinter import messagebox
from typing import Optional
import xml.etree.ElementTree as ET
import os
class ScreenDectorManager:
    __instance:Optional['ScreenDectorManager'] = None
    __path:str
    __detectors:dict[str,ScreenDetector]
    def load(self):
        #check if path exist or not
        if not os.path.isdir(self.__path):
            print("path not exist")
            return
        xml_path = os.path.join(self.__path,"ScreenDetectors.xml")
        if not os.path.isfile(xml_path):
            print("xml file not exist")
            return
        if os.path.getsize(xml_path) == 0:
            return
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for elem in root:
            name_maybe = elem.get("name")
            name = name_maybe if name_maybe is not None else "default"
            detelem = elem.find("Detector")
            detector = ScreenDetector.default()
            if detelem is not None:
                detector = ScreenDetector.from_xml_element(detelem)
            #some bad may happen here
            self.__detectors[name] = detector
        return
    def save(self):
        if not os.path.isdir(self.__path):
            print("path not exist")
            return
        if not hasattr(self, '_ScreenDetectorManager__detectors'):
            return
        #create xml file
        
        root = ET.Element("ScreenDectorManager")
        for name , detector in self.__detectors.items():
            elem = ET.Element("Detector")
            elem.set("name",name)
            detelem = ET.Element("Detector")
            detelem.append(detector.to_xml_element(name,self.__path))
            elem.append(detelem)
            root.append(elem)
        tree = ET.ElementTree(root)
        xml_path = os.path.join(self.__path,"ScreenDectorManager.xml")
        tree.write(xml_path)
        return
    @classmethod
    def Get_instance(cls)->'ScreenDectorManager':
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    def Init(self,path:str):
        #check is path a floder or not
        self.__path = path
        return
    def __init__(self):
        return
    def __del__(self):

        self.save()
        return
    def Add_Detector(self,name:str,*aimg:Image.Image,RegionLT:GUIPoint,RegionRB:GUIPoint)->bool:
        if not self.__detectors.get(name , 0):
            messagebox.showwarning("warning", f"detector: {name} already exist")
            return False
        self.__detectors[name]=ScreenDetector(*aimg, regionLT=RegionLT, regionRB=RegionRB)
        return True
    def Remove_Detector(self,name)->bool:
        if self.__detectors.get(name , 0):
            messagebox.showwarning("warning", f"detector: {name} not exist")
            return False
        del self.__detectors[name]
        return True
    def Detector_check(self,name)->bool:
        if not self.__detectors.get(name , 0):
            print("warning", f"detector: {name} not exist")
            return False
        return self.__detectors[name].Check()
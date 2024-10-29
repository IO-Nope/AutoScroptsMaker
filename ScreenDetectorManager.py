from .Base import Vector2
from .Base import ScreenDetector
from .Base import GUIPoint
from PIL import Image
from tkinter import messagebox
class ScreenDectorManager:
    __instance = None
    __path:str
    __detectors = {}
    def load(self):
        return
    def save(self):
        return
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self,path):
        self.__path = path
        self.load()
        return
    def __del__(self):
        self.save()
        return
    def Add_Detector(self,name,*aimg:Image.Image,RegionLT:GUIPoint.GUIPoint,RegionRB:GUIPoint.GUIPoint):
        if not self.__detectors.get(name , 0):
            messagebox.showwarning("warning", f"detector: {name} already exist")
            return 0
        self.__detectors[name]=ScreenDetector(*aimg, regionLT=RegionLT, regionRB=RegionRB)
        return 1
    def Remove_Detector(self,name):
        if self.__detectors.get(name , 0):
            messagebox.showwarning("warning", f"detector: {name} not exist")
            return 0
        del self.__detectors[name]
        return 1
    def Detector_check(self,name):
        if not self.__detectors.get(name , 0):
            print("warning", f"detector: {name} not exist")
            return 0
        return self.__detectors[name].check()
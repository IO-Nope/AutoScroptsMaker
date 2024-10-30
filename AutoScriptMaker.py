import ButtonManager
import ScreenDetectorManager
from .Base import GUIPoint
from .Base import Vector2
from .Base import KeyMouseMu
from typing import Optional
BMins = ButtonManager.ButtonManager.Get_instance()
SDMins = ScreenDetectorManager.ScreenDectorManager.Get_instance()
KMMins = KeyMouseMu.KeyMouseMu.Get_instance()
import os
import pygetwindow as gw
class AutoScriptMaker:
    __instance: Optional['AutoScriptMaker'] = None
    __guiname : str
    __scriptpath : str
    __detectorpath : str
    __buttonpath : str
    @classmethod
    def Get_instance(cls)->'AutoScriptMaker':
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
    
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    def __init__(self):
        return
    def __del__(self):
        self.SaveProject()
        return
    def Init(self,guiname:str)->bool:
        self.__guiname = guiname
        guis = gw.getWindowsWithTitle(self.__guiname)
        if not guis:
            print("Can't find the GUI")
            return False
        gui = guis[0]
        #Init GUIPoint!
        guiLT = Vector2(gui.left,gui.top)
        guisize = Vector2(gui.width,gui.height)
        InitGUIPoint = GUIPoint.GUIPoint(guiLT,guiLT,guisize) #init GUIPoint
        return True
    def Init_Managers(self):
        BMins.Init(self.__buttonpath)
        SDMins.Init(self.__detectorpath)
        return    
    def CreateProject(self,scriptpath:str,scriptname:str)->bool:
        if not os.path.isdir(scriptpath):
            print("The script path doesn't exist or is not a directory")
            return False
        self.__scriptpath = os.path.join(scriptpath,scriptname)
        if os.path.exists(self.__scriptpath):
            print("The project already exists")
            return False
        self.__detectorpath = os.path.join(scriptpath,scriptname,"Detectors")
        self.__buttonpath = os.path.join(scriptpath,scriptname,"Buttons.xml")
        #establish the project folder
        os.makedirs(self.__scriptpath,exist_ok=True)
        os.makedirs(self.__detectorpath,exist_ok=True)
        fp = open(self.__buttonpath,"w")
        fp.close()
        self.Init_Managers()
        return True
    def LoadProject(self,scriptpath:str)->bool:
        if not os.path.isdir(scriptpath):
            print("The script path doesn't exist or is not a directory")
            return False
        self.__scriptpath = scriptpath
        self.__detectorpath = os.path.join(scriptpath,"Detectors")
        self.__buttonpath = os.path.join(scriptpath,"Buttons.xml")
        if not (os.path.exists(self.__buttonpath) & os.path.exists(self.__detectorpath)):
            print("have no button or detectors")
            return False
        self.Init_Managers()
        BMins.load()
        SDMins.load()
        return True

    def SaveProject(self)->bool:
        BMins.save()
        SDMins.save()
        return True
    def DelProject(self)->bool:
        return True
    def Get_GUIPoint(self,PointType:GUIPoint.PointType)->GUIPoint.GUIPoint:
        #TODO:通过双击屏幕计算GUIPoint
        (x,y) = KMMins.Get_mouse_when_double_click()
        point = Vector2(x,y)
        resGP = GUIPoint.GUIPoint(point)
        return resGP
    def Add_Button(self,name,PointType:GUIPoint.PointType)->bool:
        #TODO:choose GUIPointType
        return True
    def Add_ScreenDetector(self,name)->bool:
        #TODO:选择GUIPoint
        
        #TODO
        
        return True
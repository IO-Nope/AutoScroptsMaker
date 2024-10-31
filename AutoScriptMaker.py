import ButtonManager
import ScreenDetectorManager
from Base.GUIPoint import GUIPoint
from Base.Vector2 import Vector2
from Base.KeyMouseMu import KeyMouseMu
from Base.GUIPoint import PointType
from typing import Optional
BMins = ButtonManager.ButtonManager.Get_instance()
SDMins = ScreenDetectorManager.ScreenDectorManager.Get_instance()
KMMins = KeyMouseMu.Get_instance()
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
        if hasattr(self, '_AutoScriptMaker__scriptpath'):            
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
        InitGUIPoint = GUIPoint(guiLT,guiLT,guisize) #init GUIPoint
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
        scdexml = os.path.join(self.__detectorpath,"ScreenDetectors.xml")
        fp = open(scdexml,"w")
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
    def Get_GUIPoint(self,PointType:PointType)->GUIPoint:
        #TODO:通过双击屏幕计算GUIPoint
        (x,y) = KMMins.Get_mouse_when_double_click()
        point = Vector2(x,y)
        resGP = GUIPoint(point)
        return resGP
    def Add_Button(self,name,PointType:PointType)->bool:
        print("please double click to locate the button")
        butopoint = self.Get_GUIPoint(PointType)
        return BMins.Add_Button(name,butopoint)
    def Add_ScreenDetector(self,name,PointType:PointType)->bool:
        flag = False
        print("please double click to locate the region")
        deteLT = self.Get_GUIPoint(PointType)
        print("please double click again to locate the region")
        deteRB = self.Get_GUIPoint(PointType)
        print(f"please double click to locate the img")
        imgLT = self.Get_GUIPoint(PointType)
        print(f"please double click again to locate the img")
        imgRB = self.Get_GUIPoint(PointType)
        #TODO:check region > img
        LT = imgLT.Get_point()
        RB = imgRB.Get_point()
        deteimgn = KMMins.Screenshot(region=(LT.x,LT.y,RB.x-LT.x,RB.y-LT.y))
        flag = SDMins.Add_Detector(name,deteimgn,RegionLT=deteLT,RegionRB=deteRB)
        return flag
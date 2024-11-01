from Base.GUIPoint import GUIPoint
from Base.KeyMouseMu import KeyMouseMu
from typing import Optional
import xml.etree.ElementTree as ET
import os
class ButtonManager:
    __instance: Optional['ButtonManager'] = None
    __Buttons: dict[str,GUIPoint]
    __path:str

    def load(self):
        if not os.path.exists(self.__path):
            assert False, f"ButtonManager: {self.__path} not exist"
        if os.path.getsize(self.__path) == 0:
            return
        tree = ET.parse(self.__path)
        root = tree.getroot()
        self.__Buttons = {}
        for elem in root.findall("Button"):
            name = elem.get("name")
            if not name:
                print("warning", "Button name is empty")
                continue
            point = GUIPoint.default()
            pointelem = elem.find("Point")
            if pointelem is not None:
                point = GUIPoint.from_xml_element(pointelem)
            else: 
                print("warning", f"Button: {name} Point is empty")
            self.__Buttons[name] = point
        return
    def save(self):
        if not hasattr(self, '_ButtonManager__Buttons'):
            return
        root = ET.Element("ButtonManager")
        for name,point in self.__Buttons.items():
            elem = ET.Element("Button")
            elem.set("name",name)
            pointelem = ET.Element("Point")
            pointelem.append(point.to_xml_element())
            elem.append(pointelem)
            root.append(elem)
        tree = ET.ElementTree(root)
        from builtins import open
        tree.write(self.__path,encoding="utf-8",xml_declaration=True)
    @classmethod
    def Get_instance(cls)->'ButtonManager':
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __new__(cls,*args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        return
    def __del__(self):
        return
    def Init(self,path:str):
        if not os.path.exists(path):
            assert False, f"ButtonManager: {path} not exist"
        self.__path = path
        self.load()
        return
    def Add_Button(self,name,Point:GUIPoint)->bool:
        if not hasattr(self, '_ButtonManager__Buttons'):
            self.__Buttons = {}
        if self.__Buttons.get(name , None) is not None:
            print("warning", f"Button: {name} already exist")
            return False
        self.__Buttons[name]=Point
        return True
    def Remove_Button(self,name)->bool:
        if self.__Buttons.get(name , 0):
            print("warning", f"Button: {name} not exist")
            return False
        del self.__Buttons[name]
        return True
    def Click_Button(self,name)->bool:
        if not self.__Buttons.get(name , 0):
            print("warning", f"Button: {name} not exist")
            return False
        KKMins = KeyMouseMu.Get_instance()
        tempVec = self.__Buttons[name].Get_point()
        KKMins.Click_mouse_rel(tempVec.x,tempVec.y)
        return True
    
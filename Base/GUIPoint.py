import Vector2
from enum import Enum, auto
import xml.etree.ElementTree as ET
class PointType(Enum):
    Topleft = auto()
    Topcenter = auto()
    Topright = auto()
    Centerleft = auto()
    Center = auto()
    Centerright = auto()
    Bottomleft = auto()
    Bottomcenter = auto()
    Bottomright = auto()
    description = "the way to locate the point on the GUI"
class PointSzieRelated(Enum):
    WindowWidth = auto()
    WindowHigh = auto()
    WindowHighAWidth = auto()
    Else = auto()
    description = "the way to confirm the point location"
class GUIPoint:
    #可变属性
    __base_point = Vector2.Vector2(0, 0)
    #静态属性
    __gui_LeftTop = Vector2.Vector2(0, 0)
    __gui_size = Vector2.Vector2(0, 0)
    #不可变属性
    __point_factor = Vector2.Vector2(0, 0)
    __type = PointType.Center
    __related_size = PointSzieRelated.WindowWidth

    @classmethod
    def Update_gui(cls, lefttop:Vector2.Vector2, size:Vector2.Vector2):
        cls.__gui_LeftTop = lefttop
        cls.__gui_size = size
        for updateBP in dir(GUIPoint):
            if callable(getattr(cls, updateBP))and updateBP == "__update_base_point" :
                getattr(cls,updateBP)()
        return
    def __update_base_point(self):
        match self.__type:
            case PointType.Topleft|PointType.Centerleft|PointType.Bottomleft:
                self.__base_point.x = self.__gui_LeftTop.x
            case PointType.Topcenter|PointType.Center|PointType.Bottomcenter:
                self.__base_point.x = self.__gui_LeftTop.x + self.__gui_size.x / 2
            case PointType.Topright|PointType.Centerright|PointType.Bottomright:
                self.__base_point.x = self.__gui_LeftTop.x + self.__gui_size.x
        match self.__type:
            case PointType.Topleft|PointType.Topcenter|PointType.Topright:
                self.__base_point.y = self.__gui_LeftTop.y
            case PointType.Centerleft|PointType.Center|PointType.Centerright:
                self.__base_point.y = self.__gui_LeftTop.y + self.__gui_size.y / 2 +20 #窗体标题尺寸
            case PointType.Bottomleft|PointType.Bottomcenter|PointType.Bottomright:
                self.__base_point.y = self.__gui_LeftTop.y + self.__gui_size.y
    def Get_point(self):
        resx ,resy = 0,0
        match self.__related_size:
            case PointSzieRelated.WindowWidth:
                resx = self.__base_point.x + self.__point_factor.x * self.__gui_size.x
                resy = self.__base_point.y + self.__point_factor.y * self.__gui_size.x
            case PointSzieRelated.WindowHigh:
                resx = self.__base_point.x + self.__point_factor.x * self.__gui_size.y
                resy = self.__base_point.y + self.__point_factor.y * self.__gui_size.y
            case PointSzieRelated.WindowHighAWidth:
                resx = self.__base_point.x + self.__point_factor.x * self.__gui_size.x
                resy = self.__base_point.y + self.__point_factor.y * self.__gui_size.y
            case PointSzieRelated.Else:
                assert False, "PointSzieRelated.Else has not been implemented"
        return Vector2.Vector2(resx, resy)
    def __init_factor(self, point:Vector2.Vector2):
        match self.__related_size:
            case PointSzieRelated.WindowWidth:
                self.__point_factor.x = (point.x - self.__base_point.x) / self.__gui_size.x
                self.__point_factor.y = (point.y - self.__base_point.y)/ self.__gui_size.x
            case PointSzieRelated.WindowHigh:
                self.__point_factor.x = (point.x - self.__base_point.x) / self.__gui_size.y
                self.__point_factor.y = (point.y - self.__base_point.y) / self.__gui_size.y
            case PointSzieRelated.WindowHighAWidth:
                self.__point_factor.x = (point.x - self.__base_point.x) / self.__gui_size.x
                self.__point_factor.y = (point.y - self.__base_point.y) / self.__gui_size.y
            case PointSzieRelated.Else:
                assert False, "PointSzieRelated.Else has not been implemented"
        return
    def __init__(self, point:Vector2.Vector2,lefttop:Vector2.Vector2=Vector2.Vector2(-1,-1), size:Vector2.Vector2=Vector2.Vector2(-1,-1), type=PointType.Center, related_size=PointSzieRelated.WindowWidth,factor=Vector2.Vector2(-1,-1)):
        self.__type = type
        self.__related_size = related_size
        if lefttop.x + lefttop.y + size.x +size.y != -4:
            self.Update_gui(lefttop, size)
        else :self.__update_base_point()
        if factor.x + factor.y == -2:
            self.__init_factor(point)
        return
    @classmethod
    def default(cls):
        return cls(Vector2.Vector2(0,0))
    def __sub__(self, other):
        return Vector2.Vector2(self.Get_point().x - other.Get_point().x, self.Get_point().y - other.get_point().y)

    def to_xml_element(self)->ET.Element:
        elem = ET.Element("GUIPoint")
        elem.set("type", self.__type.name)
        elem.set("related_size", self.__related_size.name)
        Vector2elem = self.__point_factor.to_xml_element()
        Vector2elem.tag = "point_factor"
        elem.append(Vector2elem)
        return elem
    @classmethod
    def from_xml_element(cls, elem:ET.Element)->"GUIPoint":
        type_str = elem.get("type")
        type = PointType[type_str] if type_str is not None else PointType.Center
        relate_size_str = elem.get("related_size")
        related_size = PointSzieRelated[relate_size_str] if relate_size_str is not None else PointSzieRelated.WindowWidth
        pfelem = elem.find("point_factor")
        point_factor = Vector2.Vector2(0,0)
        if pfelem is not None:
            point_factor = Vector2.Vector2.from_xml_element(pfelem)
        return cls(Vector2.Vector2(0,0), type=type, related_size=related_size, factor=point_factor)
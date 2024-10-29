import Vector2
from enum import Enum,auto
class PointType:
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
class PointSzieRelated:
    WindowWidth = auto()
    WindowHigh = auto()
    WindowHighAWidth = auto()
    Else = auto()
    description = "the way to confirm the point location"
class GUIPoint:
    #动态属性
    __base_point = Vector2.Vector2(0, 0)
    __gui_LeftTop = Vector2.Vector2(0, 0)
    __gui_size = Vector2.Vector2(0, 0)
    #静态属性
    __point_factor = Vector2.Vector2(0, 0)
    __type = PointType.Center
    __related_size = PointSzieRelated.WindowWidth

    @classmethod
    def update_gui(cls, lefttop:Vector2.Vector2, size:Vector2.Vector2):
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
    def get_point(self):
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
    def __init__(self, point:Vector2.Vector2,lefttop:Vector2.Vector2=Vector2.Vector2(-1,-1), size:Vector2.Vector2=Vector2.Vector2(-1,-1), type=PointType.Center, related_size=PointSzieRelated.WindowWidth):
        self.__type = type
        self.__related_size = related_size
        if lefttop.x + lefttop.y + size.x +size.y != -4:
            self.update_gui(lefttop, size)
        else :self.__update_base_point()
        self.__init_factor(point)
        return
    def __sub__(self, other):
        return Vector2.Vector2(self.get_point().x - other.get_point().x, self.get_point().y - other.get_point().y)

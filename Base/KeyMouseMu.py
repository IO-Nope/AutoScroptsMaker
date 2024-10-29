import pyautogui
import Vector2
class KeyMouseMu:
    __instance = None
    __move_time = 0.3
    __mufunc = pyautogui
    __mouse_pre_pos = Vector2.Vector2(0,0)
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    def __init__(self):
        self.__mouse_pre_pos = Vector2.Vector2(0,0)
        return
    def __update_pre_pos(self, x, y):
        self.__mouse_pre_pos.x = x
        self.__mouse_pre_pos.y = y
        return
    def set_move_time(self, t):
        self.__move_time = t
        return
    def move_mouse(self, x, y):
        self.__mufunc.moveTo(x, y)
        self.__update_pre_pos(x, y)
        return
    def move_mouse_rel(self, x, y):
        self.__mufunc.moveRel(x, y, self.__move_time)
        self.__update_pre_pos(x, y)
        return
    def click_mouse(self, x, y, button='left'):
        if button == 'left':
            self.__mufunc.click(x, y)
        elif button == 'right':
            self.__mufunc.click(x, y, button='right')
        return
    def click_mouse_rel(self, x, y, button='left'):
        self.move_mouse_rel(x, y)
        if button == 'left':
            self.__mufunc.click(x, y)
        elif button == 'right':
            self.__mufunc.click(x, y, button='right')
        return
    def press(self, key):
        self.__mufunc.press(key)
        return
    def screenshot(self, region=None):
        screenshot = pyautogui.screenshot(region=region)
        return screenshot
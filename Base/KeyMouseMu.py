import pyautogui
import Vector2
from typing import Optional
from pynput import mouse, keyboard
import threading

class KeyMouseMu:
    __instance: Optional['KeyMouseMu'] = None
    __move_time = 0.3
    __mufunc = pyautogui
    __mouse_pre_pos = Vector2.Vector2(0,0)
    @classmethod
    def Get_instance(cls)->'KeyMouseMu':
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
    def Set_move_time(self, t):
        self.__move_time = t
        return
    def Move_mouse(self, x, y):
        self.__mufunc.moveTo(x, y)
        self.__update_pre_pos(x, y)
        return
    def Move_mouse_rel(self, x, y):
        self.__mufunc.moveRel(x, y, self.__move_time)
        self.__update_pre_pos(x, y)
        return
    def Click_mouse(self, x, y, button='left'):
        if button == 'left':
            self.__mufunc.click(x, y)
        elif button == 'right':
            self.__mufunc.click(x, y, button='right')
        return
    def Click_mouse_rel(self, x, y, button='left'):
        self.Move_mouse_rel(x, y)
        if button == 'left':
            self.__mufunc.click(x, y)
        elif button == 'right':
            self.__mufunc.click(x, y, button='right')
        return
    def Press(self, key):
        self.__mufunc.press(key)
        return
    def Screenshot(self, region=None):
        screenshot = pyautogui.screenshot(region=region)
        return screenshot
    def Get_mouse_pos(self):
        return pyautogui.position()
    def Get_mouse_when_double_click(self):
        stop_event = threading.Event()
        positon = Vector2.Vector2(0,0)
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                if positon.x ==x and positon.y == y:
                    positon.x = x
                    positon.y = y
                    stop_event.set()
                positon.x = x
                positon.y = y
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        stop_event.wait()
        listener.stop()
    
        return (positon.x, positon.y)
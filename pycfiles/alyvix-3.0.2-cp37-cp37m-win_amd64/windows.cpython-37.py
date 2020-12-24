# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\python\envs\alyvix\alyvix_py37\lib\site-packages\alyvix\core\interaction\mouse\windows.py
# Compiled at: 2019-11-11 12:27:44
# Size of source mod 2**32: 6147 bytes
from .base import MouseManagerBase
from ctypes import *
import time, sys, os

class MouseManager(MouseManagerBase):

    def __init__(self):
        super(MouseManager, self).__init__()
        self.ahk = None
        self._coordmode = 'CoordMode "Mouse", "Screen"'
        autohotkey_dll_fullname = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'ahkdll_x64w' + os.sep + 'AutoHotkey.dll'
        self.ahk = CDLL(autohotkey_dll_fullname)
        self.ahk.ahktextdll('')
        while not self.ahk.ahkReady():
            time.sleep(0.01)

        self._scaling_factor = 1

    def click(self, x, y, button=1, n_clicks=1, click_delay=10):
        xs = int(x / self._scaling_factor)
        ys = int(y / self._scaling_factor)
        self.move(xs, ys)
        for cnt_click in range(n_clicks):
            if button == self.left_button:
                self.ahk.ahkExec(self._coordmode + '\nClick "' + str(xs) + ' ' + str(ys) + '"')
            else:
                if button == self.right_button:
                    self.ahk.ahkExec(self._coordmode + '\nClick "right ' + str(xs) + ' ' + str(ys) + '"')
                else:
                    if button == self.middle_button:
                        self.ahk.ahkExec(self._coordmode + '\nClick "middle ' + str(xs) + ' ' + str(ys) + '"')
            time.sleep(click_delay / 1000)

    def move(self, x, y):
        xs = int(x / self._scaling_factor)
        ys = int(y / self._scaling_factor)
        self.ahk.ahkExec(self._coordmode + '\nClick "' + str(xs) + ' ' + str(ys + 5) + ' 0"')
        time.sleep(0.25)
        self.ahk.ahkExec(self._coordmode + '\nClick "' + str(xs) + ' ' + str(ys) + ' 0"')

    def scroll(self, x, y, steps, direction, scroll_delay):
        xs = int(x / self._scaling_factor)
        ys = int(y / self._scaling_factor)
        self.move(xs, ys)
        cnt = 0
        if direction == self.wheel_down or direction == self.wheel_up:
            for step in range(0, steps, 1):
                if direction == self.wheel_down:
                    self.ahk.ahkExec(self._coordmode + '\nClick "WheelDown"')
                else:
                    if direction == self.wheel_up:
                        self.ahk.ahkExec(self._coordmode + '\nClick "WheelUp"')
                time.sleep(scroll_delay / 1000)

        else:
            if direction == self.wheel_left or direction == self.wheel_right:
                if direction == self.wheel_left:
                    self.ahk.ahkExec(self._coordmode + '\nClick "middle"')
                    time.sleep(0.5)
                    self.ahk.ahkExec(self._coordmode + '\nClick "' + str(xs - steps) + ' ' + str(ys) + ' 0"')
                    time.sleep(scroll_delay / 1000)
                    self.ahk.ahkExec(self._coordmode + '\nClick "middle"')
                else:
                    if direction == self.wheel_right:
                        self.ahk.ahkExec(self._coordmode + '\nClick "middle"')
                        time.sleep(0.5)
                        self.ahk.ahkExec(self._coordmode + '\nClick "' + str(xs + steps) + ' ' + str(ys) + ' 0"')
                        time.sleep(scroll_delay / 1000)
                        self.ahk.ahkExec(self._coordmode + '\nClick "middle"')

    def hold(self, x, y):
        xs = int(x / self._scaling_factor)
        ys = int(y / self._scaling_factor)
        self.ahk.ahkExec(self._coordmode + '\nClick "' + str(xs) + ' ' + str(ys) + ' 0"')
        time.sleep(0.25)
        self.ahk.ahkExec(self._coordmode + '\nClick "down"')
        time.sleep(0.25)
        self.ahk.ahkExec(self._coordmode + '\nClick "' + str(xs) + ' ' + str(ys + 5) + ' 0"')
        time.sleep(0.25)

    def release(self, x, y):
        xs = int(x / self._scaling_factor)
        ys = int(y / self._scaling_factor)
        self.ahk.ahkExec(self._coordmode + '\nClick "' + str(xs) + ' ' + str(ys) + ' 0"')
        time.sleep(0.25)
        self.ahk.ahkExec(self._coordmode + '\nClick "up"')

    def drag(self, x1, y1, x2, y2, button=1):
        x1s = int(x1 / self._scaling_factor)
        y1s = int(y1 / self._scaling_factor)
        x2s = int(x2 / self._scaling_factor)
        y2s = int(y2 / self._scaling_factor)
        if button == self.left_button:
            self.ahk.ahkExec(self._coordmode + '\nClick "' + str(x1s) + ' ' + str(y1s) + ' 0"')
            time.sleep(0.5)
            self.ahk.ahkExec(self._coordmode + '\nClick "down"')
            time.sleep(0.5)
            self.ahk.ahkExec(self._coordmode + '\nClick "' + str(x2s) + ' ' + str(y2s) + ' 0"')
            time.sleep(0.5)
            self.ahk.ahkExec(self._coordmode + '\nClick "up"')
        else:
            if button == self.right_button:
                self.ahk.ahkExec(self._coordmode + '\nClick "' + str(x1s) + ' ' + str(y1s) + ' 0"')
                time.sleep(0.5)
                self.ahk.ahkExec(self._coordmode + '\nClick "right down"')
                time.sleep(0.5)
                self.ahk.ahkExec(self._coordmode + '\nClick "' + str(x2s) + ' ' + str(y2s) + ' 0"')
                time.sleep(0.5)
                self.ahk.ahkExec(self._coordmode + '\nClick "right up"')
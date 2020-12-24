# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dspc_bot_ctrl\window_manager.py
# Compiled at: 2020-03-15 02:34:07
# Size of source mod 2**32: 1389 bytes
import logging, win32gui, win32com.client
lformat = '[*] %(asctime)s ::: %(levelname)s - %(message)s'
logging.basicConfig(format=lformat)
logger = logging.getLogger('pccbot_log')
logger.setLevel(logging.DEBUG)

class WindowMgr:

    def __init__(self, type):
        self._handle = None
        self.type = type

    def find_window(self, class_name, window_name=None):
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        if self.type == 0:
            if wildcard == str(win32gui.GetWindowText(hwnd)):
                logger.info('Changing active window to ' + str(win32gui.GetWindowText(hwnd)) + ' for exact wildcard')
                self._handle = hwnd
        elif self.type == 1:
            if wildcard in str(win32gui.GetWindowText(hwnd)).lower():
                logger.info('Changing active window to ' + str(win32gui.GetWindowText(hwnd)) + ' for within wildcard')
                self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        shell = win32com.client.Dispatch('WScript.Shell')
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self._handle)
        logger.info('Active window changed')
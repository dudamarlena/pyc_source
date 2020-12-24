# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\eyedropper.py
# Compiled at: 2018-08-17 15:26:38
# Size of source mod 2**32: 238 bytes
import pyautogui, pyperclip

def run():
    img = pyautogui.screenshot()
    color = img.getpixel(pyautogui.position())
    pyperclip.copy(('#{0:02x}{1:02x}{2:02x}'.format)(*color))


if __name__ == '__main__':
    run()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/qrcode/utils.py
# Compiled at: 2019-06-07 02:02:02
# Size of source mod 2**32: 154 bytes
import cv2

def window_is_open(window_name):
    return cv2.waitKey(1) and cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) == 1.0
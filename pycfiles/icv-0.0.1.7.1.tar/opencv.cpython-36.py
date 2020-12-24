# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/opencv.py
# Compiled at: 2019-04-20 14:11:24
# Size of source mod 2**32: 132 bytes
import cv2

def use_opencv2():
    return cv2.__version__.split('.')[0] == '2'


USE_OPENCV2 = use_opencv2()
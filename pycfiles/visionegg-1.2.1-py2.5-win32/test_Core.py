# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\test_Core.py
# Compiled at: 2009-07-07 11:29:44
from VisionEgg.Core import FrameTimer

def test_FrameTimer():
    ft = FrameTimer()
    ft.tick()
    ft.tick()
    result = ft.get_longest_frame_duration_sec()
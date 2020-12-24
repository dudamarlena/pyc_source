# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/functions/perceptual/camera/is_center_black_line.py
# Compiled at: 2019-04-07 11:14:15
from __future__ import print_function, absolute_import
import numpy as np, sys, os
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import visual_auxiliary as va

def is_center_black_line(lbot):
    frame = lbot.getImage()
    rois = va.detect_black_line(frame)
    maxIndex = np.argmax(rois)
    if maxIndex == 1 and rois[maxIndex] > 20:
        return True
    return False
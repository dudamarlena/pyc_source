# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/functions/perceptual/camera/is_up_face.py
# Compiled at: 2019-04-07 11:14:15
from __future__ import print_function, absolute_import
import sys, os
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import visual_auxiliary as va

def is_up_face(lbot):
    frame = lbot.getImage()
    mat = va.detect_face(frame)
    if mat[0][0] is not 0 or mat[0][1] is not 0 or mat[0][2] is not 0:
        return True
    return False
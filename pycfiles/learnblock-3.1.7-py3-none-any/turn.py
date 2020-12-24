# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/functions/motor/base/turn.py
# Compiled at: 2019-04-07 11:14:15
from __future__ import print_function, absolute_import
import time, math

def turn(lbot, angle=0):
    lbot.setBaseSpeed(lbot.getAdv(), math.radians(angle))
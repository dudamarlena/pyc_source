# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/functions/proprioceptive/base/near_to_target.py
# Compiled at: 2019-04-07 11:14:15
import math as m

def near_to_target(lbot, targetX, targetY, nearDist=50):
    x, y, alpha = lbot.getPose()
    distToTarget = m.sqrt(m.pow(x - targetX, 2) + m.pow(y - targetY, 2))
    if distToTarget <= nearDist:
        return True
    return False
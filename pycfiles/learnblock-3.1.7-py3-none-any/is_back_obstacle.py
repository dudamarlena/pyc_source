# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/functions/perceptual/distancesensors/is_back_obstacle.py
# Compiled at: 2019-04-07 11:14:15


def is_back_obstacle(lbot, threshold=200):
    sonarsValue = lbot.getSonars()
    if sonarsValue['back'] < threshold:
        return True
    return False
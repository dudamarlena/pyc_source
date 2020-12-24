# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/functions/perceptual/distancesensors/get_min_distance.py
# Compiled at: 2019-04-07 11:14:15


def get_min_distance(lbot, left=0, front=1, right=0):
    sonarsValue = lbot.getSonars()
    if left:
        return min(sonarsValue['left'])
    else:
        if front:
            return min(sonarsValue['front'])
        if right:
            return min(sonarsValue['right'])
        return min(map(lambda x: min(x), sonarsValue.values()))
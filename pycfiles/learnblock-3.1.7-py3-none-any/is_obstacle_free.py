# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/functions/perceptual/distancesensors/is_obstacle_free.py
# Compiled at: 2019-04-07 11:14:15


def is_obstacle_free(lbot, threshold=200):
    sonarsvalue = lbot.getSonars()
    values = sonarsvalue['front']
    values += sonarsvalue['left']
    values += sonarsvalue['right']
    if min(values) < threshold:
        return True
    return False
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astro_py/component/my_timedelta.py
# Compiled at: 2019-10-14 11:32:31
# Size of source mod 2**32: 1578 bytes
from datetime import timedelta
import numpy as np
TIMEDELTA = 1
TIMEDELTADEG = 2
TIMEDELTAMIN = 3

def compute(self, swTimeDelta):
    """ Return ° in sign value """
    ms = self.microseconds
    sec = self.seconds
    hours = sec // 3600
    minutes = sec // 60 - hours * 60
    secondes = sec - minutes * 60 - hours * 60 * 60
    if secondes <= 59:
        if ms >= 500000:
            secondes += 1
    elif ms >= 500000:
        secondes = 0
        if minutes <= 59:
            minutes += 1
        else:
            minutes = 0
            hours += 1
    days = int(self.days)
    d = self / np.timedelta64(1, 'D').astype(int)
    stringDays = int(d.days)
    calc = int(hours + int(d.days) * 24)
    switcher = {TIMEDELTA: "{}°{}'{}''".format(calc, str(minutes).zfill(2), str(secondes).zfill(2)), 
     TIMEDELTADEG: 'degre{}'.format(calc), 
     TIMEDELTAMIN: 'min{}'.format(str(minutes).zfill(2))}
    return switcher.get(swTimeDelta, '?')


class my_timedelta(timedelta):

    def __str__(self):
        """ Return __°__'__'' in sign value """
        return compute(self, TIMEDELTA)


class my_timedelta_deg(timedelta):

    def __str__(self):
        """ Return only __° in sign value"""
        return compute(self, TIMEDELTADEG)


class my_timedelta_min(timedelta):

    def __str__(self):
        """ Return only __' in sign value"""
        return compute(self, TIMEDELTAMIN)
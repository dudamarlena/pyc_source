# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/prog/hoerkules/software/core/env/lib/python3.5/site-packages/RPiSim/PIN.py
# Compiled at: 2016-06-27 12:07:44
# Size of source mod 2**32: 261 bytes


class PIN:
    SetMode = 'None'
    Out = '0'
    pull_up_down = 'PUD_OFF'
    In = '1'

    def __init__(self, SetMode):
        self.SetMode = SetMode
        self.Out = '0'
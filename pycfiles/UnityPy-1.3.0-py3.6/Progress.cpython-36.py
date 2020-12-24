# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\Progress.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 387 bytes


class Progress:
    pre_value: int

    def reset(self):
        self.pre_value = 0
        self.report(0)

    def report(self, current: int, total: int=None):
        if total:
            value = current * 100 // total
        else:
            value = current
        if value > self.pre_value:
            self.pre_value = value
            print(f"{value}%")
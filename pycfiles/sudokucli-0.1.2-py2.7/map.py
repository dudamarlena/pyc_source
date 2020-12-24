# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\src\abs\map.py
# Compiled at: 2018-08-21 23:22:13


class Map(object):

    def __init__(self):
        self.rows = 9
        self.cols = 9
        self.min_rows = 3
        self.min_cols = 3
        self.numList = []

    def check_legal(self):
        if len(self.numList) != 9:
            raise Exception('')
        for nums in self.numList:
            if len(nums) != 9:
                raise Exception('')

        return True
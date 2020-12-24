# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\mode\returncodes.py
# Compiled at: 2016-07-05 08:01:48
# Size of source mod 2**32: 211 bytes


class Returncodes:
    OK = 0
    Warning = 1
    Critical = 2
    Unknown = 3

    @staticmethod
    def name(nr):
        return next(name for name, value in vars(Returncodes).items() if value == nr)
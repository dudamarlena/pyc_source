# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\helper\time_converter.py
# Compiled at: 2016-07-05 08:30:27


class Units:
    ms = 1
    s = ms * 1000
    m = s * 60
    h = m * 60
    d = h * 24

    @classmethod
    def fromstring(cls, string):
        return getattr(cls, string.lower(), None)


def string_to_ms(string):
    unit = string[-1:]
    value = int(string[:-1])
    return int(value * Units.fromstring(unit))
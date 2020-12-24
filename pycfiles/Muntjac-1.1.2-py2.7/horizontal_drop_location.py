# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/client/ui/dd/horizontal_drop_location.py
# Compiled at: 2013-04-04 15:36:36


class HorizontalDropLocation(object):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    CENTER = 'CENTER'
    _values = [
     LEFT, RIGHT, CENTER]

    @classmethod
    def values(cls):
        return cls._enum_values[:]

    @classmethod
    def valueOf(cls, name):
        for v in cls._values:
            if v.lower() == name.lower():
                return v
        else:
            return

        return
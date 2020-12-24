# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\util\cbProps.py
# Compiled at: 2013-03-15 12:05:06
"""Vm property getters/setters/translators."""

class Prop(object):
    _readName = _writeName = None

    def __init__(self, name, cliName=None, extraCb=False):
        self._readName = name
        self.extraCb = extraCb
        if cliName:
            self._writeName = cliName
        else:
            self._writeName = name

    def fromCli(self, val):
        return val

    def toCli(self, val):
        return val

    def __get__(self, instance, owner):
        assert instance is not None
        if callable(self._readName):
            name = self._readName(instance)
        else:
            name = self._readName
        val = instance.getProp(name)
        return self.fromCli(val)

    def __set__(self, instance, val):
        if callable(self._writeName):
            name = self._writeName(instance)
        else:
            name = self._writeName
        val = self.toCli(val)
        instance.setProp(name, val)
        extraCb = self.extraCb
        if extraCb:
            extraCb(instance, val)


class String(Prop):
    """Just a class to explicilty state type of a property."""
    pass


class Switch(Prop):
    """on/off property."""
    trueVals = ('on', )
    falseVals = ('off', 'none')
    outTrue = 'on'
    outFalse = 'off'

    def fromCli(self, val):
        assert val in self.trueVals or val in self.falseVals or val is None, val
        return val in self.trueVals

    def toCli(self, val):
        if val:
            return self.outTrue
        return self.outFalse


class Int(Prop):

    def fromCli(self, val):
        return int(val)
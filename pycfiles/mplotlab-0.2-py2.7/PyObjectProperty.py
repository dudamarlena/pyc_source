# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\graphics\PyObjectProperty.py
# Compiled at: 2016-02-07 09:44:32
import wx.propgrid as wxpg

class PyObjectPropertyValue:

    def __init__(self, s=None):
        try:
            self.ls = [ a.strip() for a in s.split('-') ]
        except:
            self.ls = []

    def __repr__(self):
        return (' - ').join(self.ls)


class PyObjectProperty(wxpg.PyProperty):

    def __init__(self, label, name=wxpg.LABEL_AS_NAME, value=None):
        wxpg.PyProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        return self.__class__.__name__

    def GetEditor(self):
        return 'TextCtrl'

    def ValueToString(self, value, flags):
        return repr(value)

    def StringToValue(self, s, flags):
        v = PyObjectPropertyValue(s)
        return (True, v)
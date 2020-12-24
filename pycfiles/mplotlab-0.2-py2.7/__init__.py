# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\__init__.py
# Compiled at: 2016-02-07 09:56:43
""" description here
"""
__version__ = '0.1'
__date__ = '21/10/2015'
import sys, wx
try:
    if not hasattr(sys, 'frozen'):
        import wxversion
        wxversion.ensureMinimal('2.8')
except ImportError:
    pass
except:
    pass

class App(object):
    __instance = None

    def __new__(cls, *a, **k):
        if cls.__instance is None:
            cls.__instance = App.newApp(*a, **k)
        return cls.__instance

    @staticmethod
    def newApp(*a, **k):
        app = wx.App(*a, **k)
        app.mainWin = newWxPlotFrame()
        app.SetTopWindow(app.mainWin)
        app.mainWin.Show()
        return app


from utils import log, configParser, msgMap, createError, getErrHdlr, regErrHdlr, remErrHdlr, checkTypeParams, checkTypeReturned
from mplotlab.models import Slide, Variable, Collection, Projection, Container
from graphics import newWxPlotFrame, newWxPlotPanel
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/test/testView.py
# Compiled at: 2008-06-30 11:43:30
from dbsprockets.view import View
from tw.api import Widget
from dbsprockets.viewconfig import ViewConfig
from dbsprockets.metadata import Metadata
from dbsprockets.iprovider import IProvider

class testView:

    def setup(self):
        provider = IProvider()
        viewConfig = ViewConfig(provider, '')
        self.view = View(Widget(), viewConfig)

    def testCreate(self):
        pass

    def testDisplay(self):
        s = self.view.widget(value={})
        assert s == None, s
        return
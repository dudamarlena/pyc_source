# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/viewfactory.py
# Compiled at: 2008-06-30 11:43:48
from view import View

class ViewFactory:

    def create(self, viewConfig, id=None):
        kw = viewConfig.getWidgetArgs()
        if id == None:
            id = viewConfig.__class__.__name__ + '_' + viewConfig.identifier
        kw['id'] = id
        parentWidget = viewConfig.widgetType(**kw)
        return View(parentWidget, viewConfig)
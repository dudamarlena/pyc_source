# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/skin/standardmacros.py
# Compiled at: 2006-09-21 05:27:37
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.basicskin.standardmacros import StandardMacros as BaseMacros

class WorldCookeryMacros(BrowserView):
    __module__ = __name__
    template = ViewPageTemplateFile('worldcookery.pt')

    def __getitem__(self, key):
        return self.template.macros[key]


class StandardMacros(BaseMacros):
    __module__ = __name__
    macro_pages = ('worldcookery_macros', )
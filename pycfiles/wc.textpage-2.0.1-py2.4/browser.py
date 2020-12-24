# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/wc/textpage/browser.py
# Compiled at: 2007-02-23 15:42:05
from zope.component import createObject, getMultiAdapter
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile

class ViewPage(BrowserPage):
    __module__ = __name__
    __call__ = ViewPageTemplateFile('view.pt')

    def render(self):
        source = createObject(self.context.type, self.context.text)
        view = getMultiAdapter((source, self.request))
        return view.render()
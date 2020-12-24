# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/extdirect/zope/metaconfigure.py
# Compiled at: 2010-02-06 11:39:35
from zope.interface import Interface
from zope.viewlet.metaconfigure import viewletDirective
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.viewlet.viewlet import ViewletBase
try:
    from Products.Five.browser.metaconfigure import page
except ImportError:
    from zope.app.publisher.browser.viewmeta import page

from extdirect.router import DirectProviderDefinition
from interfaces import IExtDirectJavaScriptManager

class SourceViewletBase(ViewletBase):
    _source = ''
    weight = 0

    def render(self):
        return self._source


def JavaScriptSourceViewlet(source):
    klass = type('JavaScriptSourceViewlet', (
     SourceViewletBase,), {'_source': source, 'weight': 2})
    return klass


def directRouter(_context, name, class_, namespace, timeout=None, for_=Interface, layer=IDefaultBrowserLayer):
    page(_context, name, 'zope.Public', for_, layer, class_=class_)
    source = DirectProviderDefinition(class_, name, namespace, timeout).render()
    viewletclass = JavaScriptSourceViewlet(source)
    viewletDirective(_context, name, 'zope.Public', for_, layer, manager=IExtDirectJavaScriptManager, class_=viewletclass)
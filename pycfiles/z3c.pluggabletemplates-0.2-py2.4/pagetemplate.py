# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/pluggabletemplates/pagetemplate.py
# Compiled at: 2006-11-01 03:49:22
"""
$Id: pagetemplate.py 70786 2006-10-18 14:33:55Z jukart $
"""
__docformat__ = 'reStructuredText'
from zope import interface
from zope import component
from zope.pagetemplate.interfaces import IPageTemplate
from zope.publisher.browser import BrowserView

class RegisteredPageTemplate(object):
    __module__ = __name__

    def __init__(self, name=None):
        self.name = name

    def __call__(self, instance, *args, **keywords):
        import sys
        if self.name:
            template = component.getMultiAdapter((instance, instance.request), IPageTemplate, name=self.name)
        else:
            template = component.getMultiAdapter((instance, instance.request), IPageTemplate)
        if isinstance(template, tuple):
            template = template[1]
        return template(instance, *args, **keywords)

    def __get__(self, instance, type):
        return BoundRegisteredPageTemplate(self, instance)


class BoundRegisteredPageTemplate(object):
    __module__ = __name__

    def __init__(self, pt, ob):
        object.__setattr__(self, 'im_func', pt)
        object.__setattr__(self, 'im_self', ob)

    def __call__(self, *args, **kw):
        if self.im_self is None:
            im_self, args = args[0], args[1:]
        else:
            im_self = self.im_self
        return self.im_func(im_self, *args, **kw)

    def __setattr__(self, name, v):
        raise AttributeError("Can't set attribute", name)

    def __repr__(self):
        return '<BoundRegisteredPageTemplateFile of %r>' % self.im_self
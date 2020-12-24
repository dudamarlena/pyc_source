# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/masturbozpt/template.py
# Compiled at: 2006-01-06 22:24:14
"""
By VladDrac@irc.freenode.net/#turbogears
+ Some small modifications
"""
from zope.pagetemplate import pagetemplatefile
import os.path, sys

class Here(object):
    __module__ = __name__

    def __init__(self, base):
        self.base = base

    def __getattr__(self, name):
        tpl = PageTemplate(os.path.join(self.base, name))
        return tpl


class PageTemplate(pagetemplatefile.PageTemplateFile):
    __module__ = __name__

    def __init__(self, name):
        base = os.path.dirname(sys._getframe(1).f_globals['__file__'])
        self.extra_context = {}
        self.name = name
        self.fullpath = os.path.join(base, self.name)
        self.base = os.path.dirname(self.fullpath)
        pagetemplatefile.PageTemplateFile.__init__(self, self.fullpath)

    def render(self, extra_dict=None):
        if extra_dict:
            context = self.pt_getContext()
            context.update(extra_dict)
        return self.pt_render(context)

    def add_context(self, d):
        self.extra_context.update(d)

    def pt_getContext(self, args=(), options={}, **ignored):
        rval = pagetemplatefile.PageTemplateFile.pt_getContext(self, args, options, **ignored)
        rval.update(options)
        rval.update(self.extra_context)
        rval.update({'here': Here(self.base), 'template': self})
        return rval
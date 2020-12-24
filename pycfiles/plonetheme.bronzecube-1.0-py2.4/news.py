# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/bronzecube/browser/portlets/news.py
# Compiled at: 2010-02-07 14:25:20
from plone.app.portlets.portlets.news import Renderer as BaseRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Renderer(BaseRenderer):
    __module__ = __name__
    _template = ViewPageTemplateFile('news.pt')
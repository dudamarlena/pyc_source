# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/bronzecube/browser/portlets/login.py
# Compiled at: 2010-02-07 14:25:20
from plone.app.portlets.portlets.login import Renderer as BaseRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Renderer(BaseRenderer):
    __module__ = __name__
    render = ViewPageTemplateFile('login.pt')
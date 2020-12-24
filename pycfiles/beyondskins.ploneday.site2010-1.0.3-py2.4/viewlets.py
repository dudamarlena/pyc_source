# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat/egg/beyondskins/ploneday/site2010/browser/viewlets.py
# Compiled at: 2010-04-15 11:12:59
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import LogoViewlet
from plone.app.layout.viewlets.common import ViewletBase

class MyLogo(LogoViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/logo.pt')
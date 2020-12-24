# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/alterootheme/intensesimplicity/browser/viewlets.py
# Compiled at: 2008-03-23 23:35:14
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets import common

class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/sections.pt')
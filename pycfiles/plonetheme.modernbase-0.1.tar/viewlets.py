# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/minimalist/browser/viewlets.py
# Compiled at: 2008-09-20 00:50:42
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets import common

class SiteActionsViewlet(common.SiteActionsViewlet):
    """siteaction customizado"""
    __module__ = __name__
    render = ViewPageTemplateFile('templates/site_actions.pt')
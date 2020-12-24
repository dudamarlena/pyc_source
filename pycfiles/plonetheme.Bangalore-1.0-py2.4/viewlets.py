# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/Bangalore/browser/viewlets.py
# Compiled at: 2010-02-05 09:52:09
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase, SiteActionsViewlet

class SiteActionsViewletFooter(SiteActionsViewlet):
    __module__ = __name__
    index = ViewPageTemplateFile('templates/site_actions_footer.pt')
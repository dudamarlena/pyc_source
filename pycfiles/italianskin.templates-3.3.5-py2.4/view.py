# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/italianskin/templates/browser/plone/app/contentmenu/view.py
# Compiled at: 2010-09-08 03:48:21
from plone.app.contentmenu.view import ContentMenuProvider as ContentMenuProviderOriginal
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class ContentMenuProvider(ContentMenuProviderOriginal):
    """Content menu provider for the "view" tab: displays the menu
    """
    __module__ = __name__
    render = ZopeTwoPageTemplateFile('contentmenu.pt')
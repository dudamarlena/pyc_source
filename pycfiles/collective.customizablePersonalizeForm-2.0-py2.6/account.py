# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/customizablePersonalizeForm/browser/account.py
# Compiled at: 2011-09-08 04:35:46
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from plone.app.users.browser.interfaces import IAccountPanelForm, IAccountPanelView
from plone.app.users.browser.account import AccountPanelView

class ExtendedAccountPanelView(AccountPanelView):
    template = ViewPageTemplateFile('templates/extended-account-panel-bare.pt')
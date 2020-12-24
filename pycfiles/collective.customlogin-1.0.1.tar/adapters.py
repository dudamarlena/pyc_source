# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/customizablePersonalizeForm/adapters/adapters.py
# Compiled at: 2011-09-08 04:35:46
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from collective.customizablePersonalizeForm.adapters.interfaces import IExtendedUserDataPanel
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from zope.site.hooks import getSite
from zope.component import getAdapters
from Acquisition import aq_inner

class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    real_context = None

    def __init__(self, context):
        self.real_context = context
        providers = [ x for x in getAdapters((context, context.REQUEST), IExtendedUserDataPanel) ]
        for provider in providers:
            for prop in provider[1].getProperties():
                if isinstance(prop, dict):
                    setattr(self.__class__, prop['name'], property(prop['getter'], prop['setter']))
                else:
                    setattr(self.__class__, prop, self.make_prop(prop))

        super(EnhancedUserDataPanelAdapter, self).__init__(context)

    def make_prop(self, name):

        def getter(self):
            return self.context.getProperty(name, '')

        def setter(self, value):
            return self.context.setMemberProperties({name: value})

        return property(getter, setter)
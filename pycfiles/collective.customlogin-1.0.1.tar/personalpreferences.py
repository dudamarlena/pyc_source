# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/customizablePersonalizeForm/browser/personalpreferences.py
# Compiled at: 2011-09-08 04:35:46
from plone.app.users.browser.personalpreferences import UserDataPanel
from OFS.Image import Image
from collective.customizablePersonalizeForm.adapters.interfaces import IExtendedUserDataWidgets
from zope.component import getAdapters

class ExtendedUserDataPanel(UserDataPanel):

    def isImage(self, widget):
        return isinstance(widget._data, Image)

    def __init__(self, context, request):
        """ Load the UserDataSchema at view time.

        (Because doing getUtility for IUserDataSchemaProvider fails at startup
        time.)

        """
        super(ExtendedUserDataPanel, self).__init__(context, request)
        providers = [ x for x in getAdapters((context, request), IExtendedUserDataWidgets) ]
        for provider in providers:
            for association in provider[1].getWidgets():
                self.form_fields[association['field']].custom_widget = association['factory']
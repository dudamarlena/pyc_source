# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/qPloneDropDownMenu/browser/views.py
# Compiled at: 2010-07-19 08:14:01
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

class PrefsDropDownView(BrowserView):
    """DropDown configlet.
    
    """
    template = ViewPageTemplateFile('templates/prefs_dropdownmenu_edit_form.pt')

    def __init__(self, context, request):
        super(PrefsDropDownView, self).__init__(context, request)
        self.portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        self.portal = self.portal_state.portal()
        self.pp = getToolByName(self.portal, 'portal_properties')
        self.dp = getattr(self.pp, 'dropdownmenu_properties', None)
        return

    def menu(self):
        menu = ''
        if self.dp is not None:
            menu = self.dp.getProperty('menu', '')
        return menu

    def __call__(self):
        save = self.request.get('save', None)
        update = self.request.get('regenerate_menu', None)
        status = IStatusMessage(self.request)
        if save is not None:
            if self.dp is None:
                status.addStatusMessage('Dropdown menu property sheet does not exist.\n                Please, firstly regenerate menu before editing it.')
                return self.template()
            menu = self.menu()
            if not menu:
                status.addStatusMessage('Menu field does not exist in dropdown menu property sheet.\n                Please, firstly regenerate menu before editing it.')
                return self.template()
            self.dp.manage_changeProperties(menu=self.request.get('menu'))
            status.addStatusMessage('DropDown Menu updated.')
            return self.template()
        else:
            if update is not None:
                getToolByName(self.portal, 'portal_dropdownmenu').regenerateMenu()
                status.addStatusMessage('DropDown Menu regenerated.')
            return self.template()
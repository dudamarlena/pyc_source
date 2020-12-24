# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/republisher/controlpanel.py
# Compiled at: 2010-09-29 12:35:38
from plone.app.registry.browser import controlpanel
from Products.republisher.interfaces import IRepublisherSettings
from Products.CMFPlone import PloneMessageFactory as _p
from z3c.form import form, button
from plone.app.form.validators import null_validator
from Products.statusmessages.interfaces import IStatusMessage
from uploadr import Uploadr
from plone.registry.interfaces import IRegistry
from Products.republisher.interfaces import IRepublisherTokenKeeper, IRepublisherSettings
from zope.component import getUtility
from zope.component import queryUtility

class RepublisherSettingsEditForm(controlpanel.RegistryEditForm):
    __module__ = __name__
    schema = IRepublisherSettings
    label = 'Republisher'
    description = 'Settings for the republisher product authentication on the social networks'

    def updateFields(self):
        super(RepublisherSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(RepublisherSettingsEditForm, self).updateWidgets()

    @button.buttonAndHandler(_p('Save'), name='save')
    def handleSave(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_p('Changes saved'), 'info')
        self.request.response.redirect('%s/%s' % (self.context.absolute_url(), self.control_panel_view))

    @button.buttonAndHandler(_p('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_p('Edit cancelled'), 'info')
        self.request.response.redirect('%s/%s' % (self.context.absolute_url(), self.control_panel_view))

    @button.buttonAndHandler('Generate Auth URL', name='auth')
    def handle_auth_action(self, action):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IRepublisherSettings)
        tokenkeeper = registry.forInterface(IRepublisherTokenKeeper)
        flickr = Uploadr()
        flickr.setAPIKeyAndSecret(settings.api_key, settings.api_secret)
        frob = flickr.getFrob()
        tokenkeeper.flickr_frob = unicode(str(frob))
        url = flickr.getAuthKey()
        self.status = 'To Authorise the republisher please visit: ' + url + ' and then press check authentication.'

    @button.buttonAndHandler('Check authorization', name='check')
    def handle_check_action(self, action):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IRepublisherSettings)
        tokenkeeper = registry.forInterface(IRepublisherTokenKeeper)
        flickr = Uploadr(frob=tokenkeeper.flickr_frob)
        flickr.setAPIKeyAndSecret(settings.api_key, settings.api_secret)
        if flickr.getToken():
            tokenkeeper.flickr_token = unicode(flickr.token)
            self.status = 'You have authorized the app sucessfully'
        else:
            url = flickr.getAuthKey()
            self.status = 'You have not yet authorized the app. Please visit ' + url + 'and then try again.'


class RepublisherSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    __module__ = __name__
    form = RepublisherSettingsEditForm
# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/republisher/republisherprefs.py
# Compiled at: 2010-10-08 12:47:05
from zope import schema
from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface, implements
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator
from plone.protect import CheckAuthenticator
from zope.event import notify
from plone.app.controlpanel.events import ConfigurationChangedEvent
from Products.CMFPlone import PloneMessageFactory as _p

class IRepublisherPrefsForm(Interface):
    """ The view for Republisher prefs form. """
    __module__ = __name__
    allowed_types = schema.Tuple(title='Portal types', description='Portal types to republish', missing_value=tuple(), value_type=schema.Choice(vocabulary='plone.app.vocabularies.UserFriendlyTypes'), required=False)
    api_key = schema.TextLine(title='Republisher Flickr app key', default='None')
    api_secret = schema.TextLine(title='Republisher Flickr app secret', default='None')
    republisher_toggle = schema.Bool(title='Republisher on', default=True)


class RepublisherControlPanelAdapter(SchemaAdapterBase):
    """ Control Panel adapter """
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(IRepublisherPrefsForm)

    def __init__(self, context, other):
        super(RepublisherControlPanelAdapter, self).__init__(context)
        self.context = context


class RepublisherPrefsForm(ControlPanelForm):
    """ The view class for the lead image preferences form. """
    __module__ = __name__
    implements(IRepublisherPrefsForm)
    form_fields = form.FormFields(IRepublisherPrefsForm)
    schema = IRepublisherPrefsForm
    label = 'Republisher Settings Form'
    description = 'Select properties for the Republisher'
    form_name = 'Republisher Settings'

    @form.action(_p('label_save', default='Save'), name='save')
    def handle_edit_action(self, action, data):
        CheckAuthenticator(self.request)
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            self.status = _p('Changes saved.')
            notify(ConfigurationChangedEvent(self, data))
            self._on_save(data)
        else:
            self.status = _p('No changes made.')

    @form.action(_p('label_cancel', default='Cancel'), validator=null_validator, name='cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_p('Changes canceled.'), type='info')
        url = getMultiAdapter((self.context, self.request), name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''

    @form.action('Authenticate FLICKR', name='authFlickr', validator=null_validator)
    def handle_scales_action(self, action, data):
        CheckAuthenticator(self.request)
        self.status = 'You are now authenticated.'
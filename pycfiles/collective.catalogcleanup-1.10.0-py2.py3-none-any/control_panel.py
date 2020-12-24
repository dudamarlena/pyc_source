# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/castle/control_panel.py
# Compiled at: 2010-08-09 05:35:03
from StringIO import StringIO
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.schema import TextLine
from zope.schema import Bool
from zope.formlib import form
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from plone.fieldsets.form import FieldsetsEditForm
from plone.app.controlpanel.interfaces import IPloneControlPanelForm
from Products.statusmessages.interfaces import IStatusMessage
from rwproperty import getproperty
from rwproperty import setproperty

class ICAS4PASPluginSchema(Interface):
    __module__ = __name__
    login_url = TextLine(title=_('CAS Log in URL'), description=_(''), required=True)
    logout_url = TextLine(title=_('CAS Log out URL'), description=_(''), required=True)
    validate_url = TextLine(title=_('CAS Validate URL'), description=_(''), required=True)
    session_var = TextLine(title=_('Session Variable'), description=_(''), required=True)
    use_ACTUAL_URL = Bool(title=_('Use Actual URL'), description=_(''), required=True)


class CASSettingsAdapter(object):
    __module__ = __name__
    implements(ICAS4PASPluginSchema)
    adapts(IPloneSiteRoot)

    def __init__(self, context):
        url_tool = getToolByName(context, 'portal_url')
        portal = url_tool.getPortalObject()
        acl_users = portal.acl_users
        cas_auth_helpers = acl_users.objectValues(['CAS Auth Helper'])
        if not cas_auth_helpers:
            cas = acl_users.manage_addProduct['CAS4PAS']
            cas.addCASAuthHelper('cas', 'CAS Auth Helper')
            cas.login_url = 'https://your.cas.server:port/cas/login'
            cas.logout_url = 'https://your.cas.server:port/cas/logout'
            cas.validate_url = 'https://your.cas.server:port/cas/validate'
            cas.session_var = '__ac'
            cas.use_ACTUAL_URL = True
            out = StringIO()
            activatePluginInterfaces(portal, 'cas', out)
            msg = 'Created CAS plugin. %s' % out.getvalue()
            IStatusMessage(context.request).addStatusMessage(msg, 'info')
        else:
            cas = cas_auth_helpers[0]
        self.cas = cas

    @getproperty
    def login_url(self):
        return self.cas.login_url

    @setproperty
    def login_url(self, login_url):
        self.cas.login_url = login_url

    @getproperty
    def logout_url(self):
        return self.cas.logout_url

    @setproperty
    def logout_url(self, logout_url):
        self.cas.logout_url = logout_url

    @getproperty
    def validate_url(self):
        return self.cas.validate_url

    @setproperty
    def validate_url(self, validate_url):
        self.cas.validate_url = validate_url

    @getproperty
    def session_var(self):
        return self.cas.session_var

    @setproperty
    def session_var(self, session_var):
        self.cas.session_var = session_var

    @getproperty
    def use_ACTUAL_URL(self):
        return self.cas.use_ACTUAL_URL

    @setproperty
    def use_ACTUAL_URL(self, use_ACTUAL_URL):
        self.cas.use_ACTUAL_URL = use_ACTUAL_URL


class CASControlPanel(FieldsetsEditForm):
    __module__ = __name__
    implements(IPloneControlPanelForm)
    form_fields = form.FormFields(ICAS4PASPluginSchema)
    label = _('CAS settings')
    description = _('CAS settings for this site.')
    form_name = _('CAS settings')

    @form.action(_('Save'))
    def save(self, action, data):
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            self.status = _('Changes saved.')
        else:
            self.status = _('No changes made.')

    @form.action(_('Cancel'))
    def cancel(self, action, data):
        pass
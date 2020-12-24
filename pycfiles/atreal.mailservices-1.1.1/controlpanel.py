# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/romain/dev/buildouts/xnet4.1/src/atreal.mailservices/atreal/mailservices/browser/controlpanel.py
# Compiled at: 2011-11-25 03:57:49
from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import SourceText, TextLine, Bool
from zope.formlib import form
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from atreal.mailservices import MailServicesMessageFactory as _
from plone.app.controlpanel.form import ControlPanelForm

class IMailServicesSchema(Interface):
    mailservices_admin_bcc = Bool(title=_('label_admin_bcc', default='Would you like the Administrator of this Plone Site receive all mails?'), description=_('help_admin_bcc', default='This will mail each mail sended with MailServices to Portal Administrator.'), default=True, required=True)
    mailservices_additionals = Bool(title=_('label_mailservices_additionals', default='Would you like Users can send mail to additionals recipients?'), description=_('help_mailservices_additionals', default='This will add additionals fields to MailServices form to add mail address manually.'), default=False, required=True)
    mailservices_subject = TextLine(title=_('label_mailservices_subject', default='Default Subject'), description=_('help_mailservices_subject', default='Default subject. You can use ${portal_title}, ${object_title}, ${object_url} to replace with values.'), required=False)
    mailservices_body = SourceText(title=_('label_mailservices_body', default='Message template'), description=_('help_mailservices_body', default='Default body message. You can use ${portal_title}, ${object_title}, ${object_url} to replace with values.'), required=False)


class MailServicesControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IMailServicesSchema)

    def __init__(self, context):
        super(MailServicesControlPanelAdapter, self).__init__(context)

    mailservices_admin_bcc = ProxyFieldProperty(IMailServicesSchema['mailservices_admin_bcc'])
    mailservices_additionals = ProxyFieldProperty(IMailServicesSchema['mailservices_additionals'])
    mailservices_subject = ProxyFieldProperty(IMailServicesSchema['mailservices_subject'])
    mailservices_body = ProxyFieldProperty(IMailServicesSchema['mailservices_body'])


class MailServicesControlPanel(ControlPanelForm):
    form_fields = form.FormFields(IMailServicesSchema)
    label = _('MailServices settings')
    description = _('MailServices settings for this site.')
    form_name = _('MailServices settings')
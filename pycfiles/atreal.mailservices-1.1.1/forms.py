# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/romain/dev/buildouts/xnet4.1/src/atreal.mailservices/atreal/mailservices/browser/forms.py
# Compiled at: 2011-11-25 03:57:49
"""
"""
from zope.interface import Interface
from zope import schema
from zope.formlib import form
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser.decode import setPageEncoding
from Products.CMFPlone.utils import safe_unicode
from plone.fieldsets.fieldsets import FormFieldsets
from plone.fieldsets.form import FieldsetsInputForm
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from atreal.mailservices.browser.overrides import processInputs
from atreal.mailservices.browser.views import MailServicesView
from atreal.mailservices import MailServicesMessageFactory as _
from email import message_from_string
from email.Header import Header
try:
    import plone.app.upgrade
    PLONE_VERSION = 4
except ImportError:
    PLONE_VERSION = 3

class IMailServicesGroupsUsersSchema(Interface):
    """
    """
    pass


class IMailServicesAdditionalsSchema(Interface):
    """
    """
    pass


class IMailServicesMailSchema(Interface):
    """
    """
    subject = schema.TextLine(title=_('label_subject', default='Subject'), description=_('help_subject', default='The subject of your email.'), required=True)
    body = schema.SourceText(title=_('label_message', default='Body'), description=_('help_message', default='The body of your email.'), required=True)


class IMailServicesFormSchema(IMailServicesGroupsUsersSchema, IMailServicesAdditionalsSchema, IMailServicesMailSchema):
    """ Define the fields of the form
    """
    pass


ms_groupsusersset = FormFieldsets(IMailServicesGroupsUsersSchema)
ms_groupsusersset.id = 'groupsusers'
ms_groupsusersset.label = _('Groups & Users')
ms_additionalsset = FormFieldsets(IMailServicesAdditionalsSchema)
ms_additionalsset.id = 'additionals'
ms_additionalsset.label = _('Additionals mails')
ms_mailset = FormFieldsets(IMailServicesMailSchema)
ms_mailset.id = 'mail'
ms_mailset.label = _('Write the mail')

class MailServicesForm(MailServicesView, FieldsetsInputForm):
    """
    """
    form_name = _('Mail Services')
    label = _('Mail Services')
    description = _('description_mailservices', default='Fill the tabs and valid the form to send an email.')
    template = ZopeTwoPageTemplateFile('mailservices.pt')

    @property
    def form_fields(self):
        """
        """
        form_fields = None
        if self.mailservices_additionals():
            form_fields = FormFieldsets(ms_groupsusersset, ms_additionalsset, ms_mailset)
        else:
            form_fields = FormFieldsets(ms_groupsusersset, ms_mailset)
        form_fields['body'].field.default = self.getTextReplaced('body')
        form_fields['subject'].field.default = self.getTextReplaced('subject')
        return form_fields

    def getTextReplaced(self, field=None):
        """
        """
        template = getattr(self._options, 'mailservices_' + field)
        if template is None:
            return ''
        else:
            for field in self.getFieldsReplaceables():
                template = template.replace('${' + field + '}', getattr(self, field, None))

            return template

    def getFieldsReplaceables(self):
        """
        """
        return [
         'portal_title', 'object_title', 'object_url']

    @property
    def portal_title(self):
        """
        """
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        return safe_unicode(portal_state.portal_title())

    @property
    def object_title(self):
        """
        """
        return safe_unicode(self.context.title_or_id())

    @property
    def object_url(self):
        """
        """
        return self.context.absolute_url()

    def update(self):
        processInputs(self.request)
        setPageEncoding(self.request)
        super(MailServicesForm, self).update()

    def getMailForUserById(self, user_id=''):
        """
        """
        user = self.acl_users.getUserById(user_id)
        if user is None:
            return
        else:
            return user.getProperty('email', None)

    def getMailsForUsersByIds(self, user_ids=[]):
        """
        """
        return set([ self.getMailForUserById(user) for user in user_ids if self.getMailForUserById(user) is not None
                   ])

    def getMailsForGroupById(self, group_id=''):
        """
        """
        group = self.acl_users.getGroupById(group_id)
        if group is None:
            return set([])
        else:
            return self.getMailsForUsersByIds(group.getAllGroupMemberIds())

    def getMailsForGroupsByIds(self, group_ids=[]):
        """
        """
        result = set()
        for group_id in group_ids:
            result |= self.getMailsForGroupById(group_id)

        return result

    def getAllMails(self):
        """
        """
        self.acl_users = getToolByName(self.context, 'acl_users')
        mails = {'to': set([]), 
           'cc': set([]), 
           'bcc': set([])}
        for recipient in self.recipients():
            id = recipient['id']
            if self.request.form.get('groups', None) is not None:
                mails[id] |= self.getMailsForGroupsByIds([ group.id for group in self.request.form['groups'] if getattr(group, 'recipient_' + id, False) == 'True'
                                                         ])
            if self.request.form.get('users', None) is not None:
                mails[id] |= self.getMailsForUsersByIds([ user.id for user in self.request.form['users'] if getattr(user, 'recipient_' + id, False) == 'True'
                                                        ])
            additionals = self.request.form.get('email_' + id, None)
            if additionals is not None:
                mails[id] |= set([ additional for additional in additionals.replace(' ', '').split(';') if len(additional)
                                 ])

        site_properties = getToolByName(self, 'portal_properties').site_properties
        mails['admin'] = site_properties.email_from_address
        if getattr(self._options, 'mailservices_admin_bcc', True) is True:
            mails['cc'] |= set([mails['admin']])
        mails['from'] = self.usermail_from_address()
        mails['to'] |= set([mails['from']])
        mails['to'] = list(mails['to'])
        mails['cc'] = list(mails['cc'])
        mails['bcc'] = list(mails['bcc'])
        return mails

    def sendMail(self):
        """ Send an email to all emails from emailsList,
            with the info passsed in info, via the host object.
            Return a dict with the (email,exception) of problematics
            emails, or empty if no errors occured.
        """
        host = getToolByName(self, 'MailHost')
        mails = self.getAllMails()
        plone_utils = getToolByName(self.context, 'plone_utils')
        encoding = plone_utils.getSiteEncoding()
        result = {}
        try:
            if PLONE_VERSION >= 4:
                message_body = self.request.form['form.body']
                my_message = message_from_string(message_body.encode(encoding))
                my_message.set_charset(encoding)
                if mails['cc']:
                    my_message['CC'] = Header((',').join(mails['cc']))
                if mails['bcc']:
                    my_message['BCC'] = Header((',').join(mails['bcc']))
                if mails['from']:
                    my_message['From'] = Header(mails['from'])
                host.send(my_message, mto=mails['to'], mfrom=mails['admin'], subject=self.request.form['form.subject'], charset=encoding, msg_type='text/plain')
            else:
                host.secureSend(self.request.form['form.body'], mails['to'], mails['admin'], mbcc=mails['bcc'], subject=self.request.form['form.subject'], mcc=mails['cc'], subtype='plain', charset=encoding, debug=False, From=mails['from'])
        except Exception, e:
            result['email'] = e.__class__.__name__ + ' : ' + str(e)

        return result

    @form.action(_('Send'), name='send')
    def action_send(self, action, data):
        """
        """
        result = self.sendMail()
        res = result.get('email', None)
        if res is not None:
            self.form_reset = False
            self.status = _('Mail not sent.') + res
            return
        else:
            type = 'info'
            message = _('Mail sent.')
            props = getToolByName(self.context, 'portal_properties')
            stp = props.site_properties
            view_action_types = stp.getProperty('typesUseViewActionInListings', ())
            suffix = ''
            if self.context.portal_type in view_action_types:
                suffix = '/view'
            self.request.response.redirect(self.context.absolute_url() + suffix)
            IStatusMessage(self.request).addStatusMessage(message, type=type)
            return ''
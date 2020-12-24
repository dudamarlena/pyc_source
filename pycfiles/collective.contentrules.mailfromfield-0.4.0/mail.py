# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/collective/contentrules/mailadapter/actions/mail.py
# Compiled at: 2009-06-10 07:32:58
from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from zope.component import adapts
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface, implements
from zope.formlib import form
from zope import schema
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import safe_unicode
from collective.contentrules.mailadapter.interfaces import IRecipientsResolver

class IMailAction(Interface):
    """Definition of the configuration available for a mail action
    """
    __module__ = __name__
    subject = schema.TextLine(title=_('Subject'), description=_('Subject of the message'), required=True)
    source = schema.TextLine(title=_('Email source'), description=_('The email address that sends the email. If no email is provided here, it will use the portal from address.'), required=False)
    message = schema.Text(title=_('Message'), description=_('Type in here the message that you want to mail. Some defined content can be replaced: ${title} will be replaced by the title of the item. ${url} will be replaced by the URL of the item.'), required=True)


class MailAction(SimpleItem):
    """
    The implementation of the action defined before
    """
    __module__ = __name__
    implements(IMailAction, IRuleElementData)
    subject = ''
    source = ''
    message = ''
    element = 'collective.actions.Mail'

    @property
    def summary(self):
        return _('Email report sent')


class MailActionExecutor(object):
    """The executor for this action.
    """
    __module__ = __name__
    implements(IExecutable)
    adapts(Interface, IMailAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        recipient_resolver = IRecipientsResolver(self.event.object)
        if recipient_resolver:
            recipients = recipient_resolver.recipients()
        mailhost = aq_inner(self.context).MailHost
        if not mailhost:
            raise ComponentLookupError, 'You must have a Mailhost utility to execute this action'
        source = self.element.source
        urltool = getToolByName(aq_inner(self.context), 'portal_url')
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')
        if not source:
            from_address = portal.getProperty('email_from_address')
            if not from_address:
                raise ValueError, 'You must provide a source address for this action or enter an email in the portal properties'
            from_name = portal.getProperty('email_from_name')
            source = '%s <%s>' % (from_name, from_address)
        obj = self.event.object
        event_title = safe_unicode(obj.Title())
        event_url = obj.absolute_url()
        message = self.element.message.replace('${url}', event_url)
        message = message.replace('${title}', event_title)
        subject = self.element.subject.replace('${url}', event_url)
        subject = subject.replace('${title}', event_title)
        for email_recipient in recipients:
            mailhost.secureSend(message, email_recipient, source, subject=subject, subtype='plain', charset=email_charset, debug=False, From=source)

        return True


class MailAddForm(AddForm):
    """
    An add form for the mail action
    """
    __module__ = __name__
    form_fields = form.FormFields(IMailAction)
    label = _('Add Mail Action')
    description = _('A mail action can mail different recipient.')
    form_name = _('Configure element')

    def create(self, data):
        a = MailAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class MailEditForm(EditForm):
    """
    An edit form for the mail action
    """
    __module__ = __name__
    form_fields = form.FormFields(IMailAction)
    label = _('Edit Mail Action')
    description = _('A mail action can mail different recipient.')
    form_name = _('Configure element')
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/patch/plone3mail/HotfixRegistrationTool.py
# Compiled at: 2010-02-22 09:06:15
"""
HotfixRegistrationTool.py

Created by Manabu Terada on 2009-11-21.
Copyright (c) 2009 CMScom. All rights reserved.
"""
from email import message_from_string, MIMEText
from smtplib import SMTPRecipientsRefused
from logging import getLogger
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from AccessControl import Unauthorized
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from Products.CMFPlone.RegistrationTool import _checkEmail
from Products.CMFPlone.RegistrationTool import RegistrationTool
logger = getLogger(__name__)
info = logger.info
try:
    from Products.CMFPlone.RegistrationTool import get_member_by_login_name
    HAS_PLONE4 = True
except ImportError:
    HAS_PLONE4 = False

_ = MessageFactory('plone')

def _mailPassword(self, forgotten_userid, REQUEST):
    """ Wrapper around mailPassword """
    membership = getToolByName(self, 'portal_membership')
    if not membership.checkPermission('Mail forgotten password', self):
        raise Unauthorized(_('Mailing forgotten passwords has been disabled.'))
    utils = getToolByName(self, 'plone_utils')
    props = getToolByName(self, 'portal_properties').site_properties
    emaillogin = props.getProperty('use_email_as_login', False)
    if emaillogin:
        if HAS_PLONE4:
            member = get_member_by_login_name(self, forgotten_userid)
        else:
            member = membership.getMemberById(forgotten_userid)
        if member is None:
            raise ValueError(_('The username you entered could not be found.'))
        if emaillogin:
            forgotten_userid = member.getId()
        email = member.getProperty('email')
        raise email or ValueError(_('That user does not have an email address.'))
    elif not utils.validateSingleEmailAddress(email):
        raise ValueError(_('The email address did not validate.'))
    (check, msg) = _checkEmail(email)
    if not check:
        raise ValueError(msg)
    reset_tool = getToolByName(self, 'portal_password_reset')
    reset = reset_tool.requestReset(forgotten_userid)
    encoding = getUtility(ISiteRoot).getProperty('email_charset', 'utf-8')
    mail_text = self.mail_password_template(self, REQUEST, member=member, reset=reset, password=member.getPassword(), charset=encoding)
    if isinstance(mail_text, unicode):
        mail_text = mail_text.encode(encoding, 'replace')
    message_obj = message_from_string(mail_text)
    subject = message_obj['Subject']
    m_to = message_obj['To']
    m_from = message_obj['From']
    host = getToolByName(self, 'MailHost')
    try:
        host.secureSend(message_obj, m_to, m_from, subject=subject, charset=encoding)
        return self.mail_password_response(self, REQUEST)
    except SMTPRecipientsRefused:
        raise SMTPRecipientsRefused(_('Recipient address rejected by server.'))

    return


def _registeredNotify(self, new_member_id):
    """ Wrapper around registeredNotify """
    membership = getToolByName(self, 'portal_membership')
    utils = getToolByName(self, 'plone_utils')
    member = membership.getMemberById(new_member_id)
    if member and member.getProperty('email'):
        if not utils.validateSingleEmailAddress(member.getProperty('email')):
            raise ValueError(_('The email address did not validate.'))
    email = member.getProperty('email')
    try:
        checkEmailAddress(email)
    except EmailAddressInvalid:
        raise ValueError(_('The email address did not validate.'))

    pwrt = getToolByName(self, 'portal_password_reset')
    reset = pwrt.requestReset(new_member_id)
    mail_text = self.registered_notify_template(self, self.REQUEST, member=member, reset=reset, email=email)
    encoding = getUtility(ISiteRoot).getProperty('email_charset', 'utf-8')
    if isinstance(mail_text, unicode):
        mail_text = mail_text.encode(encoding, 'replace')
    message_obj = message_from_string(mail_text)
    subject = message_obj['Subject']
    m_to = message_obj['To']
    m_from = message_obj['From']
    host = getToolByName(self, 'MailHost')
    host.secureSend(message_obj, m_to, m_from, subject=subject, charset=encoding)
    return self.mail_password_response(self, self.REQUEST)


RegistrationTool.mailPassword = _mailPassword
RegistrationTool.registeredNotify = _registeredNotify
info('patched %s', str(RegistrationTool.mailPassword))
info('patched %s', str(RegistrationTool.registeredNotify))
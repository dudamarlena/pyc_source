# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/patch/plone3mail/HotfixSecureMailHost.py
# Compiled at: 2010-02-22 09:45:27
__doc__ = '\nHotfixSecureMailHost.py\n\nCreated by Manabu Terada on 2009-05-24.\nCopyright (c) 2009 CMScom. All rights reserved.\n'
from Products.SecureMailHost.config import BAD_HEADERS
from copy import deepcopy
import email.Message, email.Header, email.MIMEText, email
from email.Utils import getaddresses
from email.Utils import formataddr
from AccessControl.Permissions import use_mailhost_services
from Globals import Persistent, DTMLFile, InitializeClass
from Products.CMFCore.utils import getToolByName
from Products.MailHost.MailHost import MailHostError
from Products.SecureMailHost.SecureMailHost import encodeHeaderAddress
from Products.SecureMailHost.SecureMailHost import SecureMailHost
from logging import getLogger
logger = getLogger(__name__)
info = logger.info

def _to_unicode_to_str(s, old_chr, new_chr):
    if s is None:
        return s
    if isinstance(s, unicode):
        return s.encode(new_chr, 'replace')
    else:
        return s.decode(old_chr).encode(new_chr, 'replace')
    return


def _secureSend(self, message, mto, mfrom, subject='[No Subject]', mcc=None, mbcc=None, subtype='plain', charset='us-ascii', debug=False, **kwargs):
    """A more secure way to send a message

    message:
        The plain message text without any headers or an
        email.Message.Message based instance
    mto:
        To: field (string or list)
    mfrom:
        From: field
    subject:
        Message subject (default: [No Subject])
    mcc:
        Cc: (carbon copy) field (string or list)
    mbcc:
        Bcc: (blind carbon copy) field (string or list)
    subtype:
        Content subtype of the email e.g. 'plain' for text/plain (ignored
        if message is a email.Message.Message instance)
    charset:
        Charset used for the email, subject and email addresses
    kwargs:
        Additional headers
    """
    portal_prop = getToolByName(self, 'portal_properties')
    site_charset = portal_prop.site_properties.getProperty('default_charset', 'utf-8')
    mto = self.emailListToString(_to_unicode_to_str(mto, site_charset, charset))
    mcc = self.emailListToString(_to_unicode_to_str(mcc, site_charset, charset))
    mbcc = self.emailListToString(_to_unicode_to_str(mbcc, site_charset, charset))
    for addr in (mto, mcc, mbcc):
        if addr:
            result = self.validateEmailAddresses(addr)
            if not result:
                raise MailHostError, 'Invalid email address: %s' % addr

    result = self.validateSingleEmailAddress(mfrom)
    if not result:
        raise MailHostError, 'Invalid email address: %s' % mfrom
    if isinstance(message, email.Message.Message):
        msg = deepcopy(message)
    else:
        if isinstance(message, unicode):
            message = message.encode(charset, 'replace')
        else:
            message = message.decode(site_charset).encode(charset, 'replace')
        msg = email.MIMEText.MIMEText(message, subtype, charset)
    mfrom = encodeHeaderAddress(mfrom, charset)
    mto = encodeHeaderAddress(mto, charset)
    mcc = encodeHeaderAddress(mcc, charset)
    mbcc = encodeHeaderAddress(mbcc, charset)
    subject = _to_unicode_to_str(subject, site_charset, charset)
    self.setHeaderOf(msg, skipEmpty=True, From=mfrom, To=mto, Subject=str(email.Header.Header(subject, charset)), Cc=mcc, Bcc=mbcc)
    for bad in BAD_HEADERS:
        if bad in kwargs:
            raise MailHostError, 'Header %s is forbidden' % bad

    self.setHeaderOf(msg, **kwargs)
    to = msg.get_all('to', [])
    cc = msg.get_all('cc', [])
    bcc = msg.get_all('bcc', [])
    recipient_list = getaddresses(to + cc + bcc)
    all_recipients = [ formataddr(pair) for pair in recipient_list ]
    return self._send(mfrom, all_recipients, msg, debug=debug)


SecureMailHost.secureSend = _secureSend
info('patched %s', str(SecureMailHost.secureSend))
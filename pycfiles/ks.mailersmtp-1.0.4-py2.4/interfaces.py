# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/mailersmtp/interfaces.py
# Compiled at: 2008-12-23 09:44:03
"""Interfaces for the Zope 3 based mailersmtp package

$Id: interfaces.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from zope.interface import Interface
from zope.schema import Choice, Bool, ASCIILine, Text, TextLine
from ks.mailer.interfaces import IMailer
from ks.mailersmtp import _

class IMailerSMTPAnnotable(Interface):
    __module__ = __name__


mailersmtpannotationkey = 'ks.mailersmtp.mailersmtp.MailerSMTP'

class IMailerSMTP(IMailer):
    __module__ = __name__
    use_container = Bool(title=_('Use container'), default=False)
    use_alternative = Bool(title=_('Use alternative'), default=False)
    mime = ASCIILine(title=_('Mime type'), default='text/plain')
    filename = ASCIILine(title=_('File name'), default='body')
    Subject = TextLine(title=_('"Subject:" template'))
    mail_header = Text(title=_('Header template'), required=False, default='', missing_value='')
    mail_footer = Text(title=_('Footer template'), required=False, default='', missing_value='')
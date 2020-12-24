# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/mailersmtp/mailerannotation.py
# Compiled at: 2008-12-23 09:44:03
"""IMailerSMTPAnnotation to IMailerSMTP adapter for the Zope 3 based mailersmtp package

$Id: mailerannotation.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from interfaces import mailersmtpannotationkey
from zope.annotation.interfaces import IAnnotations
from mailersmtp import MailerSMTP

def MailerAnnotableAdapter(context):
    annotations = IAnnotations(context)
    if annotations.has_key(mailersmtpannotationkey):
        return annotations[mailersmtpannotationkey]
    else:
        annotation = annotations[mailersmtpannotationkey] = MailerSMTP()
    return annotation
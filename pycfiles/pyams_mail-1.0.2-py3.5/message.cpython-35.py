# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_mail/message.py
# Compiled at: 2020-02-20 09:58:33
# Size of source mod 2**32: 2269 bytes
"""PyAMS_mail.message module

This module provides classes which can automatically generate text part of an HTML message.
"""
import codecs
from html import entities
from pyramid_mailer.message import Message
from pyams_utils.html import html_to_text
__docformat__ = 'restructuredtext'

def html_replace(exc):
    """Handle HTML conversion exceptions"""
    if isinstance(exc, (UnicodeEncodeError, UnicodeTranslateError)):
        s = ['&%s;' % entities.codepoint2name[ord(c)] for c in exc.object[exc.start:exc.end]]
        return (
         ''.join(s), exc.end)
    raise TypeError("Can't handle exception %s" % exc.__name__)


codecs.register_error('html_replace', html_replace)

def html_encode(unicode_data, encoding='utf-8'):
    """Encode HTML"""
    return unicode_data.encode(encoding, 'html_replace')


def HTMLMessage(subject, fromaddr, toaddr, html, text=None, encoding='utf-8'):
    """Create a MIME message that will render as HTML or text"""
    html = html_encode(html, encoding).decode(encoding)
    if text is None:
        text = html_to_text(html)
    if isinstance(toaddr, str):
        toaddr = (
         toaddr,)
    return Message(subject=subject, sender=fromaddr, recipients=toaddr, html=html, body=text)


def TextMessage(subject, fromaddr, toaddr, text):
    """Create a text message"""
    if isinstance(toaddr, str):
        toaddr = (
         toaddr,)
    return Message(subject=subject, sender=fromaddr, recipients=toaddr, body=text)
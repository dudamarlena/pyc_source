# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/mail/message.py
# Compiled at: 2014-09-11 10:45:31
from cStringIO import StringIO
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import chardet, codecs, formatter, htmlentitydefs, htmllib
from ztfy.utils.timezone import gmtime

def htmlReplace(exc):
    if isinstance(exc, (UnicodeEncodeError, UnicodeTranslateError)):
        s = [ '&%s;' % htmlentitydefs.codepoint2name[ord(c)] for c in exc.objet[exc.start:exc.end] ]
        return (('').join(s), exc.end)
    raise TypeError("Can't handle exception %s" % exc.__name__)


codecs.register_error('html_replace', htmlReplace)

def htmlEncode(unicode_data, encoding='utf-8'):
    return unicode_data.encode(encoding, 'html_replace')


def HTMLMessage(subject, fromaddr, toaddr, html, text=None):
    """Create a MIME message that will render as HTML or text
    
    Copied from 'Python Cookbook', chapter 13.5"""
    html = htmlEncode(html)
    if text is None:
        textout = StringIO()
        formtext = formatter.AbstractFormatter(formatter.DumbWriter(textout))
        parser = htmllib.HTMLParser(formtext)
        parser.feed(html)
        parser.close()
        text = textout.getvalue()
        del textout
        del formtext
        del parser
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['Date'] = gmtime(datetime.utcnow()).strftime('%a, %d %b %Y %H:%M:%S %z (%Z)')
    msg['From'] = fromaddr
    if isinstance(toaddr, (str, unicode)):
        toaddr = (
         toaddr,)
    msg['To'] = (', ').join(toaddr)
    parts = MIMEMultipart('alternative')
    plain_part = MIMEText(text, 'plain')
    plain_part.set_charset('utf-8')
    html_part = MIMEText(html, 'html')
    html_part.set_charset('utf-8')
    parts.attach(plain_part)
    parts.attach(html_part)
    msg.attach(parts)
    return msg


def TextMessage(subject, fromaddr, toaddr, text, charset=None):
    """Create a text message"""
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['Date'] = gmtime(datetime.utcnow()).strftime('%a, %d %b %Y %H:%M:%S %z (%Z)')
    msg['From'] = fromaddr
    if isinstance(toaddr, (str, unicode)):
        toaddr = (
         toaddr,)
    msg['To'] = (', ').join(toaddr)
    if charset is None:
        charset = chardet.detect(text).get('encoding', 'utf-8')
    plain_part = MIMEText(text, 'plain', charset)
    msg.attach(plain_part)
    return msg
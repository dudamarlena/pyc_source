# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/turbomail/compat.py
# Compiled at: 2009-08-26 19:47:50
"""Compatibility module that exports symbols in a unified way on different 
versions of Python."""
try:
    set = set
except NameError:
    from sets import Set as set

try:
    from email import charset
    from email.encoders import encode_base64
    from email.header import Header
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import formataddr, formatdate, make_msgid, parseaddr, parsedate_tz
except ImportError:
    from email import Charset as charset
    from email.Encoders import encode_base64
    from email.Header import Header
    from email.MIMEBase import MIMEBase
    from email.MIMEImage import MIMEImage
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.Utils import formataddr, formatdate, make_msgid, parseaddr, parsedate_tz

def get_message(e):
    if hasattr(e, 'args') and len(e.args) == 1:
        return e.args[0]
    else:
        return ''
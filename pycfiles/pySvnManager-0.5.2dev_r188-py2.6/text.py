# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/lib/text.py
# Compiled at: 2010-06-08 22:36:02
import locale

def to_unicode(text, charset=None, escape=False):
    """Convert a `str` object to an `unicode` object.
    """
    utext = ''
    if not isinstance(text, str):
        if isinstance(text, Exception):
            try:
                utext = unicode(text)
            except UnicodeError:
                utext = (' ').join([ to_unicode(arg, charset, False) for arg in text.args ])

        else:
            utext = unicode(text)
    else:
        if charset:
            utext = unicode(text, charset, 'replace')
        else:
            try:
                utext = unicode(text, 'utf-8')
            except UnicodeError:
                utext = unicode(text, locale.getpreferredencoding(), 'replace')

        if escape:
            return utext.encode('raw_unicode_escape')
        return utext


def to_utf8(text, charset='gb18030', escape=False):
    """Convert a string to UTF-8, assuming the encoding is either UTF-8, ISO
    Latin-1, or as specified by the optional `charset` parameter.
    """
    utext = ''
    if isinstance(text, unicode):
        utext = text.encode('utf-8')
    else:
        if not isinstance(text, str):
            utext = unicode(text).encode('utf-8')
        else:
            try:
                u = unicode(text, 'utf-8')
                utext = text
            except UnicodeError:
                try:
                    u = unicode(text, charset)
                except UnicodeError:
                    u = unicode(text, 'iso-8859-15')
                else:
                    utext = u.encode('utf-8')

        if escape:
            return repr(utext)[1:-1]
        return utext
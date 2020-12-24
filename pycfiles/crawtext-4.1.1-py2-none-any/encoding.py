# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/c24b/projets/crawtext/newspaper/utils/encoding.py
# Compiled at: 2014-11-06 08:50:33
"""
Byte string <---> unicode conversions take place
here, pretty much anything encoding related
"""
import datetime, types
from decimal import Decimal

class DjangoUnicodeDecodeError(UnicodeDecodeError):

    def __init__(self, obj, *args):
        self.obj = obj
        UnicodeDecodeError.__init__(self, *args)

    def __str__(self):
        original = UnicodeDecodeError.__str__(self)
        return '%s. You passed in %r (%s)' % (original, self.obj,
         type(self.obj))


class StrAndUnicode(object):
    """A class whose __str__ returns its __unicode__ as a UTF-8 bytestring.
    Useful as a mix-in.
    """

    def __str__(self):
        return self.__unicode__().encode('utf-8')


def smart_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
    """Returns a unicode object representing 's'. Treats bytestrings using the
    'encoding' codec.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    return force_unicode(s, encoding, strings_only, errors)


def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_unicode(strings_only=True).
    """
    return isinstance(obj, (
     types.NoneType,
     int, long,
     datetime.datetime, datetime.date, datetime.time,
     float, Decimal))


def force_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
    """Similar to smart_unicode, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if isinstance(s, unicode):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                try:
                    s = unicode(str(s), encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(s, Exception):
                        raise
                    s = (' ').join([ force_unicode(arg, encoding, strings_only, errors) for arg in s
                                   ])

        elif not isinstance(s, unicode):
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise DjangoUnicodeDecodeError(s, *e.args)
        else:
            s = (' ').join([ force_unicode(arg, encoding, strings_only, errors) for arg in s
                           ])

    return s


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """Returns a bytestring version of 's', encoded as specified in 'encoding'.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                return (' ').join([ smart_str(arg, encoding, strings_only, errors) for arg in s
                                  ])
            return unicode(s).encode(encoding, errors)

    else:
        if isinstance(s, unicode):
            return s.encode(encoding, errors)
        else:
            if s and encoding != 'utf-8':
                return s.decode('utf-8', errors).encode(encoding, errors)
            return s
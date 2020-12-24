# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/utils/encoding.py
# Compiled at: 2010-05-30 09:35:01
import types, urllib, datetime

class DjangoUnicodeDecodeError(UnicodeDecodeError):

    def __init__(self, obj, *args):
        self.obj = obj
        UnicodeDecodeError.__init__(self, *args)

    def __str__(self):
        original = UnicodeDecodeError.__str__(self)
        return '%s. You passed in %r (%s)' % (original, self.obj,
         type(self.obj))


class StrAndUnicode(object):
    """
    A class whose __str__ returns its __unicode__ as a UTF-8 bytestring.

    Useful as a mix-in.
    """

    def __str__(self):
        return self.__unicode__().encode('utf-8')


def force_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_unicode, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int, long, datetime.datetime, datetime.date, datetime.time, float)):
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
    except UnicodeDecodeError, e:
        raise DjangoUnicodeDecodeError(s, *e.args)

    return s


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

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


def iri_to_uri(iri):
    """
    Convert an Internationalized Resource Identifier (IRI) portion to a URI
    portion that is suitable for inclusion in a URL.

    This is the algorithm from section 3.1 of RFC 3987.  However, since we are
    assuming input is either UTF-8 or unicode already, we can simplify things a
    little from the full method.

    Returns an ASCII string containing the encoded result.
    """
    if iri is None:
        return iri
    else:
        return urllib.quote(smart_str(iri), safe='/#%[]=:;$&()+,!?*')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/common/encodeutils.py
# Compiled at: 2015-11-08 18:30:19
import sys, six

def safe_decode(text, incoming=None, errors='strict'):
    """Decodes incoming text/bytes string

    Using `incoming` if they're not already unicode.

    :param incoming: Text's current encoding
    :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html
    :returns: text or a unicode `incoming` encoded
                representation of it.
    :raises TypeError: If text is not an instance of str
    """
    if not isinstance(text, (six.string_types, six.binary_type)):
        raise TypeError("%s can't be decoded" % type(text))
    if isinstance(text, six.text_type):
        return text
    if not incoming:
        incoming = sys.stdin.encoding or sys.getdefaultencoding()
    try:
        return text.decode(incoming, errors)
    except UnicodeDecodeError:
        return text.decode('utf-8', errors)


def safe_encode(text, incoming=None, encoding='utf-8', errors='strict'):
    """Encodes incoming text/bytes string using `encoding`.

    If incoming is not specified, text is expected to be encoded with
    current python's default encoding. (`sys.getdefaultencoding`)

    :param incoming: Text's current encoding
    :param encoding: Expected encoding for text (Default UTF-8)
    :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html
    :returns: text or a bytestring `encoding` encoded
                representation of it.
    :raises TypeError: If text is not an instance of str
    """
    if not isinstance(text, (six.string_types, six.binary_type)):
        raise TypeError("%s can't be encoded" % type(text))
    if not incoming:
        incoming = sys.stdin.encoding or sys.getdefaultencoding()
    if hasattr(incoming, 'lower'):
        incoming = incoming.lower()
    if hasattr(encoding, 'lower'):
        encoding = encoding.lower()
    if isinstance(text, six.text_type):
        return text.encode(encoding, errors)
    else:
        if text and encoding != incoming:
            text = safe_decode(text, incoming, errors)
            return text.encode(encoding, errors)
        return text
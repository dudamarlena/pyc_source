# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/backports/email/_encoded_words.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 8443 bytes
""" Routines for manipulating RFC2047 encoded words.

This is currently a package-private API, but will be considered for promotion
to a public API if there is demand.

"""
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.builtins import bytes
from future.builtins import chr
from future.builtins import int
from future.builtins import str
import re, base64, binascii, functools
from string import ascii_letters, digits
from future.backports.email import errors
__all__ = [
 'decode_q',
 'encode_q',
 'decode_b',
 'encode_b',
 'len_q',
 'len_b',
 'decode',
 'encode']
_q_byte_subber = functools.partial(re.compile(b'=([a-fA-F0-9]{2})').sub, lambda m: bytes([int(m.group(1), 16)]))

def decode_q(encoded):
    encoded = bytes(encoded.replace(b'_', b' '))
    return (_q_byte_subber(encoded), [])


class _QByteMap(dict):
    safe = bytes(b'-!*+/' + ascii_letters.encode('ascii') + digits.encode('ascii'))

    def __missing__(self, key):
        if key in self.safe:
            self[key] = chr(key)
        else:
            self[key] = '={:02X}'.format(key)
        return self[key]


_q_byte_map = _QByteMap()
_q_byte_map[ord(' ')] = '_'

def encode_q(bstring):
    return str(''.join(_q_byte_map[x] for x in bytes(bstring)))


def len_q(bstring):
    return sum(len(_q_byte_map[x]) for x in bytes(bstring))


def decode_b(encoded):
    defects = []
    pad_err = len(encoded) % 4
    if pad_err:
        defects.append(errors.InvalidBase64PaddingDefect())
        padded_encoded = encoded + b'==='[:4 - pad_err]
    else:
        padded_encoded = encoded
    try:
        if not re.match(b'^[A-Za-z0-9+/]*={0,2}$', padded_encoded):
            raise binascii.Error('Non-base64 digit found')
        return (
         base64.b64decode(padded_encoded), defects)
    except binascii.Error:
        defects = [
         errors.InvalidBase64CharactersDefect()]
        for i in (0, 1, 2, 3):
            try:
                return (
                 base64.b64decode(encoded + b'=' * i), defects)
            except (binascii.Error, TypeError):
                if i == 0:
                    defects.append(errors.InvalidBase64PaddingDefect())

        else:
            raise AssertionError('unexpected binascii.Error')


def encode_b(bstring):
    return base64.b64encode(bstring).decode('ascii')


def len_b(bstring):
    groups_of_3, leftover = divmod(len(bstring), 3)
    return groups_of_3 * 4 + (4 if leftover else 0)


_cte_decoders = {'q': decode_q, 
 'b': decode_b}

def decode(ew):
    """Decode encoded word and return (string, charset, lang, defects) tuple.

    An RFC 2047/2243 encoded word has the form:

        =?charset*lang?cte?encoded_string?=

    where '*lang' may be omitted but the other parts may not be.

    This function expects exactly such a string (that is, it does not check the
    syntax and may raise errors if the string is not well formed), and returns
    the encoded_string decoded first from its Content Transfer Encoding and
    then from the resulting bytes into unicode using the specified charset.  If
    the cte-decoded string does not successfully decode using the specified
    character set, a defect is added to the defects list and the unknown octets
    are replaced by the unicode 'unknown' character \ufdff.

    The specified charset and language are returned.  The default for language,
    which is rarely if ever encountered, is the empty string.

    """
    _, charset, cte, cte_string, _ = str(ew).split('?')
    charset, _, lang = charset.partition('*')
    cte = cte.lower()
    bstring = cte_string.encode('ascii', 'surrogateescape')
    bstring, defects = _cte_decoders[cte](bstring)
    try:
        string = bstring.decode(charset)
    except UnicodeError:
        defects.append(errors.UndecodableBytesDefect('Encoded word contains bytes not decodable using {} charset'.format(charset)))
        string = bstring.decode(charset, 'surrogateescape')
    except LookupError:
        string = bstring.decode('ascii', 'surrogateescape')
        if charset.lower() != 'unknown-8bit':
            defects.append(errors.CharsetError('Unknown charset {} in encoded word; decoded as unknown bytes'.format(charset)))

    return (
     string, charset, lang, defects)


_cte_encoders = {'q': encode_q, 
 'b': encode_b}
_cte_encode_length = {'q': len_q, 
 'b': len_b}

def encode(string, charset='utf-8', encoding=None, lang=''):
    """Encode string using the CTE encoding that produces the shorter result.

    Produces an RFC 2047/2243 encoded word of the form:

        =?charset*lang?cte?encoded_string?=

    where '*lang' is omitted unless the 'lang' parameter is given a value.
    Optional argument charset (defaults to utf-8) specifies the charset to use
    to encode the string to binary before CTE encoding it.  Optional argument
    'encoding' is the cte specifier for the encoding that should be used ('q'
    or 'b'); if it is None (the default) the encoding which produces the
    shortest encoded sequence is used, except that 'q' is preferred if it is up
    to five characters longer.  Optional argument 'lang' (default '') gives the
    RFC 2243 language string to specify in the encoded word.

    """
    string = str(string)
    if charset == 'unknown-8bit':
        bstring = string.encode('ascii', 'surrogateescape')
    else:
        bstring = string.encode(charset)
    if encoding is None:
        qlen = _cte_encode_length['q'](bstring)
        blen = _cte_encode_length['b'](bstring)
        encoding = 'q' if qlen - blen < 5 else 'b'
    encoded = _cte_encoders[encoding](bstring)
    if lang:
        lang = '*' + lang
    return '=?{0}{1}?{2}?{3}?='.format(charset, lang, encoding, encoded)
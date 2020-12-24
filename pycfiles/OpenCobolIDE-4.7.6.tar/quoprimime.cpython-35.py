# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/backports/email/quoprimime.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 10923 bytes
"""Quoted-printable content transfer encoding per RFCs 2045-2047.

This module handles the content transfer encoding method defined in RFC 2045
to encode US ASCII-like 8-bit data called `quoted-printable'.  It is used to
safely encode text that is in a character set similar to the 7-bit US ASCII
character set, but that includes some 8-bit characters that are normally not
allowed in email bodies or headers.

Quoted-printable is very space-inefficient for encoding binary files; use the
email.base64mime module for that instead.

This module provides an interface to encode and decode both headers and bodies
with quoted-printable encoding.

RFC 2045 defines a method for including character set information in an
`encoded-word' in a header.  This method is commonly used for 8-bit real names
in To:/From:/Cc: etc. fields, as well as Subject: lines.

This module does not do the line wrapping or end-of-line character
conversion necessary for proper internationalized headers; it only
does dumb encoding and decoding.  To deal with the various line
wrapping issues, use the email.header module.
"""
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.builtins import bytes, chr, dict, int, range, super
__all__ = [
 'body_decode',
 'body_encode',
 'body_length',
 'decode',
 'decodestring',
 'header_decode',
 'header_encode',
 'header_length',
 'quote',
 'unquote']
import re, io
from string import ascii_letters, digits, hexdigits
CRLF = '\r\n'
NL = '\n'
EMPTYSTRING = ''
_QUOPRI_HEADER_MAP = dict((c, '=%02X' % c) for c in range(256))
_QUOPRI_BODY_MAP = _QUOPRI_HEADER_MAP.copy()
for c in bytes(b'-!*+/' + ascii_letters.encode('ascii') + digits.encode('ascii')):
    _QUOPRI_HEADER_MAP[c] = chr(c)

_QUOPRI_HEADER_MAP[ord(' ')] = '_'
for c in bytes(b' !"#$%&\'()*+,-./0123456789:;<>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\t'):
    _QUOPRI_BODY_MAP[c] = chr(c)

def header_check(octet):
    """Return True if the octet should be escaped with header quopri."""
    return chr(octet) != _QUOPRI_HEADER_MAP[octet]


def body_check(octet):
    """Return True if the octet should be escaped with body quopri."""
    return chr(octet) != _QUOPRI_BODY_MAP[octet]


def header_length(bytearray):
    """Return a header quoted-printable encoding length.

    Note that this does not include any RFC 2047 chrome added by
    `header_encode()`.

    :param bytearray: An array of bytes (a.k.a. octets).
    :return: The length in bytes of the byte array when it is encoded with
        quoted-printable for headers.
    """
    return sum(len(_QUOPRI_HEADER_MAP[octet]) for octet in bytearray)


def body_length(bytearray):
    """Return a body quoted-printable encoding length.

    :param bytearray: An array of bytes (a.k.a. octets).
    :return: The length in bytes of the byte array when it is encoded with
        quoted-printable for bodies.
    """
    return sum(len(_QUOPRI_BODY_MAP[octet]) for octet in bytearray)


def _max_append(L, s, maxlen, extra=''):
    if not isinstance(s, str):
        s = chr(s)
    if not L:
        L.append(s.lstrip())
    else:
        if len(L[(-1)]) + len(s) <= maxlen:
            L[(-1)] += extra + s
        else:
            L.append(s.lstrip())


def unquote(s):
    """Turn a string in the form =AB to the ASCII character with value 0xab"""
    return chr(int(s[1:3], 16))


def quote(c):
    return '=%02X' % ord(c)


def header_encode(header_bytes, charset='iso-8859-1'):
    """Encode a single header line with quoted-printable (like) encoding.

    Defined in RFC 2045, this `Q' encoding is similar to quoted-printable, but
    used specifically for email header fields to allow charsets with mostly 7
    bit characters (and some 8 bit) to remain more or less readable in non-RFC
    2045 aware mail clients.

    charset names the character set to use in the RFC 2046 header.  It
    defaults to iso-8859-1.
    """
    if not header_bytes:
        return ''
    encoded = []
    for octet in header_bytes:
        encoded.append(_QUOPRI_HEADER_MAP[octet])

    return '=?%s?q?%s?=' % (charset, EMPTYSTRING.join(encoded))


class _body_accumulator(io.StringIO):

    def __init__(self, maxlinelen, eol, *args, **kw):
        super().__init__(*args, **kw)
        self.eol = eol
        self.maxlinelen = self.room = maxlinelen

    def write_str(self, s):
        """Add string s to the accumulated body."""
        self.write(s)
        self.room -= len(s)

    def newline(self):
        """Write eol, then start new line."""
        self.write_str(self.eol)
        self.room = self.maxlinelen

    def write_soft_break(self):
        """Write a soft break, then start a new line."""
        self.write_str('=')
        self.newline()

    def write_wrapped(self, s, extra_room=0):
        """Add a soft line break if needed, then write s."""
        if self.room < len(s) + extra_room:
            self.write_soft_break()
        self.write_str(s)

    def write_char(self, c, is_last_char):
        if not is_last_char:
            self.write_wrapped(c, extra_room=1)
        else:
            if c not in ' \t':
                self.write_wrapped(c)
            else:
                if self.room >= 3:
                    self.write(quote(c))
                else:
                    if self.room == 2:
                        self.write(c)
                        self.write_soft_break()
                    else:
                        self.write_soft_break()
                        self.write(quote(c))


def body_encode(body, maxlinelen=76, eol=NL):
    r"""Encode with quoted-printable, wrapping at maxlinelen characters.

    Each line of encoded text will end with eol, which defaults to "\n".  Set
    this to "\r\n" if you will be using the result of this function directly
    in an email.

    Each line will be wrapped at, at most, maxlinelen characters before the
    eol string (maxlinelen defaults to 76 characters, the maximum value
    permitted by RFC 2045).  Long lines will have the 'soft line break'
    quoted-printable character "=" appended to them, so the decoded text will
    be identical to the original text.

    The minimum maxlinelen is 4 to have room for a quoted character ("=XX")
    followed by a soft line break.  Smaller values will generate a
    ValueError.

    """
    if maxlinelen < 4:
        raise ValueError('maxlinelen must be at least 4')
    if not body:
        return body
    last_has_eol = body[(-1)] in '\r\n'
    encoded_body = _body_accumulator(maxlinelen, eol)
    lines = body.splitlines()
    last_line_no = len(lines) - 1
    for line_no, line in enumerate(lines):
        last_char_index = len(line) - 1
        for i, c in enumerate(line):
            if body_check(ord(c)):
                c = quote(c)
            encoded_body.write_char(c, i == last_char_index)

        if line_no < last_line_no or last_has_eol:
            encoded_body.newline()

    return encoded_body.getvalue()


def decode(encoded, eol=NL):
    r"""Decode a quoted-printable string.

    Lines are separated with eol, which defaults to \n.
    """
    if not encoded:
        return encoded
    decoded = ''
    for line in encoded.splitlines():
        line = line.rstrip()
        if not line:
            decoded += eol
            continue
            i = 0
            n = len(line)
            while i < n:
                c = line[i]
                if c != '=':
                    decoded += c
                    i += 1
                else:
                    if i + 1 == n:
                        i += 1
                        continue
                    else:
                        if i + 2 < n and line[(i + 1)] in hexdigits and line[(i + 2)] in hexdigits:
                            decoded += unquote(line[i:i + 3])
                            i += 3
                        else:
                            decoded += c
                            i += 1
                if i == n:
                    decoded += eol

    if encoded[(-1)] not in '\r\n' and decoded.endswith(eol):
        decoded = decoded[:-1]
    return decoded


body_decode = decode
decodestring = decode

def _unquote_match(match):
    """Turn a match in the form =AB to the ASCII character with value 0xab"""
    s = match.group(0)
    return unquote(s)


def header_decode(s):
    """Decode a string encoded with RFC 2045 MIME header `Q' encoding.

    This function does not parse a full MIME header value encoded with
    quoted-printable (like =?iso-8895-1?q?Hello_World?=) -- please use
    the high level email.header class for that functionality.
    """
    s = s.replace('_', ' ')
    return re.sub('=[a-fA-F0-9]{2}', _unquote_match, s, re.ASCII)
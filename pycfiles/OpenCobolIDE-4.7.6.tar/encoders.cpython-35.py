# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/backports/email/encoders.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 2800 bytes
"""Encodings and related functions."""
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.builtins import str
__all__ = [
 'encode_7or8bit',
 'encode_base64',
 'encode_noop',
 'encode_quopri']
try:
    from base64 import encodebytes as _bencode
except ImportError:
    from base64 import encodestring as _bencode

from quopri import encodestring as _encodestring

def _qencode(s):
    enc = _encodestring(s, quotetabs=True)
    return enc.replace(' ', '=20')


def encode_base64(msg):
    """Encode the message's payload in Base64.

    Also, add an appropriate Content-Transfer-Encoding header.
    """
    orig = msg.get_payload()
    encdata = str(_bencode(orig), 'ascii')
    msg.set_payload(encdata)
    msg['Content-Transfer-Encoding'] = 'base64'


def encode_quopri(msg):
    """Encode the message's payload in quoted-printable.

    Also, add an appropriate Content-Transfer-Encoding header.
    """
    orig = msg.get_payload()
    encdata = _qencode(orig)
    msg.set_payload(encdata)
    msg['Content-Transfer-Encoding'] = 'quoted-printable'


def encode_7or8bit(msg):
    """Set the Content-Transfer-Encoding header to 7bit or 8bit."""
    orig = msg.get_payload()
    if orig is None:
        msg['Content-Transfer-Encoding'] = '7bit'
        return
    try:
        if isinstance(orig, str):
            orig.encode('ascii')
        else:
            orig.decode('ascii')
    except UnicodeError:
        charset = msg.get_charset()
        output_cset = charset and charset.output_charset
        if output_cset and output_cset.lower().startswith('iso-2022-'):
            msg['Content-Transfer-Encoding'] = '7bit'
        else:
            msg['Content-Transfer-Encoding'] = '8bit'
    else:
        msg['Content-Transfer-Encoding'] = '7bit'
    if not isinstance(orig, str):
        msg.set_payload(orig.decode('ascii', 'surrogateescape'))


def encode_noop(msg):
    """Do nothing."""
    orig = msg.get_payload()
    if not isinstance(orig, str):
        msg.set_payload(orig.decode('ascii', 'surrogateescape'))
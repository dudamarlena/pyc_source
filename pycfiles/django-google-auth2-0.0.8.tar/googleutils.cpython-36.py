# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/GoogleAuthenticatorPyPI/django_google_auth/utils/googleutils/googleutils.py
# Compiled at: 2019-04-01 22:45:59
# Size of source mod 2**32: 2797 bytes
from __future__ import print_function, unicode_literals, division, absolute_import
import unicodedata
try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

def build_uri(secret, name, initial_count=None, issuer_name=None):
    """
    Returns the provisioning URI for the OTP; works for either TOTP or HOTP.

    This can then be encoded in a QR Code and used to provision the Google
    Authenticator app.

    For module-internal use.

    See also:
        http://code.google.com/p/google-authenticator/wiki/KeyUriFormat

    @param [String] the hotp/totp secret used to generate the URI
    @param [String] name of the account
    @param [Integer] initial_count starting counter value, defaults to None.
        If none, the OTP type will be assumed as TOTP.
    @param [String] the name of the OTP issuer; this will be the
        organization title of the OTP entry in Authenticator
    @return [String] provisioning uri
    """
    is_initial_count_present = initial_count is not None
    otp_type = 'hotp' if is_initial_count_present else 'totp'
    base = 'otpauth://%s/' % otp_type
    if issuer_name:
        issuer_name = quote(issuer_name)
        base += '%s:' % issuer_name
    uri = '%(base)s%(name)s?secret=%(secret)s' % {'name':quote(name, safe='@'), 
     'secret':secret, 
     'base':base}
    if is_initial_count_present:
        uri += '&counter=%s' % initial_count
    if issuer_name:
        uri += '&issuer=%s' % issuer_name
    return uri


def _compare_digest(s1, s2):
    differences = 0
    for c1, c2 in izip_longest(s1, s2):
        if c1 is None or c2 is None:
            differences = 1
        else:
            differences |= ord(c1) ^ ord(c2)

    return differences == 0


try:
    from hmac import compare_digest
except ImportError:
    compare_digest = _compare_digest

def strings_equal(s1, s2):
    """
    Timing-attack resistant string comparison.

    Normal comparison using == will short-circuit on the first mismatching
    character. This avoids that by scanning the whole string, though we
    still reveal to a timing attack whether the strings are the same
    length.
    """
    try:
        s1 = unicodedata.normalize('NFKC', str(s1))
        s2 = unicodedata.normalize('NFKC', str(s2))
    except:
        s1 = unicodedata.normalize('NFKC', unicode(s1))
        s2 = unicodedata.normalize('NFKC', unicode(s2))

    return compare_digest(s1, s2)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/didi/PycharmProjects/nnmail/yamail/validate.py
# Compiled at: 2017-06-25 19:03:20
# Size of source mod 2**32: 5157 bytes
""" Module for validating emails.
"Forked" only the regexp part from the "validate_email", see copyright below.
The reason is that if you plan on sending out loads of emails or
doing checks can actually get you blacklisted, if it would be reliable at all.
However, this regexp is the best one I've come accross, so props to Syrus Akbary.
"""
import re
try:
    from .error import YagInvalidEmailAddress
except (ValueError, SystemError):
    from error import YagInvalidEmailAddress

WSP = '[ \\t]'
CRLF = '(?:\\r\\n)'
NO_WS_CTL = '\\x01-\\x08\\x0b\\x0c\\x0f-\\x1f\\x7f'
QUOTED_PAIR = '(?:\\\\.)'
FWS = '(?:(?:' + WSP + '*' + CRLF + ')?' + WSP + '+)'
CTEXT = '[' + NO_WS_CTL + '\\x21-\\x27\\x2a-\\x5b\\x5d-\\x7e]'
CCONTENT = '(?:' + CTEXT + '|' + QUOTED_PAIR + ')'
COMMENT = '\\((?:' + FWS + '?' + CCONTENT + ')*' + FWS + '?\\)'
CFWS = '(?:' + FWS + '?' + COMMENT + ')*(?:' + FWS + '?' + COMMENT + '|' + FWS + ')'
ATEXT = "[\\w!#$%&\\'\\*\\+\\-/=\\?\\^`\\{\\|\\}~]"
ATOM = CFWS + '?' + ATEXT + '+' + CFWS + '?'
DOT_ATOM_TEXT = ATEXT + '+(?:\\.' + ATEXT + '+)*'
DOT_ATOM = CFWS + '?' + DOT_ATOM_TEXT + CFWS + '?'
QTEXT = '[' + NO_WS_CTL + '\\x21\\x23-\\x5b\\x5d-\\x7e]'
QCONTENT = '(?:' + QTEXT + '|' + QUOTED_PAIR + ')'
QUOTED_STRING = CFWS + '?' + '"(?:' + FWS + '?' + QCONTENT + ')*' + FWS + '?' + '"' + CFWS + '?'
LOCAL_PART = '(?:' + DOT_ATOM + '|' + QUOTED_STRING + ')'
DTEXT = '[' + NO_WS_CTL + '\\x21-\\x5a\\x5e-\\x7e]'
DCONTENT = '(?:' + DTEXT + '|' + QUOTED_PAIR + ')'
DOMAIN_LITERAL = CFWS + '?' + '\\[' + '(?:' + FWS + '?' + DCONTENT + ')*' + FWS + '?\\]' + CFWS + '?'
DOMAIN = '(?:' + DOT_ATOM + '|' + DOMAIN_LITERAL + ')'
ADDR_SPEC = LOCAL_PART + '@' + DOMAIN
VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'

def validate_email_with_regex(email_address):
    """
    Note that this will only filter out syntax mistakes in emailaddresses.
    If a human would think it is probably a valid email, it will most likely pass.
    However, it could still very well be that the actual emailaddress has simply
    not be claimed by anyone (so then this function fails to devalidate).
    """
    if not re.match(VALID_ADDRESS_REGEXP, email_address):
        emsg = 'Emailaddress "{}" is not valid according to RFC 2822 standards'.format(email_address)
        raise YagInvalidEmailAddress(emsg)
    if '.' not in email_address:
        if 'localhost' not in email_address.lower():
            raise YagInvalidEmailAddress('Missing dot in emailaddress')
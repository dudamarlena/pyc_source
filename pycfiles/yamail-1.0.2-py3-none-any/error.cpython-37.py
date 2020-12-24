# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/didi/PycharmProjects/nnmail/yamail/error.py
# Compiled at: 2017-05-10 07:50:44
# Size of source mod 2**32: 1173 bytes
"""Contains the exceptions"""

class YagConnectionClosed(Exception):
    __doc__ = '\n    The connection object has been closed by the user.\n    This object can be used to send emails again after logging in,\n    using self.login().\n    '


class YagAddressError(Exception):
    __doc__ = "\n    This means that the address was given in an invalid format.\n    Note that From can either be a string, or a dictionary where the key is an email,\n    and the value is an alias {'sample@gmail.com', 'Sam'}. In the case of 'to',\n    it can either be a string (email), a list of emails (email addresses without aliases)\n    or a dictionary where keys are the email addresses and the values indicate the aliases.\n    Furthermore, it does not do any validation of whether an email exists.\n    "


class YagInvalidEmailAddress(Exception):
    __doc__ = '\n    Note that this will only filter out syntax mistakes in emailaddresses.\n    If a human would think it is probably a valid email, it will most likely pass.\n    However, it could still very well be that the actual emailaddress has simply\n    not be claimed by anyone (so then this function fails to devalidate).\n    '
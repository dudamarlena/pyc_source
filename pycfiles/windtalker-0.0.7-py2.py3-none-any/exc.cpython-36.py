# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/windtalker-project/windtalker/exc.py
# Compiled at: 2020-03-04 17:13:17
# Size of source mod 2**32: 227 bytes


class PasswordError(Exception):
    __doc__ = 'symmetric encrypt wrong password error.\n    '


class SignatureError(Exception):
    __doc__ = 'asymmetric encrypt wrong signature error.\n    '
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/to_email.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 96 bytes
from .email import Email

class To(Email):
    __doc__ = 'A to email address with an optional name.'
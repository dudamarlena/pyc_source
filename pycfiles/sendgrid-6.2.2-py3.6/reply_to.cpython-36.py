# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/reply_to.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 107 bytes
from .email import Email

class ReplyTo(Email):
    __doc__ = 'A reply to email address with an optional name.'
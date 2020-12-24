# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/todd/github/python-email-split/email_split/__init__.py
# Compiled at: 2016-02-04 14:02:27


class Email(object):

    def __init__(self, local, domain):
        self.local = local
        self.domain = domain

    @classmethod
    def split_email(cls, email):
        """Break up an email and initialize a new class"""
        local, _, domain = email.partition('@')
        return Email(local=local, domain=domain)


email_split = Email.split_email
# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjama/core/exceptions.py
# Compiled at: 2012-01-06 12:40:57
__doc__ = '\nCreated on Dec 29, 2011\n\n@author: maemo\n'
from ..common import version
version.getInstance().submitRevision('$Revision: 131 $')

class PyjamaCaptchaException(Exception):
    """
    Login failure because google required a capcha
    """

    def __init__(self, token, url, doc_storage=None):
        self.captcha_token = token
        self.captcha_url = url
        self.doc_storage = doc_storage

    def get_token(self):
        return self.captcha_token

    def get_url(self):
        return self.captcha_url

    def get_storage(self):
        return self.doc_storage
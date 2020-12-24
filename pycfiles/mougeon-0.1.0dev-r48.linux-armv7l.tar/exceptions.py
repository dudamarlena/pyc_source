# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mougeon/core/exceptions.py
# Compiled at: 2012-03-01 11:28:38
"""
Created on 01 March 2012 04:19:29

@author: maemo
"""
from ..common import version
version.getInstance().submitRevision('$Revision: 3 $')

class MougeonCaptchaException(Exception):
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
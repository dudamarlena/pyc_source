# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/net/www/url_lib.py
# Compiled at: 2016-07-25 10:38:46
"""url_lib"""
from urllib import FancyURLopener

class NoAsk_URLopener(FancyURLopener):
    """URL opener that does not ask for a password interactively"""

    def __init__(self, username, password):
        FancyURLopener.__init__(self)
        self.username = username
        self.password = password
        self._asked = 0

    def prompt_user_passwd(self, host, realm):
        if self._asked:
            return (None, None)
        else:
            self._asked = 1
            return (self.username, self.password)
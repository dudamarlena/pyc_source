# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kclient/subscribe.py
# Compiled at: 2018-03-10 04:55:35
"""
    kclient.subscribe
    ~~~~~~~~~~

    Python wrapper for k-client Subscribe API.
"""
from .client import Client
from .enums import Groups

class Subscribe(Client):

    def list(self):
        """
        :return:
        """
        return self._post('/subscribe/list')
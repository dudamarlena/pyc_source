# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kclient/group.py
# Compiled at: 2018-03-10 04:55:20
"""
    kclient.subscribe
    ~~~~~~~~~~

    Python wrapper for k-client Group API.
"""
from .client import Client
from .enums import Groups

class Group(Client):

    def info(self, group=Groups.KEYAKIZAKA):
        """

        :return:
        """
        param = {'group': group.value}
        return self._post('/group/info', param)
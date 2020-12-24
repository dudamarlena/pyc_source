# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/domain/user.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 765 bytes


class User(object):

    def __init__(self, account, name='', privilege='', client=None):
        self._User__account = account
        self._User__name = name
        self._User__client_object = client
        self._User__privilege = privilege

    @property
    def account(self):
        return self._User__account

    @property
    def name(self):
        return self._User__name

    @property
    def privilege(self):
        return self._User__privilege

    @property
    def client_object(self):
        return self._User__client_object

    @name.setter
    def name(self, value):
        self._User__name = value

    @privilege.setter
    def privilege(self, value):
        self._User__privilege = value

    @client_object.setter
    def client_object(self, obj):
        self._User__client_object = obj
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/account.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 1233 bytes
"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""
from . import JsonObject, JsonList

class Account(JsonObject):
    __doc__ = '\n    Represents a tenant account on the controller. The following attributes are defined:\n\n    .. data:: id\n\n        Numeric ID of the account.\n\n    .. data:: name\n\n        Account name.\n    '
    FIELDS = {'id':'', 
     'name':''}

    def __init__(self, acct_id='0', name=None):
        self.id, self.name = acct_id, name


class Accounts(JsonList):
    __doc__ = '\n    Represents a collection of :class:Account objects. Extends :class:UserList, so it supports the\n    standard array index and :keyword:`for` semantics.\n    '

    def __init__(self, initial_list=None):
        super(Accounts, self).__init__(Account, initial_list)

    def __getitem__(self, i):
        """
        :rtype: Account
        """
        return self.data[i]

    def by_name(self, name):
        """
        Finds an account by name.

        :returns: First account with the correct name
        :rtype: Account
        """
        found = [x for x in self.data if x.name == name]
        try:
            return found[0]
        except IndexError:
            raise KeyError(name)
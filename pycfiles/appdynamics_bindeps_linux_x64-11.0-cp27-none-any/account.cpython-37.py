# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/account.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 1233 bytes
__doc__ = '\nModel classes for AppDynamics REST API\n\n.. moduleauthor:: Todd Radel <tradel@appdynamics.com>\n'
from . import JsonObject, JsonList

class Account(JsonObject):
    """Account"""
    FIELDS = {'id':'', 
     'name':''}

    def __init__(self, acct_id='0', name=None):
        self.id, self.name = acct_id, name


class Accounts(JsonList):
    """Accounts"""

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
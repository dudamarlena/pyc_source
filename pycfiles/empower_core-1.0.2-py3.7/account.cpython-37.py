# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/accountsmanager/account.py
# Compiled at: 2020-05-10 06:48:31
# Size of source mod 2**32: 1746 bytes
"""Account Class."""
from pymodm import MongoModel, fields
from empower_core.serialize import serializable_dict

@serializable_dict
class Account(MongoModel):
    __doc__ = 'An user account on this controller.'
    username = fields.CharField(primary_key=True)
    password = fields.CharField(required=True)
    name = fields.CharField(required=True)
    email = fields.EmailField(required=True)

    def to_dict(self):
        """Return JSON-serializable representation of the object."""
        return {'username':self.username, 
         'name':self.name, 
         'email':self.email}

    def to_str(self):
        """Return an ASCII representation of the object."""
        return str(self.username)

    def __str__(self):
        return self.to_str()

    def __hash__(self):
        return hash(self.username)

    def __eq__(self, other):
        if isinstance(other, Account):
            return self.username == other.username
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + "('" + self.to_str() + "')"
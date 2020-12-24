# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/acl.py
# Compiled at: 2020-05-10 06:48:38
# Size of source mod 2**32: 1669 bytes
"""Access Control List."""
from pymodm import MongoModel, fields
from empower_core.etheraddress import EtherAddressField
from empower_core.serialize import serializable_dict

@serializable_dict
class ACL(MongoModel):
    __doc__ = 'Access Control List.'
    addr = EtherAddressField(primary_key=True)
    desc = fields.CharField(required=True)

    def to_dict(self):
        """Return JSON-serializable representation of the object."""
        out = {'addr':self.addr, 
         'desc':self.desc}
        return out

    def to_str(self):
        """Return an ASCII representation of the object."""
        return '%s' % self.addr

    def __str__(self):
        return self.to_str()

    def __hash__(self):
        return hash(self.addr)

    def __eq__(self, other):
        if isinstance(other, ACL):
            return self.addr == other.addr
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + "('" + self.to_str() + "')"
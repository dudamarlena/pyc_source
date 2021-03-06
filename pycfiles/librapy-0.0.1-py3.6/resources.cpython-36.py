# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/types/resources.py
# Compiled at: 2019-09-05 06:49:35
# Size of source mod 2**32: 1597 bytes
"""
Each Libra resource is stored relative to a specific path represented by an
AccessPath. Each AccessPath consists of a StructTag and a list of accesses
concatenated together.
"""
from librapy.lib.lcs import Serializer
import librapy.lib.hasher as hasher

class AccessPath:
    resource_tag = '01'
    separator = '/'

    def accesses_as_separated_string(accesses):
        path = ''
        for access in accesses:
            path += str(access) + AccessPath.separator

        return path

    def resource_access_vec(struct_tag, accesses):
        path = bytes.fromhex(AccessPath.resource_tag)
        path += struct_tag.hash()
        path += AccessPath.accesses_as_separated_string(accesses).encode('utf8')
        return path


class StructTag:

    def __init__(self, account_address, module, name, type_params):
        self.account_address = account_address
        self.module = module
        self.name = name
        self.type_params = type_params

    @classmethod
    def get_hash_prefix(cls):
        return b'VM_ACCESS_PATH'

    def hash(self):
        serializer = Serializer()
        serializer.encode_struct(self)
        hf = hasher.get_hash_function(self)
        hf.update(serializer.get_buffer())
        return hf.digest()

    def serialize(self, serializer):
        serializer.encode_struct(self.account_address)
        serializer.encode_string(self.module)
        serializer.encode_string(self.name)
        serializer.encode_vec_for_struct(self.type_params)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/types/program.py
# Compiled at: 2019-09-05 07:31:14
# Size of source mod 2**32: 3298 bytes
"""
Core components for constructing and parsing Libra transactions
"""
import json, os.path
from librapy.lib.common import InvalidInstanceException
from librapy.types.account_address import AccountAddress

class Program:

    def __init__(self, args, code=None, modules=None):
        self.code = code if code is not None else self.load_program()
        self.args = args
        self.modules = modules if modules is not None else []

    def __repr__(self):
        return 'Program(\n\tcode: {}\n\targs: {}\n\tmodules: {}\n)'.format(self.code.hex(), self.args, map(lambda x: x.hex(), self.modules))

    def deserialize(deserializer):
        code = deserializer.decode_bytes()
        args = deserializer.decode_vec_for_struct(TransactionArgument)
        modules = deserializer.decode_vec(deserializer.decode_bytes)
        return Program(args, code, modules)

    def get_path(self):
        raise NotImplementedError()

    def load_program(self):
        actual_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'programs', self.get_path())
        with open(actual_path) as (f):
            data = json.load(f)
        code = data['code']
        return bytes(code)

    def serialize(self, serializer):
        serializer.encode_bytes(self.code)
        serializer.encode_vec(self.args, serializer.encode_struct)
        serializer.encode_vec(self.modules, serializer.encode_bytes)


class TransactionArgument:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'TransactionArgument({})'.format(self.value)

    def type_to_u32(self):
        if isinstance(self.value, int):
            return 0
        else:
            if isinstance(self.value, AccountAddress):
                return 1
            if isinstance(self.value, str):
                return 2
            if isinstance(self.value, bytes):
                return 3
        raise InvalidInstanceException()

    def deserialize(deserializer):
        value_type = deserializer.decode_u32()
        if value_type == 0:
            return TransactionArgument(deserializer.decode_u64())
        if value_type == 1:
            return TransactionArgument(deserializer.decode_struct(AccountAddress))
        if value_type == 2:
            return TransactionArgument(deserializer.decode_string())
        if value_type == 3:
            return TransactionArgument(deserializer.decode_bytes())
        raise InvalidInstanceException(value_type)

    def serialize(self, serializer):
        serializer.encode_u32(self.type_to_u32())
        if isinstance(self.value, int):
            serializer.encode_u64(self.value)
            return serializer
        if isinstance(self.value, AccountAddress):
            serializer.encode_struct(self.value)
            return serializer
        if isinstance(self.value, str):
            serializer.encode_string(self.value)
            return serializer
        if isinstance(self.value, bytes):
            serializer.encode_bytes(self.value)
            return serializer
        raise InvalidInstanceException()
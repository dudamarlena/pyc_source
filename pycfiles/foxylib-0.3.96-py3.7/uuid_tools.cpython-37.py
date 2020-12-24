# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/uuid/uuid_tools.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 2660 bytes
from uuid import UUID
from foxylib.tools.binary2text.base64_tool import Base64Tool
from foxylib.tools.function.function_tool import FunctionTool

class UUIDToolkit:

    @classmethod
    def uuid2hex(cls, uuid):
        if uuid is not None:
            return uuid.hex

    class NotUUIDException(Exception):
        pass

    @classmethod
    def x2uuid(cls, x_UUID):
        if x_UUID is None:
            return
        else:
            if x_UUID == 'null':
                return
            if isinstance(x_UUID, UUID):
                return x_UUID
            try:
                if len(x_UUID) <= 24:
                    return Base64Tool.b642uuid(x_UUID)
                return UUID(x_UUID)
            except ValueError as e:
                try:
                    raise cls.NotUUIDException(x_UUID)
                finally:
                    e = None
                    del e

    @classmethod
    def x2hex(cls, x_UUID):
        uuid = cls.x2uuid(x_UUID)
        s = cls.uuid2hex(uuid)
        return s

    @classmethod
    def x2b64(cls, x_UUID):
        uuid = cls.x2uuid(x_UUID)
        if not uuid:
            return
        return Base64Tool.uuid2b64(uuid)

    @classmethod
    def equals(cls, x1, x2):
        return cls.x2uuid(x1) == cls.x2uuid(x2)

    @classmethod
    def contains(cls, l, x):
        x_uuid = cls.x2uuid(x)
        for y in l:
            if cls.x2uuid(y) == x_uuid:
                return True

        return False

    has = contains

    @classmethod
    def contained_by(cls, x, l):
        return cls.contains(l, x)

    @classmethod
    def _collection2convert_uuid(cls, x, kv2is_uuid, uuid_converter):
        if isinstance(x, list):
            return [cls._collection2convert_uuid(y, kv2is_uuid, uuid_converter) for y in x]
        if isinstance(x, dict):
            h = {}
            for k, v_IN in x.items():
                if kv2is_uuid(k, v_IN):
                    v_OUT = uuid_converter(v_IN)
                else:
                    v_OUT = cls._collection2convert_uuid(v_IN, kv2is_uuid, uuid_converter)
                h[k] = v_OUT

            return h
        return x

    @classmethod
    def h2j(cls, h, kv2is_uuid):
        return cls._collection2convert_uuid(h, kv2is_uuid, cls.x2hex)

    @classmethod
    def j2h(cls, j, kv2is_uuid):
        return cls._collection2convert_uuid(j, kv2is_uuid, cls.x2uuid)


uuid_in = UUIDToolkit.contained_by
uuid_not_in = FunctionTool.wrap2negate(uuid_in)
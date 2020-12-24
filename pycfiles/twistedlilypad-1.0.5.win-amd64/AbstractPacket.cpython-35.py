# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Packets\AbstractPacket.py
# Compiled at: 2015-01-14 16:07:39
# Size of source mod 2**32: 627 bytes


class AbstractPacket(object):
    opcode = -1


class AbstractPacketCodec(object):

    @staticmethod
    def decode(payload):
        raise NotImplementedError

    @staticmethod
    def encode(packet):
        raise NotImplementedError


class StatusCode:
    SUCCESS = 0
    ERROR_GENERIC = 1
    ERROR_ROLE = 2

    @classmethod
    def pprint(cls, code):
        if code == cls.SUCCESS:
            return 'SUCCESS'
        else:
            if code == cls.ERROR_GENERIC:
                return 'ERROR_GENERIC'
            if code == cls.ERROR_ROLE:
                return 'ERROR_ROLE'
            return 'unknown status code'
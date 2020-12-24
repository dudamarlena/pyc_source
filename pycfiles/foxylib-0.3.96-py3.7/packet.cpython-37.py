# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/khalalib/packet/packet.py
# Compiled at: 2019-12-17 00:50:39
# Size of source mod 2**32: 1334 bytes
from foxylib.tools.json.json_tool import jdown
from khalalib.chat.chat import KhalaChat

class KhalaPacket:

    class Field:
        CHAT = 'chat'
        CONTRACT = 'contract'

    F = Field

    @classmethod
    def j_chat2j_packet(cls, j_chat):
        j_contract = KhalaContract.j_chat2j_contract(j_chat)
        j = {KhalaPacket.F.CHAT: j_chat, 
         KhalaPacket.F.CONTRACT: j_contract}
        return j

    @classmethod
    def j_packet2jinni_uuid(cls, j_packet):
        return jdown(j_packet, [cls.F.CONTRACT, KhalaContract.F.JINNI_UUID])

    @classmethod
    def j_packet2j_chat(cls, j_packet):
        return jdown(j_packet, [cls.F.CHAT])

    @classmethod
    def j_packet2j_contract(cls, j_packet):
        return jdown(j_packet, [cls.F.CONTRACT])

    @classmethod
    def j_packet2locale(cls, j_packet):
        j_chat = cls.j_packet2j_chat(j_packet)
        locale = KhalaChat.j_chat2locale(j_chat)
        return locale


class KhalaContract:

    class Field:
        ACTION_UUID = 'action_uuid'
        JINNI_UUID = 'jinni_uuid'
        CONFIG = 'config'

    F = Field

    @classmethod
    def j_chat2j_contract(cls, j_chat):
        return {KhalaContract.F.ACTION_UUID: None, 
         KhalaContract.F.CONFIG: '', 
         KhalaContract.F.JINNI_UUID: None}
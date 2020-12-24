# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/messaging/payload_headers.py
# Compiled at: 2019-05-16 09:27:10
from __future__ import absolute_import
from .payload import Payload

class BinMemberAuthenticationPayload(Payload):
    format_list = [
     'varlenH']

    def __init__(self, public_key_bin):
        super(BinMemberAuthenticationPayload, self).__init__()
        self.public_key_bin = public_key_bin

    def to_pack_list(self):
        return [
         (
          'varlenH', self.public_key_bin)]

    @classmethod
    def from_unpack_list(cls, public_key_bin):
        return BinMemberAuthenticationPayload(public_key_bin)


class GlobalTimeDistributionPayload(Payload):
    format_list = [
     'Q']

    def __init__(self, global_time):
        super(GlobalTimeDistributionPayload, self).__init__()
        self.global_time = global_time

    def to_pack_list(self):
        return [
         (
          'Q', self.global_time)]

    @classmethod
    def from_unpack_list(cls, global_time):
        return GlobalTimeDistributionPayload(global_time)
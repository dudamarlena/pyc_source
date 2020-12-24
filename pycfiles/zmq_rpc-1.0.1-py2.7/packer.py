# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zmq_rpc/packer.py
# Compiled at: 2016-12-27 13:29:54
"""Message serialization (messagepack by default).
"""
import msgpack

class Packer(object):

    def pack(self, data):
        return msgpack.packb(data, encoding='utf-8', use_bin_type=True)

    def unpack(self, data):
        return msgpack.unpackb(data, encoding='utf-8', use_list=False)
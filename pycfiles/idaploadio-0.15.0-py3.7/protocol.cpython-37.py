# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/rpc/protocol.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 507 bytes
import msgpack

class Message(object):

    def __init__(self, message_type, data, node_id):
        self.type = message_type
        self.data = data
        self.node_id = node_id

    def __repr__(self):
        return '<Message %s:%s>' % (self.type, self.node_id)

    def serialize(self):
        return msgpack.dumps((self.type, self.data, self.node_id))

    @classmethod
    def unserialize(cls, data):
        msg = cls(*msgpack.loads(data, raw=False, strict_map_key=False))
        return msg
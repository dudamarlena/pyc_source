# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/core/msg.py
# Compiled at: 2015-04-04 17:37:28
from __future__ import absolute_import, unicode_literals
import json
from tornado.escape import to_unicode
import umsgpack

class Msg(object):
    __slots__ = ('message', 'source', 'meta', 'version')

    def __init__(self, message, source, meta=None, version=1):
        self.message = to_unicode(message)
        self.source = to_unicode(source)
        self.meta = meta
        self.version = version

    def __str__(self):
        return self.message

    def update_message(self, message):
        self.message = to_unicode(message)

    def update_meta(self, d):
        if self.meta is None:
            self.meta = {}
        self.meta.update(d)
        return

    def serialize(self):
        return {b'msg': self.message, 
           b'src': self.source, 
           b'meta': self.meta, 
           b'_v': self.version}

    @classmethod
    def deserialize(cls, data):
        return cls(message=data.get(b'msg'), source=data.get(b'src'), meta=data.get(b'meta'), version=data.get(b'_v', 1))

    def serialize_json(self):
        return json.dumps(self.serialize())

    @classmethod
    def deserialize_json(cls, data):
        return cls.deserialize(json.loads(data))

    def serialize_jsonb(self):
        return umsgpack.dumps(self.serialize())

    @classmethod
    def deserialize_jsonb(cls, data):
        return cls.deserialize(umsgpack.loads(data))
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/loup/Workspace/Projects/personal/palmer/palmer/renderers.py
# Compiled at: 2016-10-17 01:51:18
# Size of source mod 2**32: 1951 bytes
from __future__ import unicode_literals
import datetime, decimal, msgpack
from flask.json import dumps as json_dumps

class MessagePackEncoder(object):

    def encode(self, obj):
        if isinstance(obj, datetime.datetime):
            return {'__class__': 'datetime', 'as_str': obj.isoformat()}
        else:
            if isinstance(obj, datetime.date):
                return {'__class__': 'date', 'as_str': obj.isoformat()}
            if isinstance(obj, datetime.time):
                return {'__class__': 'time', 'as_str': obj.isoformat()}
            if isinstance(obj, decimal.Decimal):
                return {'__class__': 'decimal', 'as_str': str(obj)}
            return obj


class BaseRenderer(object):
    __doc__ = '\n    All renderers should extend this class, setting the `media_type`\n    and `format` attributes, and override the `.render()` method.\n    '
    media_type = None
    format = None
    charset = 'utf-8'
    render_style = 'text'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        raise NotImplementedError('Renderer class requires .render() to be implemented')


class JSONRenderer(BaseRenderer):
    __doc__ = '\n    Renderer which serializes to JSON.\n    '
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        return json_dumps(data, ensure_ascii=False)


class MessagePackRenderer(BaseRenderer):
    __doc__ = '\n    Renderer which serializes to MessagePack.\n    '
    media_type = 'application/msgpack'
    format = 'msgpack'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into MessagePack, returning a bytes.
        """
        if data is None:
            return ''
        return msgpack.packb(data, default=MessagePackEncoder().encode)
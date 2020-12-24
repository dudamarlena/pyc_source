# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /hdd/dev/os/aiows/.env/lib/python3.6/site-packages/aiows/aioapp/publisher.py
# Compiled at: 2018-10-09 14:35:39
# Size of source mod 2**32: 1058 bytes
import json

class WSPublisher(object):
    """WSPublisher"""
    TYPE_JSON = 'json'
    TYPE_BYTES = 'bytes'
    TYPE_TEXT = 'text'
    AVAILABLE_TYPES = (
     TYPE_BYTES,
     TYPE_TEXT,
     TYPE_JSON)

    def __init__(self, icid, ws):
        self.icid = icid
        self.ws = ws

    def __str__(self):
        return '<WSPublisher /{}>'.format(self.icid)

    def __repr__(self):
        return str(self)

    async def __call__(self, content, package_type=TYPE_TEXT):
        if package_type not in self.AVAILABLE_TYPES:
            raise TypeError('Can not send undefined WS type.')
        return await getattr(self, 'send_{}'.format(package_type))(content)

    async def send_json(self, data):
        return await self.ws.send_json(json.dumps(data))

    async def send_text(self, data):
        return await self.ws.send_str(data)

    async def send_bytes(self, data):
        return await self.ws.send_bytes(data)
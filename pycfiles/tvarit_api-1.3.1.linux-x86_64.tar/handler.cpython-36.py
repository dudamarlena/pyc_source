# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/resources/handler.py
# Compiled at: 2019-09-30 09:28:30
# Size of source mod 2**32: 1793 bytes
from .base import Base

class Handler(Base):

    def __init__(self, api):
        super(Handler, self).__init__(api)
        self.api = api

    def get_handler_by_id(self, handler_id, brief=False, rdepends=False, resolve=None):
        if type(handler_id) == list:
            handler_id = ','.join([str(m) for m in handler_id])
        params = dict(brief=brief,
          rdepends=rdepends,
          resolve=(resolve or []))
        endpoint = '/handlers/{}'.format(handler_id)
        return self.api.GET(endpoint, params=params)

    def create_handler(self, handler, update_if_exists=False):
        params = dict(update_if_exists=update_if_exists)
        endpoint = '/handlers'
        return self.api.POST(endpoint, json=handler, params=params)

    def update_handler(self, handler_id, handler):
        endpoint = '/handlers/{}'.format(handler_id)
        return self.api.PUT(endpoint, json=handler)

    def upload_handler_json(self, handlers, strict=False):
        params = dict(strict=strict)
        endpoint = '/handlers/json'
        return self.api.POST(endpoint, json=handlers, params=params)

    def list_handlers(self, detail=False, rdepends=False, resolve=None, limit=100, page=0):
        params = dict(detail=detail,
          rdepends=rdepends,
          resolve=(resolve or []),
          limit=limit,
          page=page)
        endpoint = '/handlers'
        return self.api.GET(endpoint, params=params)

    def delete_handler_by_id(self, handler_id):
        if type(handler_id) == list:
            handler_id = ','.join([str(m) for m in handler_id])
        endpoint = '/handlers/{}'.format(handler_id)
        return self.api.DELETE(endpoint)
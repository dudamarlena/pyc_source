# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/doumail.py
# Compiled at: 2013-12-18 08:08:58
from .base import DoubanAPIBase, DEFAULT_START, DEFAULT_COUNT

class Doumail(DoubanAPIBase):

    def __repr__(self):
        return '<DoubanAPI Doumail>'

    def get(self, id):
        return self._get('/v2/doumail/%s' % id)

    def inbox(self, start=DEFAULT_START, count=DEFAULT_COUNT):
        return self._get('/v2/doumail/inbox', start=start, count=count)

    def outbox(self, start=DEFAULT_START, count=DEFAULT_COUNT):
        return self._get('/v2/doumail/outbox', start=start, count=count)

    def unread(self, start=DEFAULT_START, count=DEFAULT_COUNT):
        return self._get('/v2/doumail/inbox/unread', start=start, count=count)

    def read(self, id):
        return self._put('/v2/doumail/%s' % id, key='key')

    def reads(self, ids):
        if isinstance(ids, (list, tuple)):
            ids = (',').join(ids)
        return self._put('/v2/doumail/read', ids=ids)

    def delete(self, id):
        return self._delete('/v2/doumail/%s' % id)

    def deletes(self, ids):
        if isinstance(ids, (tuple, list)):
            ids = (',').join(ids)
        return self._post('/v2/doumail/delete', ids=ids)

    def new(self, title, content, receiver_id, captcha_token=None, captcha_string=None):
        return self._post('/v2/doumails', title=title, content=content, receiver_id=receiver_id, captcha_toke=captcha_token, captcha_string=captcha_string)
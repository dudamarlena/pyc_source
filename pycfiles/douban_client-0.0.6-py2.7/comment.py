# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/comment.py
# Compiled at: 2013-12-18 08:08:58
from .base import DoubanAPIBase, DEFAULT_START, DEFAULT_COUNT

class Comment(DoubanAPIBase):

    def __init__(self, access_token, target):
        self.access_token = access_token
        self.target = target

    def __repr__(self):
        return '<DoubanAPI Comment>'

    def list(self, target_id, start=DEFAULT_START, count=DEFAULT_COUNT):
        return self._get('/v2/%s/%s/comments' % (self.target, target_id), start=start, count=count)

    def new(self, target_id, content):
        return self._post('/v2/%s/%s/comments' % (self.target, target_id), content=content)

    def get(self, target_id, id):
        return self._get('/v2/%s/%s/comment/%s' % (self.target, target_id, id))

    def delete(self, target_id, id):
        return self._delete('/v2/%s/%s/comment/%s' % (self.target, target_id, id))
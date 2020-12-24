# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/user.py
# Compiled at: 2013-12-18 08:08:58
from .base import DoubanAPIBase, DEFAULT_START, DEFAULT_COUNT

class User(DoubanAPIBase):

    def __repr__(self):
        return '<DoubanAPI User>'

    def get(self, id):
        return self._get('/v2/user/%s' % id)

    @property
    def me(self):
        return self.get('~me')

    def search(self, q, start=DEFAULT_START, count=DEFAULT_COUNT):
        return self._get('/v2/user', q=q, start=start, count=count)

    def follow(self, id):
        return self._post('/shuo/v2/friendships/create', user_id=id)

    def unfollow(self, id):
        return self._post('/shuo/v2/friendships/destroy', user_id=id)

    def following(self, id, start=DEFAULT_START, count=DEFAULT_COUNT):
        page = start / count
        return self._get('/shuo/v2/users/%s/following' % id, page=page, count=count)

    def followers(self, id, start=DEFAULT_START, count=DEFAULT_COUNT):
        page = start / count
        return self._get('/shuo/v2/users/%s/followers' % id, page=page, count=count)
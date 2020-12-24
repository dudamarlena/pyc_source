# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/photo.py
# Compiled at: 2013-12-18 08:08:58
from .base import DoubanAPIBase, DEFAULT_START, DEFAULT_COUNT
from .comment import Comment

class Photo(DoubanAPIBase):
    target = 'photo'

    def __repr__(self):
        return '<DoubanAPI Photo>'

    def get(self, id):
        return self._get('/v2/photo/%s' % id)

    def new(self, album_id, image, desc=''):
        return self._post('/v2/album/%s' % album_id, desc=desc, files={'image': image})

    def update(self, id, desc):
        return self._put('/v2/photo/%s' % id, desc=desc)

    def delete(self, id):
        return self._delete('/v2/photo/%s' % id)

    def like(self, id):
        return self._post('/v2/photo/%s/like' % id)

    def unlike(self, id):
        return self._delete('/v2/photo/%s/like' % id)

    def comments(self, id, start=DEFAULT_START, count=DEFAULT_COUNT):
        return Comment(self.access_token, self.target).list(id, start=start, count=count)

    @property
    def comment(self):
        return Comment(self.access_token, self.target)
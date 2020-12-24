# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/discussion.py
# Compiled at: 2013-12-18 08:08:58
from .base import DoubanAPIBase, DEFAULT_START, DEFAULT_COUNT
from .comment import Comment

class Discussion(DoubanAPIBase):
    target = 'discussion'

    def __repr__(self):
        return '<DoubanAPI Discussion>'

    def get(self, id):
        return self._get('/v2/discussion/%s' % id)

    def new(self, target, target_id, title, content):
        return self._post('/v2/%s/%s/discussions' % (target, target_id), title=title, content=content)

    def list(self, target, target_id, start=DEFAULT_START, count=DEFAULT_COUNT):
        return self._get('/v2/%s/%s/discussions' % (target, target_id), start=start, count=count)

    def update(self, id, title, content):
        return self._put('/v2/discussion/%s' % id, title=title, content=content)

    def delete(self, id):
        return self._delete('/v2/discussion/%s' % id)

    def comments(self, id, start=DEFAULT_START, count=DEFAULT_COUNT):
        return Comment(self.access_token, self.target).list(id, start=start, count=count)

    @property
    def comment(self):
        return Comment(self.access_token, self.target)
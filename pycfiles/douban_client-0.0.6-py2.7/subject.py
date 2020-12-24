# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/subject.py
# Compiled at: 2013-12-18 08:08:58
from .base import DoubanAPIBase, DEFAULT_START, DEFAULT_COUNT
from .review import Review

class Subject(DoubanAPIBase):
    target = None

    def get(self, id):
        return self._get('/v2/%s/%s' % (self.target, id))

    def search(self, q='', tag='', start=DEFAULT_START, count=DEFAULT_COUNT):
        return self._get('/v2/%s/search' % self.target, q=q, tag=tag, start=start, count=count)

    def tags(self, id):
        return self._get('/v2/%s/%s/tags' % (self.target, id))

    def tagged_list(self, id):
        return self._get('/v2/%s/user_tags/%s' % (self.target, id))

    @property
    def review(self):
        return Review(self.access_token, self.target)
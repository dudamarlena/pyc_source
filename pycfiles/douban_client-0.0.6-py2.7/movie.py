# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/movie.py
# Compiled at: 2013-12-18 08:10:18
from .subject import Subject

class Movie(Subject):
    target = 'movie'

    def __repr__(self):
        return '<DoubanAPI Movie>'

    def celebrity(self, celebrity_id):
        return self._get('/v2/movie/celebrity/%s' % celebrity_id)

    def imdb(self, imdb_id):
        return self._get('/v2/movie/imdb/%s' % imdb_id)
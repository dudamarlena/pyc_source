# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/tests/test_api_movie.py
# Compiled at: 2013-12-18 08:08:21
from uuid import uuid4
from framework import DoubanClientTestBase, main

class TestApiMovie(DoubanClientTestBase):

    def setUp(self):
        super(TestApiMovie, self).setUp()
        self.user_id = '40774605'
        self.movie_id = '1296357'
        self.review_id = '5565362'
        self.imdb = 'tt1345836'
        self.celebrity_id = '1053585'

    def test_get_movie(self):
        ret = self.client.movie.get(self.movie_id)
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue('author' in ret)
        self.assertTrue('title' in ret)
        self.assertTrue('summary' in ret)

    def test_get_celebrity(self):
        ret = self.client.movie.celebrity(self.celebrity_id)
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue('name' in ret)
        self.assertTrue('avatars' in ret)
        self.assertTrue('works' in ret)

    def test_get_movie_by_imdb(self):
        ret = self.client.movie.imdb(self.imdb)
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue('author' in ret)
        self.assertTrue('title' in ret)
        self.assertTrue('summary' in ret)

    def test_search_movie(self):
        ret = self.client.movie.search('蝙蝠侠')
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue(isinstance(ret['subjects'], list))
        self.assertTrue('start' in ret)
        self.assertTrue('count' in ret)
        self.assertTrue('total' in ret)

    def test_movie_tags(self):
        ret = self.client.movie.tags(self.movie_id)
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue(isinstance(ret['tags'], list))
        self.assertTrue('start' in ret)
        self.assertTrue('count' in ret)
        self.assertTrue('total' in ret)

    def test_get_movie_tagged_list(self):
        ret = self.client.movie.tagged_list('40774605')
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue(isinstance(ret['tags'], list))
        self.assertTrue('start' in ret)
        self.assertTrue('count' in ret)
        self.assertTrue('total' in ret)

    def test_new_update_delete_review(self):
        title = content = uuid4().hex
        content = content * 10
        ret = self.client.movie.review.new(self.movie_id, title, content)
        self.assertTrue(isinstance(ret, dict))
        self.assertEqual(content, ret['content'])
        self.assertTrue('author' in ret)
        review_id = ret['id']
        content = content * 2
        ret = self.client.movie.review.update(review_id, title, content)
        self.assertEqual(content, ret['content'])
        ret = self.client.movie.review.delete(review_id)
        self.assertEqual('OK', ret)


if __name__ == '__main__':
    main()
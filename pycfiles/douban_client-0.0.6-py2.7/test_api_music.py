# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/tests/test_api_music.py
# Compiled at: 2013-12-18 08:08:21
from uuid import uuid4
from framework import DoubanClientTestBase, main

class TestApiMusic(DoubanClientTestBase):

    def setUp(self):
        super(TestApiMusic, self).setUp()
        self.user_id = '40774605'
        self.music_id = '1419262'
        self.review_id = '5572975'

    def test_get_music(self):
        ret = self.client.music.get(self.music_id)
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue('author' in ret)
        self.assertTrue('title' in ret)
        self.assertTrue('summary' in ret)

    def test_search_music(self):
        ret = self.client.music.search('坦白')
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue(isinstance(ret['musics'], list))
        self.assertTrue('start' in ret)
        self.assertTrue('count' in ret)
        self.assertTrue('total' in ret)

    def test_music_tags(self):
        ret = self.client.music.tags(self.music_id)
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue(isinstance(ret['tags'], list))
        self.assertTrue('start' in ret)
        self.assertTrue('count' in ret)
        self.assertTrue('total' in ret)

    def test_get_music_tagged_list(self):
        ret = self.client.music.tagged_list('40774605')
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue(isinstance(ret['tags'], list))
        self.assertTrue('start' in ret)
        self.assertTrue('count' in ret)
        self.assertTrue('total' in ret)

    def test_new_update_delete_review(self):
        title = content = uuid4().hex
        content = content * 10
        ret = self.client.music.review.new(self.music_id, title, content)
        self.assertTrue(isinstance(ret, dict))
        self.assertEqual(content, ret['content'])
        self.assertTrue('author' in ret)
        review_id = ret['id']
        content = content * 2
        ret = self.client.music.review.update(review_id, title, content)
        self.assertEqual(content, ret['content'])
        ret = self.client.music.review.delete(review_id)
        self.assertEqual('OK', ret)


if __name__ == '__main__':
    main()
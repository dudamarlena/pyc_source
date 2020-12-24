# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/tests/test_api_user.py
# Compiled at: 2013-12-18 08:08:21
from framework import DoubanClientTestBase, main

class TestApiUser(DoubanClientTestBase):

    def setUp(self):
        super(TestApiUser, self).setUp()
        self.user_id = '70920446'

    def test_get_user(self):
        ret = self.client.user.get('liluoliluo')
        self.assertEqual(ret['uid'], 'liluoliluo')

    def test_get_me(self):
        ret = self.client.user.me
        self.assertTrue('id' in ret)

    def test_search(self):
        q = '落'
        ret = self.client.user.search(q)
        self.assertTrue('start' in ret)
        self.assertTrue('count' in ret)
        self.assertTrue('total' in ret)

    def test_follow(self):
        ret = self.client.user.follow(self.user_id)
        self.assertTrue(ret['following'])

    def test_unfollow(self):
        self.client.user.follow(self.user_id)
        ret = self.client.user.unfollow(self.user_id)
        self.assertFalse(ret['following'])
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue('uid' in ret)

    def test_followers(self):
        ret = self.client.user.followers(self.user_id)
        self.assertTrue(isinstance(ret, list))
        self.assertTrue(all([ 'uid' in r for r in ret ]))


if __name__ == '__main__':
    main()
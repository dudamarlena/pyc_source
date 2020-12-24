# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/paparent/projects/pyforrst/tests/test.py
# Compiled at: 2010-09-19 16:01:17
__doc__ = '\nMinimal Unit Tests for Forrst API\n'
import unittest, pyforrst
TEST_USERNAME = 'kyle'
TEST_USERID = '1'
TEST_INVALID_USER = 'INVALIDUSER123'

class TestUserInfo(unittest.TestCase):
    """
    Test the user_info API function
    """

    def _verify_test_user(self, user):
        """
        Helper method for verifying user data against test user as defined by
        TEST_USERNAME and TEST_USERID
        """
        self.assertTrue('username' in user, 'Username key not in return value')
        self.assertTrue('id' in user, 'ID key not in return value')
        self.assertEqual(user['username'], TEST_USERNAME, "Username requested: '%s' returned: '%s'" % (
         TEST_USERNAME, user['username']))
        self.assertEqual(user['id'], TEST_USERID, 'User ID requested: %s returned: %s' % (
         TEST_USERID, user['id']))

    def test_user_info_success(self):
        """
        Verify that user_info() returns correct data with valid username
        """
        self._verify_test_user(pyforrst.user_info(TEST_USERNAME))

    def test_user_info_invalid_username(self):
        """
        Verify that user_info() returns an error when given invalid user
        """
        self.assertRaises(pyforrst.ForrstError, pyforrst.user_info, TEST_INVALID_USER)

    def test_user_info_id_success(self):
        """
        Verify that user_info_by_id() returns correct data with valid user id
        """
        self._verify_test_user(pyforrst.user_info_by_id(int(TEST_USERID)))

    def test_user_info_id_invalid_id(self):
        """
        Verify that user_info_by_id() returns an error when given invalid id
        """
        self.assertRaises(pyforrst.ForrstError, pyforrst.user_info_by_id, -1)


class TestUserPosts(unittest.TestCase):
    """
    Test user_posts API function
    """

    def _verify_posts_from_user(self, user, posts):
        """
        Helper method to verify posts for given user
        """
        for post in posts:
            self.assertTrue('id' in post, 'ID key missing from posts')
            self.assertTrue('content' in post, 'Content key missing from post')
            self.assertTrue('user_id' in post, 'User ID key missing from post')
            self.assertEqual(post['user_id'], TEST_USERID, "Post's User ID: %s doesn't match requested: %s" % (
             post['user_id'], TEST_USERID))

    def test_user_posts_success(self):
        """
        Verify user_posts returns correct data for valid user
        """
        self._verify_posts_from_user(TEST_USERNAME, pyforrst.user_posts(TEST_USERNAME))

    def test_user_posts_since_success(self):
        """
        Verify user_posts returns correct data for valid user and since param
        """
        since_id = 1000000
        posts = pyforrst.user_posts(TEST_USERNAME, since_id)
        self._verify_posts_from_user(TEST_USERNAME, posts)
        for post in posts:
            post_id = int(post['id'])
            self.assertTrue(post_id < since_id, 'Post ID: %d not less than since_id: %d' % (
             post_id, since_id))

    def test_user_posts_zero_posts_since(self):
        """
        Verify user_posts returns no posts for given a since_id that doesn't
        have any predecessors (-1)
        """
        self.assertEqual(0, len(pyforrst.user_posts(TEST_USERNAME, -1)))

    def test_user_posts_invalid_since(self):
        """
        Verify user_posts returns error when given invalid since id
        """
        self.assertRaises(pyforrst.ForrstError, pyforrst.user_posts, TEST_USERNAME, 'notanumber')

    def test_user_posts_invalid_user(self):
        """
        Verify user_posts returns error when given invalid username
        """
        self.assertRaises(pyforrst.ForrstError, pyforrst.user_posts, TEST_INVALID_USER)


if __name__ == '__main__':
    unittest.main()
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\prboard\tests\unit\test_hub.py
# Compiled at: 2016-04-23 12:57:02
import unittest, mock, github
from github import Requester
from prboard import utils, filters, settings, hub

class TestGithub(unittest.TestCase):

    def setUp(self):
        pass

    def test_github_init(self):
        """ Test if Github gets instantiated with addditional methods """
        g = hub.Github()
        self.assertTrue(hasattr(g, 'get_user_repos'))
        self.assertTrue(hasattr(g, 'get_org_repos'))

    @mock.patch.object(github.PaginatedList, 'PaginatedList')
    def test_github_get_user_repos_raises_assert_error(self, mock_paginated_list):
        """ Test if Github.get_user_repos raises assertion error if since is not a valid value """
        g = hub.Github()
        with self.assertRaises(AssertionError):
            g.get_user_repos('kumar', 'a')

    @mock.patch.object(github.PaginatedList, 'PaginatedList')
    def test_github_get_user_repos_pass(self, mock_paginated_list):
        """ Test if Github.get_user_repos raises assertion error if since is not a valid value """
        args = [
         mock.MagicMock(), '', '', '']
        data = [github.Repository.Repository(*args), github.Repository.Repository(*args), github.Repository.Repository(*args)]
        mock_paginated_list.return_value = data
        g = hub.Github()
        repos = g.get_user_repos('kumar')
        self.assertEqual(mock_paginated_list.call_args[0][0], github.Repository.Repository)
        self.assertEqual(mock_paginated_list.call_args[0][2], ('/users/{}/repos').format('kumar'))
        self.assertEqual(repos, data)

    @mock.patch.object(github.PaginatedList, 'PaginatedList')
    def test_github_get_org_repos_pass(self, mock_paginated_list):
        """ Test if Github.get_org_repos raises assertion error if since is not a valid value """
        args = [
         mock.MagicMock(), '', '', '']
        data = [github.Repository.Repository(*args), github.Repository.Repository(*args), github.Repository.Repository(*args)]
        mock_paginated_list.return_value = data
        g = hub.Github()
        repos = g.get_org_repos('kumar')
        self.assertEqual(mock_paginated_list.call_args[0][0], github.Repository.Repository)
        self.assertEqual(mock_paginated_list.call_args[0][2], ('orgs/{}/repositories').format('kumar'))
        self.assertEqual(repos, data)
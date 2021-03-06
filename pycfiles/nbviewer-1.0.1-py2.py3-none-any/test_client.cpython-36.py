# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/nbviewer/nbviewer/providers/github/tests/test_client.py
# Compiled at: 2016-10-24 14:40:21
# Size of source mod 2**32: 3901 bytes
import mock
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase
from ..client import AsyncGitHubClient
from ....utils import quote

class GithubClientTest(AsyncTestCase):
    __doc__ = 'Tests that the github API client makes the correct http requests.'

    def setUp(self):
        super(GithubClientTest, self).setUp()
        self.http_client = mock.create_autospec(AsyncHTTPClient)
        with mock.patch('os.environ.get', return_value='https://api.github.com/'):
            self.gh_client = AsyncGitHubClient(client=(self.http_client))

    def _get_url(self):
        """Get the last url requested from the mock http client."""
        args, kw = self.http_client.fetch.call_args
        return args[0]

    def assertStartsWith(self, string, beginning):
        """Assert that a url has the correct beginning.
        
        Github API requests involve non-trivial query strings.  This is useful
        when you want to compare URLs, but don't care about the querystring.
        """
        if string.startswith(beginning):
            return
        self.assertTrue(string.startswith(beginning), '%s does not start with %s' % (string, beginning))

    def test_basic_fetch(self):
        """Test the mock http client is hit"""
        self.gh_client.fetch('https://api.github.com/url')
        self.assertTrue(self.http_client.fetch.called)

    def test_fetch_params(self):
        """Test params are passed through."""
        params = {'unique_param_name': 1}
        self.gh_client.fetch('https://api.github.com/url', params=params)
        url = self._get_url()
        self.assertTrue('unique_param_name' in url)

    def test_log_rate_limit(self):
        pass

    def test_get_repos(self):
        self.gh_client.get_repos('username')
        url = self._get_url()
        self.assertStartsWith(url, 'https://api.github.com/users/username/repos')

    def test_get_contents(self):
        user = 'username'
        repo = 'my_awesome_repo'
        path = 'möre-path'
        self.gh_client.get_contents(user, repo, path)
        url = self._get_url()
        correct_url = 'https://api.github.com' + quote('/repos/username/my_awesome_repo/contents/möre-path')
        self.assertStartsWith(url, correct_url)

    def test_get_branches(self):
        user = 'username'
        repo = 'my_awesome_repo'
        self.gh_client.get_branches(user, repo)
        url = self._get_url()
        correct_url = 'https://api.github.com/repos/username/my_awesome_repo/branches'
        self.assertStartsWith(url, correct_url)

    def test_get_tags(self):
        user = 'username'
        repo = 'my_awesome_repo'
        self.gh_client.get_tags(user, repo)
        url = self._get_url()
        correct_url = 'https://api.github.com/repos/username/my_awesome_repo/tags'
        self.assertStartsWith(url, correct_url)

    def test_get_tree_entry(self):
        user = 'username'
        repo = 'my_awesome_repo'
        path = 'extra-path'
        self.gh_client.get_tree_entry(user, repo, path)
        url = self._get_url()
        correct_url = 'https://api.github.com/repos/username/my_awesome_repo/git/trees/master'
        self.assertStartsWith(url, correct_url)

    def test_get_gist(self):
        gist_id = 'ap90avn23iovv2ovn2309n'
        self.gh_client.get_gist(gist_id)
        url = self._get_url()
        correct_url = 'https://api.github.com/gists/' + gist_id
        self.assertStartsWith(url, correct_url)

    def test_get_gists(self):
        user = 'username'
        self.gh_client.get_gists(user)
        url = self._get_url()
        correct_url = 'https://api.github.com/users/username/gists'
        self.assertStartsWith(url, correct_url)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbintegrations/travisci/api.py
# Compiled at: 2020-01-07 04:31:42
"""Utilities for interacting with the Travis CI API."""
from __future__ import unicode_literals
import logging, json
from django.utils.http import urlquote_plus
from django.utils.six.moves.urllib.request import urlopen
from django.utils.translation import ugettext_lazy as _
from rbintegrations.util.urlrequest import URLRequest
logger = logging.getLogger(__name__)

class TravisAPI(object):
    """Object for interacting with the Travis CI API."""
    OPEN_SOURCE_ENDPOINT = b'O'
    PRIVATE_PROJECT_ENDPOINT = b'P'
    ENTERPRISE_ENDPOINT = b'E'
    ENDPOINT_CHOICES = (
     (
      OPEN_SOURCE_ENDPOINT, _(b'Open Source (travis-ci.org)')),
     (
      PRIVATE_PROJECT_ENDPOINT, _(b'Private Projects (travis-ci.com)')),
     (
      ENTERPRISE_ENDPOINT, _(b'Enterprise (custom domain)')))
    OPEN_SOURCE_ENDPOINT_URL = b'https://api.travis-ci.org'
    PRIVATE_PROJECT_ENDPOINT_URL = b'https://api.travis-ci.com'

    def __init__(self, config):
        """Initialize the object.

        Args:
            config (dict):
                The integration config to use.

        Raises:
            ValueError:
                The provided endpoint type was not valid.
        """
        endpoint = config.get(b'travis_endpoint')
        if endpoint == self.OPEN_SOURCE_ENDPOINT:
            self.endpoint = self.OPEN_SOURCE_ENDPOINT_URL
        elif endpoint == self.PRIVATE_PROJECT_ENDPOINT:
            self.endpoint = self.PRIVATE_PROJECT_ENDPOINT_URL
        elif endpoint == self.ENTERPRISE_ENDPOINT:
            custom_endpoint = config.get(b'travis_custom_endpoint')
            if custom_endpoint.endswith(b'/'):
                custom_endpoint = custom_endpoint[:-1]
            self.endpoint = b'%s/api' % custom_endpoint
        else:
            raise ValueError(b'Unexpected value for Travis CI endpoint: %s' % endpoint)
        self.token = config.get(b'travis_ci_token')

    def lint(self, travis_yml):
        """Lint a prospective travis.yml file.

        Args:
            travis_yml (unicode):
                The contents of the travis.yml file to validate.

        Returns:
            dict:
            The parsed contents of the JSON response.

        Raises:
            urllib2.URLError:
                The HTTP request failed.

            Exception:
                Some other exception occurred when trying to parse the results.
        """
        data = self._make_request(b'%s/lint' % self.endpoint, body=travis_yml, method=b'POST', content_type=b'text/yaml')
        return json.loads(data)

    def get_config(self):
        """Return the Travis CI server's config.

        Returns:
            dict:
            The parsed contents of the JSON response.

        Raises:
            urllib2.URLError:
                The HTTP request failed.
        """
        u = urlopen(URLRequest(b'%s/config' % self.endpoint))
        return json.loads(u.read())

    def get_user(self):
        """Return the Travis CI user.

        Returns:
            dict:
            The parsed contents of the JSON response.

        Raises:
            urllib2.URLError:
                The HTTP request failed.
        """
        data = self._make_request(b'%s/user' % self.endpoint)
        return json.loads(data)

    def start_build(self, repo_slug, travis_config, commit_message, branch=None):
        """Start a build.

        Args:
            repo_slug (unicode):
                The "slug" for the repository based on it's location on GitHub.

            travis_config (unicode):
                The contents of the travis config to use when doing the build.

            commit_message (unicode):
                The text to use as the commit message displayed in the Travis
                UI.

            branch (unicode, optional):
                The branch name to use.

        Returns:
            dict:
            The parsed contents of the JSON response.

        Raises:
            urllib2.URLError:
                The HTTP request failed.
        """
        travis_config[b'merge_mode'] = b'replace'
        request_data = {b'request': {b'message': commit_message, 
                        b'config': travis_config}}
        if branch:
            request_data[b'request'][b'branch'] = branch
        data = self._make_request(b'%s/repo/%s/requests' % (self.endpoint,
         urlquote_plus(repo_slug)), body=json.dumps(request_data), method=b'POST', content_type=b'application/json')
        return json.loads(data)

    def _make_request(self, url, body=None, method=b'GET', content_type=b'application/json'):
        """Make an HTTP request.

        Args:
            url (unicode):
                The URL to make the request against.

            body (unicode or bytes, optional):
                The content of the request.

            method (unicode, optional):
                The request method. If not provided, it defaults to a ``GET``
                request.

            content_type (unicode, optional):
                The type of the content being POSTed.

        Returns:
            bytes:
            The contents of the HTTP response body.

        Raises:
            urllib2.URLError:
                The HTTP request failed.
        """
        logger.debug(b'Making request to Travis CI %s', url)
        headers = {b'Accept': b'application/json', 
           b'Authorization': b'token %s' % self.token, 
           b'Travis-API-Version': b'3'}
        if content_type:
            headers[b'Content-Type'] = content_type
        request = URLRequest(url, body=body, method=method, headers=headers)
        u = urlopen(request)
        return u.read()
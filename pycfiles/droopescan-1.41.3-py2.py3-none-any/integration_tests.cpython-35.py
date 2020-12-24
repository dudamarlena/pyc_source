# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/tests/integration_tests.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 5181 bytes
from __future__ import print_function
from cement.utils import test
from dscan.common.testutils import decallmethods
from dscan.tests import BaseTest, MockHash
from mock import MagicMock
from requests.exceptions import ConnectionError
import dscan, json, re, responses, sys
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

class MultiMockHash:
    __doc__ = '\n        Like MockHash, but works for multisites.\n    '
    files = None

    def mock_func(self, *args, **kwargs):
        file_url = kwargs['file_url']
        version = _vfu(args[0])
        return self.files[version][file_url]


def _vfu(url):
    """
        Parse the version from a URL.
        @param url e.g. http://localhost/3.2.1/asd.txt
        @return e.g. 3.2.1
    """
    up = urlparse(url)
    version = up.path.split('/')[1]
    return version


class Capture(list):

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


@decallmethods(responses.activate)
class IntegrationTests(BaseTest):
    __doc__ = '\n        End-to-end tests for droopescan. These should not make any external\n        requests.\n    '

    def setUp(self):
        super(IntegrationTests, self).setUp()

    def _mock_output_pl(self, line):
        """
            Parse a single line of output.
            @param line
            @return (verb, url, status_code, hash)
                - verb will be uppercase e.g. HEAD
                - status_code will be integer.
        """
        splat = line.split(' ')
        verb = splat[0][1:-1].upper()
        url = splat[1]
        status_code = int(splat[2].strip())
        hash = splat[3].strip()
        return (
         verb, url, status_code, hash)

    def _unhandled_cb(self, request):
        error = "Unhandled request to '%s' (%s)." % (request.url, request.method)
        print(error, file=sys.stderr)
        return (404, {}, '')

    def mock_output(self, source, base_urls=None):
        """
            Mocks many responses, taking a "output_" file as a base. This is
            used for end-to-end tests.

            @param source the file to read from. e.g. tests/resources/output_drupal.txt
            @param base_urls a list of base_urls used for getting relative
                paths.
            @return MagicMock a magic mock which can be used to replace
                Drupal.enumerate_file_hash, for example.
        """
        files = {}
        with open(dscan.PWD + source, 'r') as (f):
            for line in f:
                verb, url, status_code, hash = self._mock_output_pl(line)
                if hash != '':
                    path = None
                    version = _vfu(url)
                    for base_url in base_urls:
                        if base_url in url:
                            path = url.replace(base_url, '')

                    if not path:
                        assert False
                        if version not in files:
                            files[version] = {}
                        files[version][path] = hash
                    responses.add(verb, url, status=status_code)

        default_response = re.compile('.')
        responses.add_callback(responses.GET, default_response, callback=self._unhandled_cb)
        responses.add_callback(responses.HEAD, default_response, callback=self._unhandled_cb)
        responses.add_callback(responses.POST, default_response, callback=self._unhandled_cb)
        mock_hash = MultiMockHash()
        mock_hash.files = files
        mock = MagicMock(side_effect=mock_hash.mock_func)
        return mock

    def test_integration_drupal(self):
        self.mock_output('tests/resources/output_drupal.txt')
        self.add_argv(['scan', 'drupal', '-u', self.base_url, '-n', '100', '-o',
         'json'])
        with Capture() as (out):
            self.app.run()
        json_raw = out[0]
        try:
            j = json.loads(json_raw)
        except:
            print(json_raw)
            raise

        assert len(j['interesting urls']['finds']) == 2
        assert len(j['plugins']['finds']) == 17
        assert len(j['themes']['finds']) == 0

    def test_ss_multisite(self):
        output_file = 'tests/resources/output_ss_multisite.txt'
        url_file = 'dscan/tests/resources/url_file_ss_multisite.txt'
        with open(url_file) as (f):
            base_urls = [line.strip() for line in f]
        enumerate_mock = self.mock_output(output_file, base_urls)
        self.mock_controller('silverstripe', 'enumerate_file_hash', mock=enumerate_mock)
        self.add_argv(['scan', 'ss', '-U', url_file, '-e', 'v'])
        with Capture() as (out):
            self.app.run()
        for line in out:
            j = json.loads(line)
            real_version = _vfu(j['host'])
            print(real_version, j['version']['finds'])
            if not real_version in j['version']['finds']:
                raise AssertionError
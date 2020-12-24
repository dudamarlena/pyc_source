# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/scaleway/tests/apis/test_api_metadata.py
# Compiled at: 2019-12-16 08:49:55
import json, unittest, uuid
from scaleway.apis import MetadataAPI
from six.moves.urllib.parse import parse_qs, urlparse
from . import FakeAPITestCase

class TestMetadataAPI(FakeAPITestCase, unittest.TestCase):

    def setUp(self):
        super(TestMetadataAPI, self).setUp()
        self.api = MetadataAPI()

    def make_fake_metadata_api(self):
        """ Fakes the Metadata API.
        """
        json_response = {'id': str(uuid.uuid4()), 
           'name': 'super name'}

        def fake_route_conf(_, uri, headers):
            """ Fakes the /conf route.

            Returns metadata of a running server. Our tests don't need to have
            all the metadata of a server, so only a few values are returned.

            If ?format=json is set, return a JSON dict with a application/json
            content
            type.

            If no format is given, return a text/plain response with a "shell"
            format.
            """
            querystring = parse_qs(urlparse(uri).query)
            if 'json' in querystring.get('format', []):
                return (200, headers, json.dumps(json_response))
            headers['content-type'] = 'text/plain'
            return (200, headers,
             ('\n').join('%s="%s"' % (key, value) for key, value in json_response.items()))

        self.fake_endpoint(self.api, 'conf/', body=fake_route_conf)
        return json_response

    def test_get(self):
        expected_response = self.make_fake_metadata_api()
        self.assertEqual(self.api.get_metadata(), expected_response)
        shell_response = self.api.get_metadata(as_shell=True)
        self.assertIn('id="%(id)s"' % expected_response, shell_response.decode('utf8'))
        self.assertIn('name="%(name)s"' % expected_response, shell_response.decode('utf8'))
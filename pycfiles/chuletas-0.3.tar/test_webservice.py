# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/test_webservice.py
# Compiled at: 2011-06-17 01:36:21
import cPickle, unittest
from chula import collection, error, config, json, webservice
from chula.www.adapters import env

class Test_webservice(unittest.TestCase):
    doctest = webservice

    def setUp(self):
        self.env = env.BaseEnv()
        self.env.form = {}
        self.env.form_get = {}
        self.env.form_post = {}
        self.controller = collection.Collection()
        self.controller.env = self.env
        self.controller.config = config.Config()
        self.payload = {'name': 'Test User', 'cars': ['honda', 'audi']}
        self.transport = webservice.Transport(self.controller)
        self.transport.data = self.payload

    def test_expose_default(self):

        @webservice.expose()
        def helper(foo):
            return self.payload

        response = json.decode(helper(self.controller))
        self.assertEquals(response['data'], self.payload)
        self.assertEquals(response['success'], True)

    def test_expose_ascii_via_get(self):
        self.controller.env.form['transport'] = 'ascii'
        self.payload = 'foo,bar,bla'
        self.transport.data = self.payload

        @webservice.expose()
        def helper(foo):
            return self.payload

        response = helper(self.controller)
        self.assertEquals(response, self.payload)

    def test_expose_ascii_via_kwargs(self):
        self.payload = 'foo,bar,bla'
        self.transport.data = self.payload

        @webservice.expose(transport='ascii')
        def helper(foo):
            return self.payload

        response = helper(self.controller)
        self.assertEquals(response, self.payload)

    def test_expose_json_via_get(self):
        self.controller.env.form['transport'] = 'json'

        @webservice.expose()
        def helper(foo):
            return self.payload

        response = json.decode(helper(self.controller))
        self.assertEquals(response['data'], self.payload)
        self.assertEquals(response['success'], True)

    def test_expose_json_via_kwargs(self):

        @webservice.expose(transport='json')
        def helper(foo):
            return self.payload

        response = json.decode(helper(self.controller))
        self.assertEquals(response['data'], self.payload)
        self.assertEquals(response['success'], True)

    def test_expose_json_via_x_header(self):

        @webservice.expose(x_header=True)
        def helper(foo):
            return self.payload

        HEADER_FOUND = False
        html_body = helper(self.controller)
        for header in self.controller.env.headers:
            if header[0] == 'X-JSON':
                HEADER_FOUND = True
                response = json.decode(header[1])
                break

        self.assertEquals(HEADER_FOUND, True)
        self.assertEquals(response['data'], self.payload)
        self.assertEquals(response['success'], True)

    def test_expose_pickle_via_get(self):
        self.controller.env.form['transport'] = 'pickle'

        @webservice.expose()
        def helper(foo):
            return self.payload

        response = cPickle.loads(helper(self.controller))
        self.assertEquals(response['data'], self.payload)
        self.assertEquals(response['success'], True)

    def test_expose_pickle(self):

        @webservice.expose(transport='pickle')
        def helper(foo):
            return self.payload

        response = cPickle.loads(helper(self.controller))
        self.assertEquals(response['data'], self.payload)
        self.assertEquals(response['success'], True)

    def test_unkown_transport(self):

        @webservice.expose(transport='xml')
        def helper(foo):
            return self.payload

        exception = error.WebserviceUnknownTransportError
        self.assertRaises(exception, helper, self.controller)
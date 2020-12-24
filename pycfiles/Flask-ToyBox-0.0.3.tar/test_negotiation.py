# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/drdaeman/Development/flask-toybox/tests/test_negotiation.py
# Compiled at: 2012-11-07 15:23:06
import unittest
from flask.ext.toybox.views import NegotiatingMethodView
from flask.ext.toybox import ToyBox
from flask import Flask, request
import json

class EchoView(NegotiatingMethodView):

    def get(self):
        """Echoes back a list of GET query param pairs."""
        return request.args.items()

    def post(self):
        """Echoes back a received body."""
        return request.decoded_data


class NegotiationTestCase(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        toybox = ToyBox(app)
        app.add_url_rule('/echo', view_func=EchoView.as_view('echo'))
        self.app = app.test_client()

    def test_unacceptable(self):
        response = self.app.get('/echo', headers={'Accept': 'text/x-spam'})
        self.assertEqual(response.status_code, 406)

    def test_unsupported(self):
        response = self.app.post('/echo', data='spam', content_type='text/x-spam', headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 415)

    def test_echo_get(self):
        response = self.app.get('/echo?spam=sv&eggs=ev', headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [
         [
          'eggs', 'ev'], ['spam', 'sv']])

    def test_echo_post(self):
        data = {'eggs': 'ev', 'spam': 'sv'}
        response = self.app.post('/echo', data=json.dumps(data), content_type='application/json', headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 200, response.status)
        self.assertEqual(json.loads(response.data), data)
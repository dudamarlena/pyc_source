# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brocaar/Work/Projects/Brocaar/Flask/flask-views/flask_views/tests/unit/test_json.py
# Compiled at: 2012-02-23 14:55:08
import unittest2 as unittest
from mock import patch, Mock
from flask_views.json import JSONResponseMixin, JSONView

class JSONResponseMixinTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.JSONResponseMixin`.
    """

    @patch('flask_views.json.json')
    @patch('flask_views.json.current_app')
    def test_render_to_response(self, current_app, json):
        """
        Test :py:meth:`.JSONResponseMixin.render_to_response`.
        """
        current_app.response_class.return_value = 'response-class'
        json.dumps.return_value = 'json-dump'
        mixin = JSONResponseMixin()
        self.assertEqual('response-class', mixin.render_to_response({'foo': 'bar'}))
        json.dumps.assert_called_once_with({'foo': 'bar'}, cls=None)
        current_app.response_class.assert_called_once_with('json-dump', mimetype='application/json')
        return

    @patch('flask_views.json.json')
    @patch('flask_views.json.current_app')
    def test_render_to_response_with_encoder_class(self, current_app, json):
        """
        Test :py:meth:`.JSONResponseMixin.render_to_response` with encoder cls.
        """
        current_app.response_class.return_value = 'response-class'
        json.dumps.return_value = 'json-dump'
        mixin = JSONResponseMixin()
        mixin.encoder_class = Mock()
        self.assertEqual('response-class', mixin.render_to_response({'foo': 'bar'}))
        json.dumps.assert_called_once_with({'foo': 'bar'}, cls=mixin.encoder_class)
        current_app.response_class.assert_called_once_with('json-dump', mimetype='application/json')


class JSONViewTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.JSONView`.
    """

    def test_get_context_data(self):
        """
        Test :py:meth:`.JSONView.get_context_data`.
        """
        view = JSONView()
        self.assertEqual({'params': {'foo': 'bar'}}, view.get_context_data(foo='bar'))

    def test_get(self):
        """
        Test :py:meth:`.JSONView.get`.
        """
        view = JSONView()
        view.get_context_data = Mock(return_value={'foo': 'bar'})
        view.render_to_response = Mock(return_value='response')
        self.assertEqual('response', view.get(bar='foo'))
        view.get_context_data.assert_called_once_with(bar='foo')
        view.render_to_response.assert_called_once_with({'foo': 'bar'})
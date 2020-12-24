# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\tests\request\test_basic.py
# Compiled at: 2013-06-04 13:50:32
__doc__ = ' Tests for the pyojo package.\n\n'
from base import pyojo, RequestTest, Browse, SERVER

@pyojo.route('/test_route_get', method='GET')
def test_route_get():
    return 'TEST GET'


@pyojo.route('/test_route_get', method='POST')
def test_route_post():
    return 'TEST POST'


@pyojo.route('/test_route_get', method='PUT')
def test_route_put():
    return 'TEST PUT'


@pyojo.route('/test_route_get', method='DELETE')
def test_route_delete():
    return 'TEST DELETE'


class Home(RequestTest):

    def test_route_get(self):
        r = Browse(SERVER + '/test_route_get', 'GET')
        self.assertEqual(r.response.status_code, 200, 'Status Fails')
        self.assertEqual(r.content, 'TEST GET', 'Content Fails')

    def test_route_post(self):
        r = Browse(SERVER + '/test_route_get', 'POST')
        self.assertEqual(r.response.status_code, 200, 'Status Fails')
        self.assertEqual(r.content, 'TEST POST', 'Content Fails')

    def test_route_put(self):
        r = Browse(SERVER + '/test_route_get', 'PUT')
        self.assertEqual(r.response.status_code, 200, 'Status Fails')
        self.assertEqual(r.content, 'TEST PUT', 'Content Fails')

    def test_route_delete(self):
        r = Browse(SERVER + '/test_route_get', 'DELETE')
        self.assertEqual(r.response.status_code, 200, 'Status Fails')
        self.assertEqual(r.content, 'TEST DELETE', 'Content Fails')
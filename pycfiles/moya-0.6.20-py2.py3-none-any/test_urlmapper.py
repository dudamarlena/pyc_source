# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_urlmapper.py
# Compiled at: 2015-09-01 07:17:44
import unittest
from moya import urlmapper
from moya.urlmapper import RouteMatch

class TestURLMapper(unittest.TestCase):

    def setUp(self):
        self.mapper = urlmapper.URLMapper()
        self.mapper.map('/', 'front')
        self.mapper.map('/page/', 'page', defaults={'page': 'front'})
        self.mapper.map('/page/{page}/', 'page')
        self.mapper.map('/page/{page}/edit/', 'edit', methods=['GET'])
        self.mapper.map('/page/{page}/edit/', 'editform', methods=['POST'])
        self.mapper.map('/blog/', 'blog')
        self.mapper.map('/blog/{year}/{month}/{day}/', 'post')
        self.submapper = urlmapper.URLMapper()
        self.submapper.map('/', 'wikifront')
        self.submapper.map('/page/{slug}/', 'wikipage')
        self.mapper.mount('/wiki/', self.submapper)

    def testSimple(self):
        """Test simple top-level URL mapping"""
        self.assertEqual(self.mapper.get_route('/'), RouteMatch({}, 'front', None))
        self.assertEqual(self.mapper.get_route('/page/'), RouteMatch({'page': 'front'}, 'page', None))
        self.assertEqual(self.mapper.get_route('/page/welcome/'), RouteMatch({'page': 'welcome'}, 'page', None))
        self.assertEqual(self.mapper.get_route('/blog/'), RouteMatch({}, 'blog', None))
        self.assertEqual(self.mapper.get_route('/blog/2011/7/5/'), RouteMatch(dict(year='2011', month='7', day='5'), 'post', None))
        self.assertEqual(self.mapper.get_route('/nothere/'), None)
        self.assertEqual(self.mapper.get_route('/'), RouteMatch({}, 'front', None))
        self.assertEqual(self.mapper.get_route('/page/'), RouteMatch({'page': 'front'}, 'page', None))
        self.assertEqual(self.mapper.get_route('/page/welcome/'), RouteMatch({'page': 'welcome'}, 'page', None))
        self.assertEqual(self.mapper.get_route('/blog/'), RouteMatch({}, 'blog', None))
        self.assertEqual(self.mapper.get_route('/blog/2011/7/5/'), RouteMatch(dict(year='2011', month='7', day='5'), 'post', None))
        self.assertEqual(self.mapper.get_route('/nothere/'), None)
        return

    def testSubMapper(self):
        """Test URL sub-mapper"""
        self.assertEqual(self.mapper.get_route('/wiki/'), RouteMatch({}, 'wikifront', None))
        self.assertEqual(self.mapper.get_route('/wiki/page/moya/'), RouteMatch({'slug': 'moya'}, 'wikipage', None))
        self.assertEqual(self.mapper.get_route('/wiki/'), RouteMatch({}, 'wikifront', None))
        self.assertEqual(self.mapper.get_route('/wiki/page/moya/'), RouteMatch({'slug': 'moya'}, 'wikipage', None))
        return

    def testMethodMap(self):
        """Test URL mapping by method"""
        self.assertEqual(self.mapper.get_route('/page/moya/edit/'), RouteMatch(dict(page='moya'), 'edit', None))
        self.assertEqual(self.mapper.get_route('/page/moya/edit/', 'GET'), RouteMatch(dict(page='moya'), 'edit', None))
        self.assertEqual(self.mapper.get_route('/page/moya/edit/', 'POST'), RouteMatch(dict(page='moya'), 'editform', None))
        self.assertEqual(self.mapper.get_route('/page/moya/edit/'), RouteMatch(dict(page='moya'), 'edit', None))
        self.assertEqual(self.mapper.get_route('/page/moya/edit/', 'GET'), RouteMatch(dict(page='moya'), 'edit', None))
        self.assertEqual(self.mapper.get_route('/page/moya/edit/', 'POST'), RouteMatch(dict(page='moya'), 'editform', None))
        return
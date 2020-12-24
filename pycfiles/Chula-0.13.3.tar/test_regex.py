# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/www/mapper/test_regex.py
# Compiled at: 2011-03-19 21:05:04
import logging, unittest
from chula import config, logger
from chula.www.adapters.mod_python import fakerequest
from chula.www.mapper import regex
mapper = (
 ('^/$', 'home.index'),
 ('^/home/?$', 'home.index'),
 ('^/home/index/?$', 'home.index'),
 ('^/sample/?$', 'sample.index'),
 ('^/sample/page/?$', 'sample.page'))
cfg = config.Config()
cfg.log_level = logging.WARNING + 1
log = logger.Logger(cfg).logger()

class Test_regex(unittest.TestCase):
    doctest = regex

    def setUp(self):
        req = fakerequest.FakeRequest()
        cfg = config.Config()
        cfg.classpath = 'package'
        cfg.error_controller = 'error'
        self.mapper = regex.RegexMapper(cfg, req, mapper)

    def test_homepage(self):
        self.mapper.uri = '/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'home')
        self.assertEquals(self.mapper.route.class_name, 'Home')
        self.assertEquals(self.mapper.route.method, 'index')

    def test_regex_match(self):
        self.mapper.uri = '/sample'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'sample')
        self.assertEquals(self.mapper.route.class_name, 'Sample')
        self.assertEquals(self.mapper.route.method, 'index')

    def test_regex_match_with_optional_slash(self):
        self.mapper.uri = '/sample/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'sample')
        self.assertEquals(self.mapper.route.class_name, 'Sample')
        self.assertEquals(self.mapper.route.method, 'index')

    def test_uri_without_any_match(self):
        self.mapper.uri = '/foo/bar/bla/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'error')
        self.assertEquals(self.mapper.route.class_name, 'Error')
        self.assertEquals(self.mapper.route.method, 'e404')
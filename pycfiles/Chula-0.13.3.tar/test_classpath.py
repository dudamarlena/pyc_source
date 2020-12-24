# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/www/mapper/test_classpath.py
# Compiled at: 2011-03-19 21:05:04
import unittest
from chula import config
from chula.www.adapters.mod_python import fakerequest
from chula.www.mapper import classpath

class Test_classpath(unittest.TestCase):
    doctest = classpath

    def setUp(self):
        req = fakerequest.FakeRequest()
        cfg = config.Config()
        cfg.classpath = 'package'
        cfg.error_controller = 'error'
        self.mapper = classpath.ClassPathMapper(cfg, req)

    def tearDown(self):
        pass

    def test_homepage(self):
        self.mapper.uri = '/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'home')
        self.assertEquals(self.mapper.route.class_name, 'Home')
        self.assertEquals(self.mapper.route.method, 'index')

    def test_module_with_named_method(self):
        self.mapper.uri = '/module/method/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'module')
        self.assertEquals(self.mapper.route.class_name, 'Module')
        self.assertEquals(self.mapper.route.method, 'method')

    def test_module_with_implied_method(self):
        self.mapper.uri = '/module/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'module')
        self.assertEquals(self.mapper.route.class_name, 'Module')
        self.assertEquals(self.mapper.route.method, 'index')

    def test_package_with_named_method(self):
        self.mapper.uri = '/pkg/module/method/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package.pkg')
        self.assertEquals(self.mapper.route.module, 'module')
        self.assertEquals(self.mapper.route.class_name, 'Module')
        self.assertEquals(self.mapper.route.method, 'method')
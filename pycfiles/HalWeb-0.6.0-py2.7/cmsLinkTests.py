# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/tests/cms/cmsLinkTests.py
# Compiled at: 2012-01-05 03:38:38
from tests.testImports import *
from controllers.cmsControllers import CMSLinksController
from models.BaseModels import Person

class TestLinks(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLinks, self).__init__(*args, **kwargs)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def setUp(self):
        self.request = webapp.Request({'wsgi.input': StringIO(), 
           'CONTENT_LENGTH': 0, 
           'REQUEST_METHOD': 'GET', 
           'PATH_INFO': '/'})
        self.response = webapp.Response()
        self.link = CMSLinksController()
        self.link.Impersonated = Person.CreateNew('test', 'test', 'test', 'test@test.com', 'test', True, True, 'local', None, False)
        self.link.Impersonated.IsAdmin = True
        return

    def tearDown(self):
        self.testbed.deactivate()

    def testIndexController(self):
        self.link.initialize(self.request, self.response)
        result = self.link.index('cms')
        self.assertIsNotNone(result, 'none is returned')
        print self.response.out.getvalue()
        self.assertTrue(isinstance(result, dict), 'No Dict returned. Instead dict:\r\n')
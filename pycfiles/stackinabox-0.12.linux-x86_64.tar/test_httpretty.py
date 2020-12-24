# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmeyer/Devel/stackInABox/.tox/twine/lib/python2.7/site-packages/stackinabox/tests/test_httpretty.py
# Compiled at: 2017-05-27 01:24:11
"""
Stack-In-A-Box: Basic Test
"""
import logging, unittest, httpretty, requests, six, stackinabox.util.httpretty
from stackinabox.stack import StackInABox
from stackinabox.services.hello import HelloService
from stackinabox.tests.utils.services import AdvancedService
logger = logging.getLogger(__name__)

@httpretty.activate
class TestHttprettyBasic(unittest.TestCase):

    def setUp(self):
        super(TestHttprettyBasic, self).setUp()
        StackInABox.register_service(HelloService())

    def tearDown(self):
        super(TestHttprettyBasic, self).tearDown()
        StackInABox.reset_services()

    def test_basic(self):
        stackinabox.util.httpretty.httpretty_registration('localhost')
        res = requests.get('http://localhost/hello/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'Hello')


@httpretty.activate
class TestHttprettyAdvanced(unittest.TestCase):

    def setUp(self):
        super(TestHttprettyAdvanced, self).setUp()
        StackInABox.register_service(AdvancedService())

    def tearDown(self):
        super(TestHttprettyAdvanced, self).tearDown()
        StackInABox.reset_services()

    def test_basic(self):
        stackinabox.util.httpretty.httpretty_registration('localhost')
        res = requests.get('http://localhost/advanced/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'Hello')
        res = requests.get('http://localhost/advanced/h')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'Good-Bye')
        expected_result = {'bob': 'bob: Good-Bye alice', 
           'alice': 'alice: Good-Bye bob', 
           'joe': 'joe: Good-Bye jane'}
        res = requests.get('http://localhost/advanced/g?bob=alice;alice=bob&joe=jane')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_result)
        res = requests.get('http://localhost/advanced/1234567890')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'okay')
        res = requests.get('http://localhost/advanced/_234567890')
        self.assertEqual(res.status_code, 595)
        res = requests.put('http://localhost/advanced/h')
        self.assertEqual(res.status_code, 405)
        res = requests.put('http://localhost/advanced2/i')
        self.assertEqual(res.status_code, 597)
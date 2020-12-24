# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiform\tests\test_wsgiform.py
# Compiled at: 2006-12-10 15:00:15
"""Unit tests for wsgiform."""
import wsgiform.form
from wsgiform.validators import getvalidator
import unittest, StringIO, copy

class TestWsgiForm(unittest.TestCase):
    """Test cases for wsgiform."""
    __module__ = __name__
    test_env = {'CONTENT_LENGTH': '118', 'wsgi.multiprocess': 0, 'wsgi.version': (1, 0), 'CONTENT_TYPE': 'application/x-www-form-urlencoded', 'SERVER_NAME': '127.0.0.1', 'wsgi.run_once': 0, 'wsgi.errors': StringIO.StringIO(), 'wsgi.multithread': 0, 'SCRIPT_NAME': '', 'wsgi.url_scheme': 'http', 'wsgi.input': StringIO.StringIO('num=12121&str1=test&name=%3Ctag+id%3D%22Test%22%3EThis+is+a+%27test%27+%26+another.%3C%2Ftag%3E&state=NV&Submit=Submit'), 'REQUEST_METHOD': 'POST', 'HTTP_HOST': '127.0.0.1', 'PATH_INFO': '/', 'SERVER_PORT': '80', 'SERVER_PROTOCOL': 'HTTP/1.0'}

    def dummy_app(self, environ, func):
        return environ

    def dummy_sr(self, status, headers, exc_info=None):
        pass

    def test_fieldstorage(self):
        """Parses form data into a FieldStorage instance."""
        form = wsgiform.WsgiForm(self.dummy_app, style='fieldstorage')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.fieldstorage'].getfirst('num'), '12121')

    def test_dictionary(self):
        """Parses form data into a dictionary."""
        form = wsgiform.WsgiForm(self.dummy_app, style='dict')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['num'], '12121')

    def test_kwargs(self):
        """Parses form data into keyword arguments."""
        form = wsgiform.WsgiForm(self.dummy_app, style='kwargs')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgize.kwargs']['num'], '12121')

    def test_environ(self):
        """Parses form data into individual environ entries."""
        form = wsgiform.WsgiForm(self.dummy_app, style='environ')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.num'], '12121')

    def test_escape(self):
        """Parses form data into a dictionary with HTML escaping. """
        form = wsgiform.WsgiForm(self.dummy_app)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], '&lt;tag id=&quot;Test&quot;&gt;This is a &#39;test&#39; &amp; another.&lt;/tag&gt;')

    def test_hyperescape(self):
        """Parses form data into a dictionary with HTML hyperescaping. """
        form = wsgiform.WsgiForm(self.dummy_app, func='hyperescape')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], '&#60;tag id&#61;&#34;Test&#34;&#62;This is a &#39;test&#39; &#38; another.&#60;&#47;tag&#62;')

    def test_strictescape(self):
        """Parses form data into a dictionary with strict HTML escaping."""
        form = wsgiform.WsgiForm(self.dummy_app, strict=True)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], '&lt;tag id=&quot;Test&quot;&gt;This is a &#39;test&#39; &amp; another.&lt;/tag&gt;')

    def test_stricthyperescape(self):
        """Parses form data into a dictionary with strict HTML hyperescaping."""
        form = wsgiform.WsgiForm(self.dummy_app, func='hyperescape', strict=True)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], '&#60;tag id&#61;&#34;Test&#34;&#62;This is a &#39;test&#39; &#38; another.&#60;&#47;tag&#62;')

    def test_sterilize(self):
        """Parses form data into a dictionary with data sterilization."""
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], 'tag idTestThis is a test  another.tag')

    def test_strictsterilize(self):
        """Parses form data into a dictionary with strict data sterilization."""
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize', strict=True)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], 'tag idTestThis is a test  another.tag')

    def test_validation(self):
        """Tests data validation."""
        vdict = {'num': getvalidator(('number', ('range', 10000, 15000)))}
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize', validators=vdict)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], 'tag idTestThis is a test  another.tag')

    def test_validation_false(self):
        """Tests bad data validation."""
        vdict = {'num': getvalidator(('float', ('range', 1000, 1500)))}
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize', validators=vdict)
        iteble = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(iteble[0], 'Data in field(s) num was invalid.')

    def test_validation_strict(self):
        """Tests strict data validation."""
        vdict = {'num': getvalidator(('number', ('range', 10000, 15000)))}
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize', strict=True, validators=vdict)
        iteble = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(iteble[0], 'Data in field(s) str1 name Submit state was invalid.')


if __name__ == '__main__':
    unittest.main()
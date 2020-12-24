# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/repoze/who/plugins/test_captcha.py
# Compiled at: 2008-09-23 07:17:14
from ConfigParser import ConfigParser
from repoze.who.tests import Base, DummyIdentifier, encode_multipart_formdata
PRIVATE_KEY = 'whocares'

class DummyLogger(object):

    def debug(self, msg):
        return msg


class TestFormPlugin(Base):

    def _getTargetClass(self):
        from repoze.who.plugins.captcha import RecaptchaPlugin
        return RecaptchaPlugin

    def _makeOne(self, private_key='read_some_config', form_handler=None):
        plugin = self._getTargetClass()(private_key, form_handler)
        return plugin

    def _makeFormEnviron(self, login='chris', password='password', pathinfo='/process'):
        from StringIO import StringIO
        fields = []
        if login:
            fields.append(('login', login))
        if password:
            fields.append(('password', password))
        (content_type, body) = encode_multipart_formdata(fields)
        credentials = {'login': 'chris', 'password': 'password'}
        identifier = DummyIdentifier(credentials)
        extra = {'wsgi.input': StringIO(body), 'wsgi.url_scheme': 'http', 
           'SERVER_NAME': 'localhost', 
           'SERVER_PORT': '8080', 
           'CONTENT_TYPE': content_type, 
           'CONTENT_LENGTH': len(body), 
           'REQUEST_METHOD': 'POST', 
           'repoze.who.plugins': {'cookie': identifier}, 'repoze.who.logger': DummyLogger(), 
           'PATH_INFO': pathinfo, 
           'QUERY_STRING': '', 
           'REMOTE_ADDR': '127.0.0.1'}
        environ = self._makeEnviron(extra)
        return environ

    def test_implements(self):
        from zope.interface.verify import verifyClass
        from repoze.who.interfaces import IAuthenticator
        klass = self._getTargetClass()
        verifyClass(IAuthenticator, klass)

    def test_nohandler_fail(self):
        plugin = self._makeOne(PRIVATE_KEY)
        environ = self._makeFormEnviron()
        plugin.authenticate(environ, environ['repoze.who.plugins']['cookie'])
        app = environ['repoze.who.application']
        self.assert_(isinstance(environ['repoze.who.error'], basestring))
        self.assertEqual(app.code, 401)

    def test_handler_pass(self):
        plugin = self._makeOne(PRIVATE_KEY, '/')
        environ = self._makeFormEnviron()
        plugin.authenticate(environ, environ['repoze.who.plugins']['cookie'])
        self.assertEqual(environ.get('repoze.who.error'), None)
        self.assertEqual(environ.get('repoze.who.application'), None)
        return

    def test_handler_fail(self):
        plugin = self._makeOne(PRIVATE_KEY, '/ /process /login')
        environ = self._makeFormEnviron()
        plugin.authenticate(environ, environ['repoze.who.plugins']['cookie'])
        app = environ['repoze.who.application']
        self.assert_(isinstance(environ['repoze.who.error'], basestring))
        self.assertEqual(app.code, 401)
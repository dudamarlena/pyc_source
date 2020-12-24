# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/testsuite/sessions.py
# Compiled at: 2013-03-16 04:04:43
import unittest, tempfile, shutil
from frame._app import app
from frame._config import config
from frame.dotdict import DotDict
from frame.errors import SessionLoadError, SessionSaveError
from frame.sessions import SessionInterface, Session
from frame.response import Response

class TestSession(unittest.TestCase):

    def setUp(self):
        app.request = DotDict({'headers': {}, 'cookies': {}})
        app.response = Response(app, 'junk')
        self.session_interface = SessionInterface(app)

    def test_session_load_error(self):
        app.request.cookies['FrameSession'] = Session.make_session_key()
        with self.assertRaises(SessionLoadError):
            session = self.session_interface.backend(app, self.session_interface)

    def test_session_force(self):
        session = self.session_interface.backend(app, self.session_interface, True)

    def test_session_save(self):
        session = self.session_interface.get_session()
        session['stuff'] = 'a test'
        app.request.cookies['FrameSession'] = session._key
        session.commit()
        session = self.session_interface.get_session()
        self.assertEqual(session['stuff'], 'a test')


class TestMemorySession(TestSession):

    def setUp(self):
        config.sessions.driver = 'memory'
        TestSession.setUp(self)


class TestFileSession(TestSession):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        config.sessions.driver = 'file'
        config.sessions.file.directory = self.temp_dir
        TestSession.setUp(self)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


class TestMemcacheSession(TestSession):

    def setUp(self):
        config.sessions.driver = 'memcache'
        try:
            import memcache
        except ImportError:
            self.skipTest('python-memcached not installed so not testing')

        TestSession.setUp(self)
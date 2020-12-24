# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/tests/test_init.py
# Compiled at: 2010-12-12 04:36:57
"""Unit tests for the runtime environment."""
import os, re, sys, typhoonae, unittest

class InitTestCase(unittest.TestCase):
    """Tests a number of helper functions."""

    def setUp(self):
        """Loads the sample application."""
        app_root = os.path.join(os.path.dirname(__file__), 'sample')
        os.chdir(app_root)
        sys.path.insert(0, os.getcwd())
        self.conf = typhoonae.getAppConfig()
        assert self.conf.application == 'sample'

    def testSetupStubs(self):
        """Sets up apiproxy stubs."""

        class TestOptions:
            blobstore_path = 'blobstore'
            datastore = 'mongodb'
            http_port = 8080
            internal_address = 'localhost:8770'
            login_url = '/_ah/login'
            logout_url = '/_ah/logout'
            server_name = 'localhost'
            smtp_host = 'localhost'
            smtp_port = 25
            smtp_user = ''
            smtp_password = ''
            use_celery = False
            xmpp_host = 'localhost'

        typhoonae.setupStubs(self.conf, TestOptions())

    def testInitURLMapping(self):
        """Initializes the url/script map."""

        class TestOptions:
            login_url = '/_ah/login'
            logout_url = '/_ah/logout'

        url_mapping = typhoonae.initURLMapping(self.conf, TestOptions())
        for (pattern, handler_path, path, login_required, admin_only) in url_mapping:
            if pattern.match('/foo'):
                self.assertEqual(handler_path, 'app.py')
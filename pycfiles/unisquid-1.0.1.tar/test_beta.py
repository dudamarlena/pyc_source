# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patrik/workspace/unisquid/tests/test_beta.py
# Compiled at: 2016-07-26 12:20:30
from urllib import urlopen
from flask_app import create_app
from unisquid import LiveServerTestCase

class TestLiveServer(LiveServerTestCase):

    def create_app(self):
        return create_app()

    def test_server_process_is_spawned(self):
        thread = self.server_thread
        self.assertNotEqual(thread, None)
        self.assertTrue(thread.is_alive())
        return

    def test_server_process_listening(self):
        response = urlopen(self.live_server_url)
        self.assertTrue('OK' in response.read())
        self.assertEqual(response.code, 200)
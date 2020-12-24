# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patrik/workspace/unisquid/tests/test_liveserver.py
# Compiled at: 2016-07-26 12:35:38
import unisquid, urllib, wsgiref

class TestLiveServer(unisquid.LiveServerTestCase):

    def create_app(self):
        return wsgiref.simple_server.demo_app

    def test_server_process_is_spawned(self):
        thread = self.server_thread
        self.assertNotEqual(thread, None)
        self.assertTrue(thread.is_alive())
        return

    def test_server_process_listening(self):
        response = urllib.urlopen(self.live_server_url)
        self.assertTrue('Hello world!' in response.read())
        self.assertEqual(response.code, 200)
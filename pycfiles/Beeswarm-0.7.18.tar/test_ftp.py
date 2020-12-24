# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/tests/test_ftp.py
# Compiled at: 2016-11-12 07:38:04
import gevent, gevent.monkey
gevent.monkey.patch_all()
import unittest, tempfile, shutil, os, ftplib
from ftplib import FTP
from gevent.server import StreamServer
from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.drones.honeypot.capabilities import ftp

class FtpTests(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_login(self):
        """Testing different login combinations"""
        options = {'enabled': 'True', 'port': 0, 'banner': 'Test Banner', 'users': {'test': 'test'}, 'protocol_specific_data': {'max_attempts': 3, 'banner': 'test banner', 'syst_type': 'Test Type'}}
        cap = ftp.ftp(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        ftp_client = FTP()
        ftp_client.connect('127.0.0.1', srv.server_port, 1)
        try:
            ftp_client.login('james', 'bond')
            response = ftp_client.getresp()
        except ftplib.error_perm:
            pass

        srv.stop()
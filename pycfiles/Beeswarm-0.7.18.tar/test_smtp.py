# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/tests/test_smtp.py
# Compiled at: 2016-11-12 07:38:04
import smtplib, base64, hmac, os, tempfile, shutil, gevent.monkey
from gevent.server import StreamServer
from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.drones.honeypot.capabilities import smtp
gevent.monkey.patch_all()
import unittest

class SmtpTests(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_connection(self):
        """ Tries to connect and run a EHLO command. Very basic test.
        """
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'banner': 'test'}, 'users': {'test': 'test'}}
        cap = smtp.smtp(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        smtp_ = smtplib.SMTP('127.0.0.1', srv.server_port, local_hostname='localhost', timeout=15)
        smtp_.ehlo()
        smtp_.quit()
        srv.stop()

    def test_AUTH_CRAM_MD5_reject(self):
        """ Makes sure the server rejects all invalid login attempts that use the
            CRAM-MD5 Authentication method.
        """
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'banner': 'Test'}, 'users': {'someguy': 'test'}}
        cap = smtp.smtp(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        def encode_cram_md5(challenge, user, password):
            challenge = base64.decodestring(challenge)
            response = user + ' ' + hmac.HMAC(password, challenge).hexdigest()
            return base64.b64encode(response)

        smtp_ = smtplib.SMTP('127.0.0.1', srv.server_port, local_hostname='localhost', timeout=15)
        _, resp = smtp_.docmd('AUTH', 'CRAM-MD5')
        code, resp = smtp_.docmd(encode_cram_md5(resp, 'test', 'test'))
        self.assertEqual(code, 535)
        srv.stop()

    def test_AUTH_PLAIN_reject(self):
        """ Makes sure the server rejects all invalid login attempts that use the PLAIN Authentication method.
        """
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'banner': 'Test'}, 'users': {'someguy': 'test'}}
        cap = smtp.smtp(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        smtp_ = smtplib.SMTP('127.0.0.1', srv.server_port, local_hostname='localhost', timeout=15)
        arg = '\x00%s\x00%s' % ('test', 'test')
        code, resp = smtp_.docmd('AUTH', 'PLAIN ' + base64.b64encode(arg))
        self.assertEqual(code, 535)
        srv.stop()

    def test_AUTH_LOGIN_reject(self):
        """ Makes sure the server rejects all invalid login attempts that use the LOGIN Authentication method.
        """
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'banner': 'Test'}, 'users': {'someguy': 'test'}}
        cap = smtp.smtp(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        smtp_ = smtplib.SMTP('127.0.0.1', srv.server_port, local_hostname='localhost', timeout=15)
        smtp_.docmd('AUTH', 'LOGIN')
        smtp_.docmd(base64.b64encode('test'))
        code, resp = smtp_.docmd(base64.b64encode('test'))
        self.assertEqual(code, 535)
        srv.stop()

    def test_AUTH_CRAM_MD5(self):
        """ Makes sure the server accepts valid login attempts that use the CRAM-MD5 Authentication method.
        """
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'banner': 'Test'}, 'users': {'test': 'test'}}
        cap = smtp.smtp(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        def encode_cram_md5(challenge, user, password):
            challenge = base64.decodestring(challenge)
            response = user + ' ' + hmac.HMAC(password, challenge).hexdigest()
            return base64.b64encode(response)

        smtp_ = smtplib.SMTP('127.0.0.1', srv.server_port, local_hostname='localhost', timeout=15)
        _, resp = smtp_.docmd('AUTH', 'CRAM-MD5')
        code, resp = smtp_.docmd(encode_cram_md5(resp, 'test', 'test'))
        self.assertEqual(code, 235)
        srv.stop()

    def test_AUTH_PLAIN(self):
        """ Makes sure the server accepts valid login attempts that use the PLAIN Authentication method.
        """
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'banner': 'Test'}, 'users': {'test': 'test'}}
        cap = smtp.smtp(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        smtp_ = smtplib.SMTP('127.0.0.1', srv.server_port, local_hostname='localhost', timeout=15)
        arg = '\x00%s\x00%s' % ('test', 'test')
        code, resp = smtp_.docmd('AUTH', 'PLAIN ' + base64.b64encode(arg))
        self.assertEqual(code, 235)
        srv.stop()

    def test_AUTH_LOGIN(self):
        """ Makes sure the server accepts valid login attempts that use the LOGIN Authentication method.
        """
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'banner': 'Test'}, 'users': {'test': 'test'}}
        cap = smtp.smtp(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        smtp_client = smtplib.SMTP('127.0.0.1', srv.server_port, local_hostname='localhost', timeout=15)
        smtp_client.docmd('AUTH', 'LOGIN')
        smtp_client.docmd(base64.b64encode('test'))
        code, resp = smtp_client.docmd(base64.b64encode('test'))
        self.assertEqual(code, 235)
        srv.stop()


if __name__ == '__main__':
    unittest.main()
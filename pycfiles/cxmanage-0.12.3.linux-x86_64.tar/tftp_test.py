# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/tftp_test.py
# Compiled at: 2017-02-08 04:42:30
"""Calxeda: tftp_test.py"""
import os, socket, unittest
from cxmanage_api.tests import random_file
from cxmanage_api.tftp import InternalTftp, ExternalTftp

def _get_relative_host():
    """Returns the test machine ip as a relative host to pass to the
    InternalTftp server.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return sock.getsockname()[0]
    except socket.error:
        raise


class InternalTftpTest(unittest.TestCase):
    """ Tests the functions of the InternalTftp class."""

    def setUp(self):
        """Create local Internal TFTP objects to test with."""
        self.tftp1 = InternalTftp()
        self.tftp2 = InternalTftp(ip_address='127.0.0.254')

    def test_put_and_get(self):
        """ Test file transfers on an internal host """
        filename = random_file(1024)
        contents = open(filename).read()
        basename = os.path.basename(filename)
        self.tftp1.put_file(filename, basename)
        os.remove(filename)
        self.assertFalse(os.path.exists(filename))
        self.tftp1.get_file(basename, filename)
        self.assertEqual(open(filename).read(), contents)
        os.remove(filename)

    def test_get_address_with_relhost(self):
        """Tests the get_address(relative_host) function with a relative_host
        specified.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect((socket.gethostname(), 9))
            relative_host = sock.getsockname()[0]
        except socket.error:
            raise

        self.assertEqual(self.tftp2.ip_address, self.tftp2.get_address(relative_host=relative_host))
        sock.close()


class ExternalTftpTest(unittest.TestCase):
    """Tests the ExternalTftp class.
    ..note:
        * For testing purposes the 'external' server points to an internally
          hosted one, but it allows us to make sure the actual TFTP protocol is
          working.
    """

    def setUp(self):
        """Create an ExternalTftp object to test with."""
        self.itftp = InternalTftp(ip_address='127.0.0.250')
        self.etftp = ExternalTftp(self.itftp.get_address(relative_host=_get_relative_host()), self.itftp.port)

    def test_put_and_get(self):
        """Test the put_file(src, dest) function. Test the get_file(src,dest)
        function by movign local files around using the TFT Protocol.
        """
        filename = random_file(1024)
        contents = open(filename).read()
        basename = os.path.basename(filename)
        self.etftp.put_file(src=filename, dest=basename)
        os.remove(filename)
        self.assertFalse(os.path.exists(filename))
        self.etftp.get_file(src=basename, dest=filename)
        self.assertEqual(open(filename).read(), contents)
        os.remove(filename)
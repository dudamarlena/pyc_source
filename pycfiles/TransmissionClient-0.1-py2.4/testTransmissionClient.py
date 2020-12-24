# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/test/testTransmissionClient.py
# Compiled at: 2007-08-05 15:38:01
__author__ = 'Tom Lazar (tom@tomster.org)'
__version__ = '$Revision: 0.1 $'
__date__ = '$Date: 2007/07/29 $'
__copyright__ = 'Copyright (c) 2007 Tom Lazar'
__license__ = 'MIT License'
import sys, os
sys.path = [
 '.'] + sys.path
import unittest, doctest
from TransmissionClient import TransmissionClient
SOCKETPATH = None

class TransmissionTests(unittest.TestCase):
    """ 
        These tests expect a running transmission-daemon instance listening on port 9090
    """
    __module__ = __name__

    def setUp(self):
        """makes sure we've got a transmission daemon running to run the tests against."""
        self.daemon = TransmissionClient(SOCKETPATH)

    def testStartup(self):
        self.failIf(self.daemon == None)
        return

    def testDoctests(self):
        """docstring for testDoctests"""
        doctest.testfile('README.rst', verbose=False, report=True, globs={'SOCKETPATH': SOCKETPATH, 'self': self})


def usage():
    print 'ERROR:\n        You must provide a full path to the socket of a locally running transmission-daemon as \n        the LAST command line argument to this test call, i.e.:\n        \n            python test/testTransmissionClient.py SOCKETPATH\n            python test/testTransmissionClient.py TransmissionTests SOCKETPATH\n            python test/testTransmissionClient.py TransmissionTests.testDoctests SOCKETPATH\n            etc.\n        \n        '


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)
    SOCKETPATH = sys.argv[(-1)]
    if os.path.exists(SOCKETPATH):
        sys.argv = sys.argv[:-1]
        unittest.main()
    else:
        usage()
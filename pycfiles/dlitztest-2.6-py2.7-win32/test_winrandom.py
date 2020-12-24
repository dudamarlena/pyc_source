# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Util\test_winrandom.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Util.winrandom"""
__revision__ = '$Id$'
import unittest

class WinRandomImportTest(unittest.TestCase):

    def runTest(self):
        """winrandom: simple test"""
        from Crypto.Util import winrandom
        randobj = winrandom.new()
        x = randobj.get_bytes(16)
        y = randobj.get_bytes(16)
        self.assertNotEqual(x, y)


def get_tests(config={}):
    return [
     WinRandomImportTest()]


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')
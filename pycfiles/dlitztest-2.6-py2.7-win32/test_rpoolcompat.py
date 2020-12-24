# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Random\test_rpoolcompat.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test for the Crypto.Util.randpool.RandomPool wrapper class"""
__revision__ = '$Id$'
import sys, unittest

class SimpleTest(unittest.TestCase):

    def runTest(self):
        """Crypto.Util.randpool.RandomPool"""
        from Crypto.Util.randpool import RandomPool
        sys.stderr.write('SelfTest: You can ignore the RandomPool_DeprecationWarning that follows.\n')
        rpool = RandomPool()
        x = rpool.get_bytes(16)
        y = rpool.get_bytes(16)
        self.assertNotEqual(x, y)
        self.assertNotEqual(rpool.entropy, 0)
        rpool.randomize()
        rpool.stir('foo')
        rpool.add_event('foo')


def get_tests(config={}):
    return [
     SimpleTest()]


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')
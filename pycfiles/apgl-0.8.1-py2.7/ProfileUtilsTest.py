# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/test/ProfileUtilsTest.py
# Compiled at: 2011-08-29 06:11:52
import logging, unittest, numpy, scipy.sparse
from apgl.util.ProfileUtils import ProfileUtils

class ProfileUtilsTest(unittest.TestCase):

    def testMemDisplay(self):
        A = numpy.random.rand(10, 10)
        B = numpy.random.rand(100, 100)
        C = scipy.sparse.rand(1000, 1000, 0.5)

    def testMemory(self):
        logging.info(ProfileUtils.memory())


if __name__ == '__main__':
    unittest.main()
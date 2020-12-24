# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\test_b3.py
# Compiled at: 2016-03-08 18:42:10
from tests import B3TestCase
import b3

class Test_getConfPath(B3TestCase):

    def test_getConfPath(self):
        self.console.config.fileName = '/some/where/conf/b3.xml'
        self.assertEqual('/some/where/conf', b3.getConfPath())
        self.console.config.fileName = './b3.xml'
        self.assertEqual('.', b3.getConfPath())
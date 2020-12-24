# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/mrlpy/testService.py
# Compiled at: 2017-08-11 20:26:07
from mservice import MService

class TestService(MService):

    def __init__(self, name):
        super(TestService, self).__init__(name)

    def test(self):
        print 'TEST SUCCESSFUL'


if __name__ == '__main__':
    t = TestService('t')
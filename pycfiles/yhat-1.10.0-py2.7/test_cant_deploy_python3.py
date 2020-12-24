# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_cant_deploy_python3.py
# Compiled at: 2017-04-26 17:15:42
from yhat import Yhat, YhatModel
import unittest

class HelloWorld(YhatModel):

    def execute(self, data):
        me = data['name']
        greeting = 'Hello %s!' % me
        return {'greeting': greeting}


class TestPython3Deployment(unittest.TestCase):

    def test_deployment(self):
        yh = Yhat('foo', 'bar', 'http://api.yhathq.com/')
        _, bundle = yh.deploy('HelloWorld', HelloWorld, globals(), dry_run=True)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/ENV2/lib/python2.7/site-packages/tests/test_mongo.py
# Compiled at: 2017-04-12 13:00:41
""" run with

python setup.py install; nosetests -v --nocapture tests/test_mongo.py:Test_mongo.test_001

nosetests -v --nocapture tests/test_mongo.py

or

nosetests -v tests/cm_basic/test_shell.py

"""
from __future__ import print_function
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.util import HEADING
from cloudmesh.rest.server.mongo import Mongo

def run(command):
    parameter = command.split(' ')
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return str(result)


class Test_mongo(object):
    """

    """

    def setup(self):
        pass

    def test_001(self):
        HEADING('start mongo')
        mongo = Mongo()
        r = mongo.start()
        print(r)
        r = mongo.status()
        print(r)
        assert False
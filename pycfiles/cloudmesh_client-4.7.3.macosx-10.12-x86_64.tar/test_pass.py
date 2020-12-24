# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/test_pass.py
# Compiled at: 2017-04-23 10:30:41
""" run with

nosetests -v --nocapture

or

nosetests -v

"""
from cloudmesh_client.common.util import HEADING

class Test_pass:

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        HEADING()
        assert True
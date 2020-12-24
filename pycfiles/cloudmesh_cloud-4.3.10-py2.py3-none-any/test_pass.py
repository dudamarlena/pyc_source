# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/test_pass.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\nnosetests -v --nocapture\n\nor\n\nnosetests -v\n\n'
from cloudmesh_client.common.util import HEADING

class Test_pass:

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        HEADING()
        assert True
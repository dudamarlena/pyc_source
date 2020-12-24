# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/base.py
# Compiled at: 2013-08-11 10:36:51
from factory import build_client

class BaseTestCaseMixin(object):

    def setUp(self):
        client = build_client()
        self.client = client
        self.service = client.service
        self.factory = client.factory
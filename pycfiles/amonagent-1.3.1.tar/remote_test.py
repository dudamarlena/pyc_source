# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martin/amonagent/tests/remote_test.py
# Compiled at: 2014-02-05 04:43:34
import unittest
from amonagent.remote import Remote
from amonagent.runner import runner
from amonagent.settings import settings
from nose.tools import eq_
import requests, sys, amonagent

class TestRemote(unittest.TestCase):

    def setUp(self):
        self.remote = Remote()

    def test_save_system(self):
        system_info = runner.system()
        try:
            r = requests.get(self.remote.connection_url())
        except:
            r = False

        if r != False:
            self.remote.save_system_stats(system_info)

    def test_proxy_url(self):
        eq_(self.remote.connection_url(), 'http://localhost')
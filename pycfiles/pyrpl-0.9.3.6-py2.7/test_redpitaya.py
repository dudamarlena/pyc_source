# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_redpitaya.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import os
from pyrpl import Pyrpl, RedPitaya, user_config_dir

class TestRedpitaya(object):

    @classmethod
    def setUpAll(cls):
        print '=======SETTING UP TestRedpitaya==========='
        cls.hostname = os.environ.get('REDPITAYA_HOSTNAME')
        cls.password = os.environ.get('REDPITAYA_PASSWORD')
        cls.r = RedPitaya()

    @classmethod
    def tearDownAll(cls):
        print '=======TEARING DOWN TestRedpitaya==========='
        cls.r.end_all()

    def test_redpitaya(self):
        assert self.r is not None
        return

    def test_connect(self):
        assert self.r.hk.led == 0
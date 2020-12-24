# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/base.py
# Compiled at: 2015-11-08 18:30:19
import logging
from oslo_config import fixture as fixture_config
from oslotest import base as test_base
import tvrenamer
from tvrenamer import options
logging.captureWarnings(True)

class BaseTest(test_base.BaseTestCase):

    def setUp(self):
        super(BaseTest, self).setUp()
        self.CONF = self.useFixture(fixture_config.Config()).conf
        options.register_opts(self.CONF)
        self.CONF([], project=tvrenamer.PROJECT_NAME)
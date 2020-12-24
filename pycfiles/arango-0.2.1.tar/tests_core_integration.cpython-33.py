# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_core_integration.py
# Compiled at: 2013-09-26 14:12:21
# Size of source mod 2**32: 482 bytes
import logging
from nose.tools import assert_equal, assert_not_equal
from .tests_integraion_base import TestsIntegration
logger = logging.getLogger(__name__)

class TestsCoreIntegration(TestsIntegration):

    def test_version(self):
        response = self.conn.version
        assert_equal(response.server, 'arango')
        assert_not_equal(response.version, '')
        assert_equal(repr(response), '<{0} {1}>'.format(response.server.title(), response.version))
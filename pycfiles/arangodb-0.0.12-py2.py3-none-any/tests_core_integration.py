# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_core_integration.py
# Compiled at: 2013-09-26 14:12:21
import logging
from nose.tools import assert_equal, assert_not_equal
from .tests_integraion_base import TestsIntegration
logger = logging.getLogger(__name__)

class TestsCoreIntegration(TestsIntegration):

    def test_version(self):
        response = self.conn.version
        assert_equal(response.server, 'arango')
        assert_not_equal(response.version, '')
        assert_equal(repr(response), ('<{0} {1}>').format(response.server.title(), response.version))
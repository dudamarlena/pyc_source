# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_flow.py
# Compiled at: 2012-05-30 14:38:58
# Size of source mod 2**32: 855 bytes
import logging, os
from .tests_integraion_base import TestsIntegration
logger = logging.getLogger(__name__)
__all__ = ('TestsFlow', )

class TestsFlow(TestsIntegration):
    """TestsFlow"""

    def setUp(self):
        super(TestsFlow, self).setUp()
        c = self.conn
        c.collection.test.create()
        self.cl = c.collection.test

    def tearDown(self):
        c = self.conn
        for iid in self.cl.index()[0].keys():
            c.collection.test.index.delete(iid)

        c.collection.test.delete()
        super(TestsFlow, self).tearDown()


if 'INTEGRATION' not in os.environ:
    TestsFlow = None
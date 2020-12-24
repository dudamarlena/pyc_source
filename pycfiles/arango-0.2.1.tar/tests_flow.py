# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_flow.py
# Compiled at: 2012-05-30 14:38:58
import logging, os
from .tests_integraion_base import TestsIntegration
logger = logging.getLogger(__name__)
__all__ = ('TestsFlow', )

class TestsFlow(TestsIntegration):
    """
    Class to test usecases of ArangoDB driver.

    Sample cases:
     - create document
     - update document
     - create edge
     etc.
    """

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
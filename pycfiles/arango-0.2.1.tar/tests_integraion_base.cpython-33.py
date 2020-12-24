# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_integraion_base.py
# Compiled at: 2013-11-10 14:30:06
# Size of source mod 2**32: 1628 bytes
import os, logging, unittest, sys, time
from nose import SkipTest
from arango.core import Connection
logger = logging.getLogger(__name__)
__all__ = ('TestsIntegration', )
DEFAULT_TIMEOUT = 0.2

class TestsIntegration(unittest.TestCase):
    __doc__ = '\n    This suite shoudl work with real ArangoDB instance\n    so make sure that db is running and available\n    on http://localhost:8529\n    '

    def setUp(self):
        if 'INTEGRATION' not in os.environ:
            raise SkipTest
        self.conn = Connection(db='test')
        self.conn.database.create()
        if 'DEBUG_HTTP' in os.environ:
            self.conn.client.DEBUG = True
        if 'USE_CLIENT' in os.environ:
            module_path = os.environ['USE_CLIENT'].split('.')
            client_cls = module_path.pop()
            if sys.version_info.major == 3 or hasattr(sys, 'pypy_version_info'):
                if 'pycurl' in client_cls.lower():
                    raise SkipTest
            module = __import__('.'.join(module_path))
            for c_module in module_path[1:]:
                module = getattr(module, c_module)

            self.conn.client = getattr(module, client_cls)

    def tearDown(self):
        c = self.conn
        logger.info("Deleting/Cleaning up collection 'test'")
        c.database.delete()

    def wait(self, times=1):
        """
        Waiting for async actions ``times`` times
        """
        for c in range(times):
            time.sleep(DEFAULT_TIMEOUT)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\test.py
# Compiled at: 2011-01-03 17:15:12
"""
SeisHub's test runner.

This script will run every test included into SeisHub.
"""
from seishub.core.config import Configuration
from seishub.core.db import DEFAULT_PREFIX
from seishub.core.env import Environment
import copy, doctest, sys, unittest
USE_TEST_DB = 'sqlite://'
CHECK_DATABASE = False
CLEAN_DATABASE = True
DISPOSE_CONNECTION = False
VERBOSE_DATABASE = False

class SeisHubEnvironmentTestCase(unittest.TestCase):
    """
    Generates a temporary SeisHub environment without any service.
    
    We generate a temporary configuration file, an environment object and 
    disable logging at all. Any class inheriting from this test case may 
    overwrite the _config method to preset additional options to the test 
    environment.
    
    Don't ever overwrite the __init__ or run methods!
    """

    def __init__(self, methodName='runTest', filename=None):
        """
        Initialize the test procedure.
        """
        unittest.TestCase.__init__(self, methodName)
        self.default_config = Configuration()
        self.default_config.set('seishub', 'log_level', 'OFF')
        self.default_config.set('seishub', 'auth_uri', 'sqlite://')
        self.default_config.set('db', 'uri', USE_TEST_DB)
        self.default_config.set('db', 'verbose', VERBOSE_DATABASE)

    def _config(self):
        """
        Method to write into the temporary configuration file.
        
        This method may be overwritten from any test case to set up 
        configuration parameters needed for the test case.
        """
        pass

    def __setUp(self):
        """
        Sets the environment up before each test case.
        """
        self.config = copy.copy(self.default_config)
        self._config()
        self.config.save()
        self.env = Environment('', config_file=self.config, log_file=None)
        self.env.initComponent(self)
        if CHECK_DATABASE:
            self.tables = {}
            sql = 'SELECT * FROM %s;'
            tables = self.env.db.engine.table_names()
            tables = [ t for t in tables if t.startswith(DEFAULT_PREFIX) ]
            for table in tables:
                res = self.env.db.engine.execute(sql % str(table)).fetchall()
                self.tables[table] = len(res)

        return

    def __tearDown(self):
        """
        Clean up database and remove environment objects after each test case.
        """
        if CHECK_DATABASE:
            sql = 'SELECT * FROM %s;'
            tables = self.env.db.engine.table_names()
            tables = [ t for t in tables if t.startswith(DEFAULT_PREFIX) ]
            for table in tables:
                res = self.env.db.engine.execute(sql % str(table)).fetchall()
                if len(res) != self.tables.get(table):
                    print 'table %s: %d!=%d in %s' % (table,
                     self.tables.get(table),
                     len(res), str(self))

        if CLEAN_DATABASE:
            if USE_TEST_DB.startswith('postgres'):
                sql = 'DROP TABLE %s CASCADE;'
            else:
                sql = 'DROP TABLE %s;'
            tables = self.env.db.engine.table_names()
            tables = [ t for t in tables if t.startswith(DEFAULT_PREFIX) ]
            for table in tables:
                self.env.db.engine.execute(sql % str(table))

        if DISPOSE_CONNECTION:
            self.env.db.engine.pool.dispose()
        del self.config
        del self.env

    def run(self, result=None):
        """
        Shameless copy of unittest.TestCase.run() adopted for our uses.
        """
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        testMethod = getattr(self, self._testMethodName)
        self.__setUp()
        try:
            try:
                self.setUp()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())
                return

            ok = False
            try:
                testMethod()
                ok = True
            except self.failureException:
                result.addFailure(self, self._exc_info())
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())

            try:
                self.tearDown()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())
                ok = False

            if ok:
                result.addSuccess(self)
        finally:
            result.stopTest(self)

        self.__tearDown()
        return


def getSuite():
    """
    This methods calls all test suites.
    """
    from seishub.core.registry.tests import suite as registry_suite
    from seishub.core.processor.tests import suite as processor_suite
    from seishub.core.tests import suite as tests_suite
    from seishub.core.util.tests import suite as util_suite
    from seishub.core.xmldb.tests import suite as xmldb_suite
    from seishub.core.db.tests import suite as db_suite
    suite = unittest.TestSuite()
    suite.addTest(registry_suite())
    suite.addTest(processor_suite())
    suite.addTest(tests_suite())
    suite.addTest(util_suite())
    suite.addTest(xmldb_suite())
    suite.addTest(db_suite())
    return suite


if __name__ == '__main__':
    doctest.testmod(sys.modules[__name__])
    unittest.main(module='seishub.core.test', defaultTest='getSuite')
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testAnalysisModules.py
# Compiled at: 2010-09-28 19:45:04
"""
Programmatic tests of analysis modules
"""
import logging, unittest
from netlogger import module_util as mu
from netlogger.tests import shared
from netlogger.analysis.modules._base import ConnectionException
MOD_BASE = 'netlogger.analysis.modules.'

class TestCase(shared.BaseTestCase):
    THIRD_PARTY = ('couchdb', 'mongodb', 'stampede_loader')

    def setUp(self):
        self.modules = mu.list_modules('analysis', 'modules')

    def testLoad(self):
        """Load each found module
        """
        for name in self.modules:
            try:
                module = mu.load_module(MOD_BASE + name)
            except mu.ModuleLoadError:
                if name in self.THIRD_PARTY:
                    self.log.warn('Could not load module with third-party dependencies: %s' % name)

    def testBadLoad(self):
        """Try to load a nonexistent module and catch the failure.
        """
        name = 'extremely_bogus'
        self.failUnlessRaises(mu.ModuleNotFound, mu.load_module, MOD_BASE + name)

    def testInfo(self):
        """Load each module and get the 'info string' for the main
        analysis class.
        """
        for name in self.modules:
            try:
                module = mu.load_module(MOD_BASE + name)
                info = mu.module_info('test', 'foo', module.Analyzer)
            except mu.ModuleLoadError:
                if name in self.THIRD_PARTY:
                    self.log.warn('Could not load module with third-party dependencies: %s' % name)

    def testMongodb(self):
        """Test mongodb loader - skip test if not available.
        """
        try:
            import pymongo
        except:
            self.log.warn('pymongo import failed, skipping test')
            return
        else:
            module = mu.load_module(MOD_BASE + 'mongodb')
            (db, coll) = ('test', 'testAnalysisModules')
            try:
                aclass = module.Analyzer(database=db, collection=coll)
            except ConnectionException:
                self.log.warn('connect.failed', msg='connect to mongo on localhost and default port failed, skipping test')
                return

        try:
            for i in xrange(10):
                event = {'ts': 1276321526 + i / 10, 'event': 'test', 
                   'value': i, 
                   'my.id': 10 * i}
                aclass.process(event)

        finally:
            aclass.connection.drop_database(db)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/storage/test/test_dbm.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.core.storage.dbm}.
"""
import os, os.path, shutil
from zope.interface import verify as ziv
from twisted.trial import unittest
from spamfighter.interfaces import IExpirableStorage, IPersistentStorage, IDomainBindable
from spamfighter.core.storage.dbm import DBMStorage, DomainedDBMStorage
from spamfighter.core.storage.test.base import ExpirableStorageTestMixin
from spamfighter.core.domain import getDefaultDomain
from spamfighter.utils import config

class DBMStorageTestCase(unittest.TestCase, ExpirableStorageTestMixin):
    """
    Тест на L{spamfighter.core.storage.dbm.DBMStorage}.
    """

    def setUp(self):
        if not os.path.exists(config.storage.dbm.path):
            os.makedirs(config.storage.dbm.path)
        ExpirableStorageTestMixin.setUp(self)
        self.s = DBMStorage('testing', 't')

    def tearDown(self):
        shutil.rmtree(config.storage.dbm.path)
        ExpirableStorageTestMixin.tearDown(self)

    def testInterface(self):
        ziv.verifyClass(IPersistentStorage, DBMStorage)
        ziv.verifyClass(IExpirableStorage, DBMStorage)


class DomainedDBMStorageTestCase(unittest.TestCase, ExpirableStorageTestMixin):
    """
    Тест на L{spamfighter.core.storage.dbm.DomainedDBMStorage}.
    """

    def setUp(self):
        if not os.path.exists(config.storage.dbm.path):
            os.makedirs(config.storage.dbm.path)
        ExpirableStorageTestMixin.setUp(self)
        self.s = DomainedDBMStorage()
        self.s.bind(getDefaultDomain(), 'testDBM')

    def tearDown(self):
        shutil.rmtree(config.storage.dbm.path)
        ExpirableStorageTestMixin.tearDown(self)

    def testInterface(self):
        ziv.verifyClass(IExpirableStorage, DomainedDBMStorage)
        ziv.verifyClass(IPersistentStorage, DomainedDBMStorage)
        ziv.verifyClass(IDomainBindable, DomainedDBMStorage)

    def testPickling(self):
        import pickle
        s2 = pickle.loads(pickle.dumps(self.s))
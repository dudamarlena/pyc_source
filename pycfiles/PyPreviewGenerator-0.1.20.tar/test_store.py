# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pypreval/test_store.py
# Compiled at: 2008-02-21 08:24:58
__doc__ = '\nUnittests for pypreval.store\n'
from __future__ import absolute_import
from .store import Store
import shutil, os

class AppendRootTransaction(object):
    """this transaction appends to the root object."""

    def __init__(self, newvalue):
        self._newvalue = newvalue

    def __call__(self, store):
        store.root.append(self._newvalue)


class ReplaceRootTransaction(object):
    """this transaction replaces the root object completely"""

    def __init__(self, newvalue):
        self._newvalue = newvalue

    def __call__(self, store):
        store.root = self._newvalue


class TestBasicStoreOperations:

    def setUp(self):
        self.store = Store('test_store.dir')

    def tearDown(self):
        shutil.rmtree('test_store.dir')

    def test_basic_op(self):
        """tests basic working of transaction submission, plus replay of transactions"""
        assert self.store.root is None
        self.store.submit_transaction(ReplaceRootTransaction(123))
        assert self.store.root == 123
        self.store.submit_transaction(ReplaceRootTransaction(456))
        assert self.store.root == 456
        self.store.submit_transaction(ReplaceRootTransaction(457))
        assert self.store.root == 457
        store2 = Store('test_store.dir')
        assert store2.root == 457
        return

    def test_append_op(self):
        """tests that transactions do not get applied twice, and snapshots"""
        assert self.store.root is None
        self.store.submit_transaction(ReplaceRootTransaction([]))
        assert self.store.root == []
        self.store.submit_transaction(AppendRootTransaction(456))
        assert self.store.root == [456]
        self.store.submit_transaction(AppendRootTransaction(457))
        assert self.store.root == [456, 457]
        store2 = Store('test_store.dir')
        assert store2.root == [456, 457]
        store2.save_snapshot()
        store3 = Store('test_store.dir')
        assert store3.root == [456, 457]
        print os.listdir('test_store.dir')
        assert os.path.exists(os.path.join('test_store.dir', 'snap.3'))
        return
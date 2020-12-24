# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/test/base.py
# Compiled at: 2008-01-19 12:32:25
"""Base functions and classes for SchevoPolicy tests.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from dispatch import generic
import louie, schevo
from schevo.change import Distributor
import schevo.icon
from schevo.test import CreatesSchema
from schevo.test.test_change import BaseDistributor
from schevo.test.test_icon import BaseFsIconMap, TEST_ICONS
from schevopolicy.schema import policy_from_string
ALLOW_ALL = '\n    # Allow all operations by default.\n    default = ALLOW\n\n    # Do not override any allowance.\n    '
NO_CONTEXT = None

@generic()
def class_with_policy(base_class):
    """Return a test class based on base_class that patches it to use
    a restricted database."""
    pass


@class_with_policy.when('issubclass(base_class, CreatesSchema)')
def class_with_policy_CreatesSchema(base_class):

    class TestClass(base_class):
        _use_db_cache = False

        def _open(self, suffix='', reopening=False):
            db = super(TestClass, self)._open(suffix)
            db_name = 'db' + suffix
            ex_name = 'ex' + suffix
            orig_db_name = 'orig_db' + suffix
            policy = policy_from_string(db, ALLOW_ALL)
            rdb = policy(NO_CONTEXT)
            setattr(self, orig_db_name, db)
            setattr(self, db_name, rdb)
            modname = base_class.__module__
            mod = sys.modules[modname]
            setattr(mod, db_name, rdb)
            setattr(mod, ex_name, rdb.execute)
            return rdb

    TestClass.__name__ = 'Test' + base_class.__name__[4:]
    return TestClass


@class_with_policy.when('issubclass(base_class, BaseDistributor)')
def class_with_policy_BaseFsDistributor(base_class):
    base_class = class_with_policy_CreatesSchema(base_class)

    class TestClass(base_class):

        def setUp(self):
            CreatesSchema.setUp(self)
            louie.reset()
            self.orig_db.dispatch = True
            dist = self.dist = Distributor(self.orig_db)

    TestClass.__name__ = 'Test' + base_class.__name__[4:]
    return TestClass


@class_with_policy.when('issubclass(base_class, BaseFsIconMap)')
def class_with_policy_BaseFsIconMap(base_class):
    base_class = class_with_policy_CreatesSchema(base_class)

    class TestClass(base_class):

        def setUp(self):
            CreatesSchema.setUp(self)
            schevo.icon.install(self.orig_db, TEST_ICONS)

    TestClass.__name__ = 'Test' + base_class.__name__[4:]
    return TestClass


optimize.bind_all(sys.modules[__name__])
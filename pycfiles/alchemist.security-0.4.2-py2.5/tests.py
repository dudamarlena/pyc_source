# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/alchemist/security/tests.py
# Compiled at: 2008-09-11 08:15:48
import unittest, transaction
from zope.testing import doctest, doctestunit
from zope.securitypolicy.interfaces import Allow, Deny, Unset
from ore.alchemist import Session
from sqlalchemy import orm
import sqlalchemy as rdb

def setUp(test):
    pass


def tearDown(test):
    orm.clear_mappers()


def test_suite():
    doctests = ('role.txt', 'permission.txt')
    globs = dict(Session=Session, Allow=Allow, Deny=Deny, rdb=rdb, transaction=transaction, orm=orm)
    return unittest.TestSuite((doctestunit.DocFileSuite(filename, setUp=setUp, tearDown=tearDown, globs=globs, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS) for filename in doctests))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
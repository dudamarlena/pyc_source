# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/test/testSAProviderReflected.py
# Compiled at: 2008-06-30 11:43:30
from dbsprockets.test.base import setupDatabase, setupReflection, teardownDatabase
from dbsprockets.test.testSAProvider import _TestSAProvider

def setup():
    setupDatabase()
    setupReflection()


def teardown():
    teardownDatabase()


class TestSAProviderReflected(_TestSAProvider):
    pass
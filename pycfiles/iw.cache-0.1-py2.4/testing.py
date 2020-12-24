# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/testing.py
# Compiled at: 2007-12-05 09:41:22
"""
testing framework
"""
__docformat__ = 'restructuredtext'
from zope.testing.cleanup import CleanUp
from zope.configuration.xmlconfig import XMLConfig

def clearZCML(test=None):
    cacheTearDown()
    cacheSetUp()
    import iw.cache
    XMLConfig('meta.zcml', iw.cache)()
    import iw.cache.tests
    XMLConfig('servers.zcml', iw.cache.tests)()


def cacheSetUp(test=None):
    CleanUp().setUp()


def cacheTearDown(test=None):
    CleanUp().tearDown()
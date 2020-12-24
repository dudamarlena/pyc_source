# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xanalogica/tumbler/tests.py
# Compiled at: 2008-08-31 04:10:13
import os, re, unittest, pkg_resources
from zope.testing import doctest, renormalizing

def test_suite():
    global __test__
    __test__ = dict(README=pkg_resources.resource_string(__name__, 'Tumblers.txt'))
    return doctest.DocTestSuite(checker=renormalizing.RENormalizing([
     (
      re.compile('\\S+%(sep)s\\w+%(sep)s\\w+.fs' % dict(sep=os.path.sep)),
      '/tmp/data/Data.fs'),
     (
      re.compile('\\S+sample-(\\w+)'), '/sample-\\1')]))
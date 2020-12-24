# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/tests/test_nodevisitor.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import doctest, unittest

def test_suite():
    return unittest.TestSuite((
     doctest.DocFileSuite('../visitors/nodevisitor.py', optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))
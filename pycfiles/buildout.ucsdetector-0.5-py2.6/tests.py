# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/buildout/ucsdetector/tests.py
# Compiled at: 2010-04-05 18:46:39
import doctest, zc.buildout.testing

def test_suite():
    OPTIONFLAGS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    suite = doctest.DocFileSuite('README.txt', setUp=zc.buildout.testing.buildoutSetUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=OPTIONFLAGS)
    return suite
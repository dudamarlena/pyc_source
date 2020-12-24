# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/buildout/ucsdetector/tests.py
# Compiled at: 2010-04-05 18:46:39
import doctest, zc.buildout.testing

def test_suite():
    OPTIONFLAGS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    suite = doctest.DocFileSuite('README.txt', setUp=zc.buildout.testing.buildoutSetUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=OPTIONFLAGS)
    return suite
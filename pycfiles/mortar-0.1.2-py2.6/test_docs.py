# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/tests/test_docs.py
# Compiled at: 2009-08-11 09:00:51
import unittest
from glob import glob
from os.path import dirname, join, pardir
from zope.testing.doctest import DocFileSuite, REPORT_NDIFF, ELLIPSIS

def test_suite():
    return DocFileSuite(optionflags=(REPORT_NDIFF | ELLIPSIS), module_relative=False, *glob(join(dirname(__file__), pardir, 'docs', '*.txt')))
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/tests/test_doctests.py
# Compiled at: 2008-10-10 10:13:58
"""
Running doctests
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import os, glob, doctest, unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from iw.sitestat.tests.base import sitestatFunctionalTestCase
from iw.sitestat.config import PRODUCTNAME, HAVE_COLLAGE, HAVE_PLONEARTICLE, HAVE_SIMPLEALIAS
OPTIONFLAGS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

def list_doctests():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    filenames = [ filename for filename in glob.glob(os.path.join(this_dir, 'test*.txt')) ]
    for (haveit, doctestfile) in [(HAVE_COLLAGE, 'test_collage_linksfinder.txt'), (HAVE_PLONEARTICLE, 'test_plonearticle_linksfinder.txt'), (HAVE_SIMPLEALIAS, 'test_simplealias_linksfinder.txt')]:
        if not haveit:
            filenames = [ filename for filename in filenames if not filename.endswith(doctestfile) ]

    return filenames


def test_suite():
    return unittest.TestSuite([ Suite(os.path.basename(filename), optionflags=OPTIONFLAGS, package=PRODUCTNAME + '.tests', test_class=sitestatFunctionalTestCase) for filename in list_doctests() ])
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/dist/tests/test_mupload.py
# Compiled at: 2008-03-20 05:18:16
"""Tests for distutils.command.upload."""
import sys, os, unittest
from iw.dist.mupload import mupload
from distutils.core import Distribution
from distutils.tests import support
from iw.dist.tests.test_pypirc import PYPIRC, PyPIRCCommandTestCase

class uploadTestCase(PyPIRCCommandTestCase):
    __module__ = __name__

    def test_finalize_options(self):
        f = open(self.rc, 'w')
        f.write(PYPIRC)
        f.close()
        dist = Distribution()
        cmd = mupload(dist)
        cmd.finalize_options()
        for (attr, waited) in (('username', 'me'), ('password', 'secret'), ('realm', 'pypi'), ('repository', 'http://pypi.python.org/pypi')):
            self.assertEquals(getattr(cmd, attr), waited)


def test_suite():
    return unittest.makeSuite(uploadTestCase)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
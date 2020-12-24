# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pypreval/test_util.py
# Compiled at: 2008-02-20 18:10:37
__doc__ = '\nThe unittests for the pypreval.util module.\n'
from __future__ import absolute_import
from .util import optional_makedirs
from nose.tools import assert_raises
import errno, os

class TestOptionalMakeDirs(object):
    """test pypreval.util.optional_makedirs"""

    def setUp(self):
        self.path = os.path.join('AAA', 'BBB')

    def tearDown(self):
        work = [
         (
          os.unlink, self.path),
         (
          os.rmdir, self.path),
         (
          os.unlink, os.path.dirname(self.path)),
         (
          os.rmdir, os.path.dirname(self.path))]
        for (func, arg) in work:
            try:
                func(arg)
            except os.error:
                pass

    def test_already_existing(self):
        """tests that calling optional_makedirs with the same path twice does not raise any errors"""
        optional_makedirs(self.path)
        optional_makedirs(self.path)

    def test_file_in_path(self):
        """tests that optional_makedirs raises os.error when one of the intervening directories is a file in truth."""
        file(os.path.dirname(self.path), 'w').close()
        assert_raises(os.error, optional_makedirs, self.path)
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pypreval/test_util.py
# Compiled at: 2008-02-20 18:10:37
"""
The unittests for the pypreval.util module.
"""
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
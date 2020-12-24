# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kstreitova/GitProjects/SUSE/spec-cleaner/tests/fileutils-tests.py
# Compiled at: 2019-09-26 08:32:57
# Size of source mod 2**32: 757 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from spec_cleaner import RpmException
from spec_cleaner.fileutils import open_datafile, open_stringio_spec

class TestFileutils(object):
    __doc__ = '\n    We run few tests to ensure fileutils class works fine\n    '

    def test_open_assertion(self):
        with pytest.raises(RpmException):
            open_stringio_spec('missing-file.txt')

    def test_open_datafile_assertion(self):
        with pytest.raises(RpmException):
            open_datafile('missing-file.txt')

    def test_open(self):
        data = open_stringio_spec('tests/fileutils-tests.py')
        data.close()

    def test_open_datafile(self):
        data = open_datafile('excludes-bracketing.txt')
        data.close()
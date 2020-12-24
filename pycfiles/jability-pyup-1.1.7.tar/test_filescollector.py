# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/test_filescollector.py
# Compiled at: 2013-05-25 04:38:30
import filescollector
from filescollector import *
import os, test_common

def test_clean_olders():
    files = test_common.init_dir()
    assert test_common.count_existing_files(files) == test_common.test_qty
    fcollector = FilesCollector()
    fcollector.setSourceDir(test_common.tests_dir)
    fcollector.setFileFilter('^.*\\.tmp$')
    files = fcollector.run(True)
    assert test_common.count_existing_files(files) == test_common.test_qty
    test_common.clean_dir(files)
    assert test_common.count_existing_files(files) == 0


def test_minimumFileAge():
    files = test_common.init_dir(False)
    assert test_common.count_existing_files(files) == test_common.test_qty
    fcollector = FilesCollector()
    fcollector.setSourceDir(test_common.tests_dir)
    fcollector.setFileFilter('^.*\\.tmp$')
    fcollector.setMinimumFileLastChangeAge(15)
    files = fcollector.run(True)
    assert test_common.count_existing_files(files) == 7
    test_common.clean_dir(files)


if __name__ == '__main__':
    import doctest, nose
    doctest.testmod(filescollector)
    nose.main()
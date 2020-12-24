# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/test_dircleaner.py
# Compiled at: 2013-05-25 04:38:30
import dircleaner
from dircleaner import *
import os, test_common

def test_clean_olders():
    files = test_common.init_dir()
    assert test_common.count_existing_files(files) == test_common.test_qty
    dc = dirCleaner(test_common.tests_dir)
    dc.setCleanLastest(True, 8)
    dc.clean()
    assert test_common.count_existing_files(files) == 8
    assert os.path.exists(files[0]) == True
    assert os.path.exists(files[7]) == True
    assert os.path.exists(files[9]) == False
    test_common.clean_dir(files)
    assert test_common.count_existing_files(files) == 0


def test_clean_lastests():
    files = test_common.init_dir()
    assert test_common.count_existing_files(files) == test_common.test_qty
    dc = dirCleaner(test_common.tests_dir)
    dc.setFilter('^.*\\.tmp$')
    dc.setCleanLastest(False, 2)
    dc.clean()
    assert test_common.count_existing_files(files) == 2
    assert os.path.exists(files[1]) == True
    assert os.path.exists(files[3]) == False
    test_common.clean_dir(files)
    assert test_common.count_existing_files(files) == 0


if __name__ == '__main__':
    import doctest, nose
    doctest.testmod(dircleaner)
    nose.main()
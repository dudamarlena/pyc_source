# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/test_timeflag.py
# Compiled at: 2013-05-25 04:38:30
__author__ = 'Fabrice Romand'
__copyright__ = 'Copyleft 2008 - Fabrice Romand'
__credits__ = ['Fabrice Romand']
__license__ = 'GPL'
__version__ = '1.1'
__maintainer__ = 'Fabrice Romand'
__email__ = 'fabrom@jability.org'
__status__ = 'Development'
import timeflag
from timeflag import *
import os, shutil
from test_common import *
flag_format = '%Y%m%d'
flag_dir = tests_dir
flag_name = 'test_timeflag'
flag_extension = 'dat'
timeflag_toupdate_name = 'test_timeflag'
timeflag_toupdate_path = os.path.join(module_dir, flag_dir, '..', timeflag_toupdate_name + os.extsep + flag_extension)

def test_set():
    init_dir()
    dc = timeFlag(flag_dir, flag_name, flag_extension)
    now = now_str(flag_format)
    dc.setFormat(flag_format)
    assert dc.get() == now
    assert dc.getdiff() == (0, 0, 0, 0)
    assert dc.isuptodate() == True


def test_delete():
    init_dir()
    dc = timeFlag(flag_dir, flag_name, flag_extension)
    dc.update()
    assert os.path.exists(os.path.join(flag_dir, flag_name + os.extsep + flag_extension)) == True
    dc.delete()
    assert os.path.exists(os.path.join(flag_dir, flag_name + os.extsep + flag_extension)) == False


def test_update():
    init_dir()
    now = now_str(flag_format)
    assert os.path.exists(timeflag_toupdate_path) == True
    shutil.copy(timeflag_toupdate_path, flag_dir)
    assert os.path.exists(os.path.join(flag_dir, timeflag_toupdate_name + os.extsep + flag_extension)) == True
    dc = timeFlag(flag_dir, timeflag_toupdate_name, flag_extension)
    dc.setFormat(flag_format)
    dc.update()
    assert dc.get() == now
    dc.delete()
    assert os.path.exists(os.path.join(flag_dir, timeflag_toupdate_name + os.extsep + flag_extension)) == False


if __name__ == '__main__':
    import doctest, nose
    doctest.testmod()
    nose.main()
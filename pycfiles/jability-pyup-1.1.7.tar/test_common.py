# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/test_common.py
# Compiled at: 2013-05-25 04:38:30
import datetime, os, shutil, time
module_dir = os.path.dirname(__file__)
tests_dir = os.path.join(module_dir, 'tests/temp/')
test_filename_template = 'test_%d.tmp'
test_qty = 10

def now():
    return datetime.datetime.now()


def now_str(format='%Y%m%d%H%M%S'):
    return now().strftime(format)


def def_times(qty, daytimedelta=True):
    today = now()
    tlist = list()
    if daytimedelta:
        for i in range(qty):
            pastday = today - datetime.timedelta(days=i)
            atime = int(time.mktime(pastday.timetuple()))
            mtime = atime
            times = (atime, mtime)
            tlist.append(times)

    else:
        for i in range(qty):
            pastday = today - datetime.timedelta(minutes=i * 5)
            atime = int(time.mktime(pastday.timetuple()))
            mtime = atime
            times = (atime, mtime)
            tlist.append(times)

    return tlist


def init_dir(daydelta=True):
    shutil.rmtree(tests_dir)
    if not os.path.exists(tests_dir):
        os.makedirs(tests_dir)
    i = 0
    flist = list()
    for times in def_times(test_qty, daydelta):
        fpath = os.path.join(tests_dir, test_filename_template % i)
        open(fpath, 'w').close()
        os.utime(fpath, times)
        i += 1
        flist.append(fpath)

    return flist


def clean_dir(flist, delete_base_dir=False):
    for file in flist:
        if os.path.exists(file):
            os.remove(file)

    if delete_base_dir:
        os.rmdir(tests_dir)


def count_existing_files(flist):
    i = 0
    for file in flist:
        if os.path.exists(file):
            i += 1

    return i


def test_tests_functions():
    files = init_dir()
    assert count_existing_files(files) == test_qty
    clean_dir(files)
    assert count_existing_files(files) == 0


if __name__ == '__main__':
    import doctest, nose
    doctest.testmod()
    nose.main()
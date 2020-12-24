# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/pytests/uedge_test.py
# Compiled at: 2019-07-11 16:53:00
import os, contextlib, unittest
print 'in uedge_test'

@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


try:
    if os.path.exists('pytests/level_1/dotest.py'):
        with pushd('pytests/level_1'):
            execfile('dotest.py')
except:
    pass

try:
    if os.path.exists('pytests/level_2/dotest.py'):
        with pushd('pytests/level_2'):
            execfile('dotest.py')
except:
    pass
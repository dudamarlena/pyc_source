# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/tests/util.py
# Compiled at: 2012-01-22 12:14:35
import contextlib, os

def remove(path):
    try:
        os.remove(path)
    except OSError:
        pass


@contextlib.contextmanager
def temp_file(filename):
    with open(filename, 'w') as (f):
        f.write('asdfasdf')
    yield
    remove(filename)
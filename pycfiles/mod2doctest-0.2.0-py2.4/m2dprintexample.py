# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\m2dprintexample.py
# Compiled at: 2009-11-09 10:23:18
if __name__ == '__main__':
    import mod2doctest
    mod2doctest.convert(src=None, target='m2dprintexample_test.py', run_doctest=True, add_testmod=True)
from mod2doctest import m2d_print
m2d_print.h1('TEST_SETUP')
import pickle, os
m2d_print.h1('TEST_TEARDOWN')
import sys
del sys.modules['pickle']
print sys.modules.keys()
m2d_print.h2('GOING TO DO IT')
print 'foobar'
m2d_print.h2('GOING TO DO IT')
print 'baz'
m2d_print.h3('NOW YOU WILL SEE IT')
print 'foobarbaz'
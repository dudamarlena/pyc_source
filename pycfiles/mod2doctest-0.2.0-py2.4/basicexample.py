# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\basicexample.py
# Compiled at: 2009-11-09 02:09:08
if __name__ == '__main__':
    import mod2doctest
    mod2doctest.convert(src=None, target='basicexample_test.py', run_doctest=True, add_testmod=True)
import pickle, os
alist = [
 1, -4, 50] + list(set([10, 10, 10]))
alist.sort()
print alist
print `(pickle.dumps(alist))`

class Foo(object):
    __module__ = __name__


print Foo()
print pickle
os.getcwd()
try:
    print pickle.dumps(os)
except TypeError, e:
    print 'ERROR!', e
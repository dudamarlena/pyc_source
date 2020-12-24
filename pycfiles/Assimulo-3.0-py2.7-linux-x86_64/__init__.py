# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/__init__.py
# Compiled at: 2017-12-28 04:09:42


def testattr(**kwargs):
    """Add attributes to a test function/method/class.
    
    This function is needed to be able to add
      @attr(slow = True)
    for functions.
    
    """

    def wrap(func):
        func.__dict__.update(kwargs)
        return func

    return wrap


try:
    import os
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    _fpath = os.path.join(curr_dir, 'version.txt')
    with open(_fpath, 'r') as (f):
        __version__ = f.readline().strip()
        __revision__ = f.readline().strip()
except:
    __version__ = 'unknown'
    __revision__ = 'unknown'
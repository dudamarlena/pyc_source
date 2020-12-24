# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/test_lockflag.py
# Compiled at: 2013-05-25 04:38:30
__author__ = 'Fabrice Romand'
__copyright__ = 'Copyleft 2010 - Fabrice Romand'
__credits__ = ['Fabrice Romand']
__license__ = 'GPL'
__version__ = '1.1'
__maintainer__ = 'Fabrice Romand'
__email__ = 'fabrom@jability.org'
__status__ = 'Development'
import lockflag
from lockflag import *
import os

def test_lockflag():
    dc = lockFlag(str(os.getpid()), 'tmp')
    assert dc.create() == True
    assert os.path.exists(dc.fullpath) == True
    assert dc.exists() == True
    assert dc.create() == False
    dc.delete()
    assert dc.exists() == False


if __name__ == '__main__':
    import doctest, nose
    doctest.testmod()
    nose.main()
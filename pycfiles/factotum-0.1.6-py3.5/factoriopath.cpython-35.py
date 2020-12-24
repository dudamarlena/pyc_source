# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/factotum/factoriopath.py
# Compiled at: 2017-01-20 23:30:04
# Size of source mod 2**32: 748 bytes
"""
This is the factoriopath module. 

It looks for a .factorioPath in $HOME, but otherwise tries to figure out the best place for a factorio install.

"""
import os

def getFactorioPath():
    try:
        with open('%s/.factorioPath' % os.path.expanduser('~'), 'r') as (data_file):
            path = data_file.readline().strip()
    except:
        print('%s/.factorioPath not found. Using default.' % os.path.expanduser('~'))
        if os.path.isdir('/opt/factorio'):
            path = '/opt/factorio'
        else:
            if os.access('/opt', os.W_OK):
                path = '/opt/factorio'
            else:
                path = '%s/factorio' % os.path.expanduser('~')

    return path


if __name__ == '__main__':
    import doctest
    doctest.testmod()
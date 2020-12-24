# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/nosetests.py
# Compiled at: 2018-03-12 09:48:15
# Size of source mod 2**32: 169 bytes
__doc__ = 'Nosetests Configuration File'
import os
from nose import main
if __name__ == '__main__':
    os.chdir('tests')
    main()
    os.chdir('..')
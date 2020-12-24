# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dobg/exceptions/dropletexceptions.py
# Compiled at: 2019-07-20 11:37:22
# Size of source mod 2**32: 134 bytes
import sys
sys.path.append('..')

class InvalidIdException(Exception):

    def __str__(self):
        return 'Invalid Droplet ID.'
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/modules/temp.py
# Compiled at: 2020-04-30 16:03:58
# Size of source mod 2**32: 448 bytes
import os

def write_file(filename):
    """write a file with some random nonsense"""
    with open(filename, 'w') as (filey):
        filey.write('I heard there was an octupus living in that Christmas tree.')


def create_directory(dirname):
    """create a directory named according to input variable dirname"""
    if not os.path.exists(dirname):
        os.mkdir(dirname)
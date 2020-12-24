# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pysecret/helper.py
# Compiled at: 2019-04-10 20:34:51
import os
HOME = os.path.expanduser('~')

def home_file_path(*args):
    return os.path.join(HOME, *args)
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/helper.py
# Compiled at: 2019-04-10 20:34:51
# Size of source mod 2**32: 153 bytes
import os
HOME = os.path.expanduser('~')

def home_file_path(*args):
    return (os.path.join)(HOME, *args)
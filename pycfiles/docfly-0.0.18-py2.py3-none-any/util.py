# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: docfly/util.py
# Compiled at: 2020-03-21 11:28:22
"""
utilities.
"""
from __future__ import print_function, unicode_literals
import os

def make_dir(abspath):
    """
    Make an empty directory.
    """
    try:
        os.mkdir(abspath)
        print(b'Made: %s' % abspath)
    except:
        pass


def make_file(abspath, text):
    """
    Make a file with utf-8 text.
    """
    try:
        with open(abspath, b'wb') as (f):
            f.write(text.encode(b'utf-8'))
        print(b'Made: %s' % abspath)
    except:
        pass
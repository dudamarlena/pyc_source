# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/ome/omero-figure/omero_figure/utils.py
# Compiled at: 2020-01-13 09:39:37
# Size of source mod 2**32: 977 bytes
import json, os
__version__ = '4.2.0'

def read_file(fname, content_type=None):
    p = os.path.abspath(fname)
    with open(p) as (f):
        if content_type in ('json', ):
            data = json.load(f)
        else:
            data = f.read()
    return data
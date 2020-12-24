# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/.vv/lib/python2.7/site-packages/yamli.py
# Compiled at: 2015-05-25 17:46:12
"""
yaml + includes
"""
from yaml import *
import os.path
_root = os.path.curdir

def _include(loader, node):
    """Include another YAML file."""
    global _root
    old_root = _root
    filename = os.path.join(root, loader.construct_scalar(node))
    _root = os.path.split(filename)[0]
    data = load(open(filename, 'r'))
    _root = old_root
    return data


add_constructor('!include', _include)
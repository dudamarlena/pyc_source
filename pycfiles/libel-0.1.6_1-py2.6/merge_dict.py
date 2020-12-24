# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libel/merge_dict.py
# Compiled at: 2010-08-29 19:05:39


def merge_dict(Left, Right):
    """
    Merge Right dictionary into Left
    """
    if not Right:
        return
    for key in Right:
        if isinstance(Right[key], dict) and Left.has_key(key):
            merge_dict(Left[key], Right[key])
        else:
            Left[key] = Right[key]
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/diff_and_patch/utils.py
# Compiled at: 2018-08-26 08:43:24
# Size of source mod 2**32: 207 bytes
import inspect

def fully_qualified_name(obj):
    if not inspect.isclass(obj):
        _obj = obj.__class__
    else:
        _obj = obj
    return '{m}.{kls}'.format(m=(_obj.__module__), kls=(_obj.__name__))
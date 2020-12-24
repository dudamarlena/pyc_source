# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jphillips/go/src/github.com/lyft/toasted-marshmallow/toastedmarshmallow/compat.py
# Compiled at: 2019-06-13 15:03:45
# Size of source mod 2**32: 486 bytes
import sys
if sys.version_info[0] >= 3:

    def is_overridden(instance_func, class_func):
        return instance_func.__func__ is not class_func


else:

    def is_overridden(instance_func, class_func):
        return instance_func.__func__ is not class_func.__func__
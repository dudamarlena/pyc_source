# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DJANGO-WORKON/workon/utils/types.py
# Compiled at: 2018-02-21 01:52:45
# Size of source mod 2**32: 151 bytes
from types import *

def is_lambda(value):
    return isinstance(value, LambdaType)


def is_method(value):
    return isinstance(value, MethodType)
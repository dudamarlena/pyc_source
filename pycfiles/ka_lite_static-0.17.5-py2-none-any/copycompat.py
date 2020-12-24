# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/copycompat.py
# Compiled at: 2018-07-11 18:15:30
"""
Fixes Python 2.4's failure to deepcopy unbound functions.
"""
import copy, types, warnings
warnings.warn('django.utils.copycompat is deprecated; use the native copy module instead', DeprecationWarning)
if hasattr(copy, '_deepcopy_dispatch') and types.FunctionType not in copy._deepcopy_dispatch:
    copy._deepcopy_dispatch[types.FunctionType] = copy._deepcopy_atomic
del copy
del types
from copy import *
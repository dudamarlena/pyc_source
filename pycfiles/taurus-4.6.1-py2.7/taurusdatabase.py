# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/taurusdatabase.py
# Compiled at: 2019-08-19 15:09:29
"""Do not use. Deprecated. Backwards compatibility module for transition from
TaurusDatabase to TaurusAuthority"""
from logging import warn
warn('taurusdatabase module is deprecated. Use taurusauthority instead')
import traceback
traceback.print_stack()
from .taurusauthority import *
TaurusDatabase = TaurusAuthority
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/tools/nameit/core/lib.py
# Compiled at: 2020-04-11 22:34:33
# Size of source mod 2**32: 347 bytes
"""
Module that contains base naming library for tpDcc-tools-nameit
"""
from __future__ import print_function, division, absolute_import
from tpDcc.libs.python import decorators
from tpDcc.libs.nameit.core import namelib

@decorators.Singleton
class NameItLib(namelib.NameLib, object):
    pass
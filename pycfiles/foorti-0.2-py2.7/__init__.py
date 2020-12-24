# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foorti/__init__.py
# Compiled at: 2017-02-13 23:00:12
import redis
from .foorti_systems import *
from .foorti_list import List

def fetch_list(name, system='default'):
    return List(name, system)
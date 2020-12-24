# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/yaml.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from functools import partial
from yaml import load as _load, dump as _dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper, CSafeLoader as SafeLoader, CSafeDumper as SafeDumper
except ImportError:
    from yaml import Loader, Dumper, SafeLoader, SafeDumper

load = partial(_load, Loader=Loader)
dump = partial(_dump, Dumper=Dumper)
safe_load = partial(_load, Loader=SafeLoader)
safe_dump = partial(_dump, Dumper=SafeDumper)
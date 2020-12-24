# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/marrow/cache/util.py
# Compiled at: 2015-04-23 10:56:41
"""Convienent utilities."""
from __future__ import print_function
from warnings import warn
from weakref import ref
from functools import wraps
from itertools import chain
from inspect import getmembers, getmodule, isclass, isfunction, ismethod
from collections import deque
from contextlib import contextmanager
from hashlib import sha256
from datetime import datetime, timedelta
from pprint import pformat
from marrow.package.canonical import name as resolve
from marrow.package.loader import traverse as fetch
utcnow = datetime.utcnow

@contextmanager
def stack(target, attribute, value):
    container = getattr(target, attribute, None)
    if container is None:
        container = deque()
        setattr(target, attribute, container)
    container.append(value)
    yield
    container.pop()
    if not container:
        delattr(target, attribute)
    return
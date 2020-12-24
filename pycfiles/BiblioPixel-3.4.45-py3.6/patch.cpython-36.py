# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/patch.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 272 bytes
from bibliopixel.project import importer
import contextlib

@contextlib.contextmanager
def patch(object, name, value):
    saved_value = getattr(object, name)
    setattr(object, name, value)
    try:
        yield
    finally:
        setattr(object, name, saved_value)
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/core/__init__.py
# Compiled at: 2016-04-25 13:24:07
# Size of source mod 2**32: 424 bytes
from threading import local as __local
from .application import Application
from .util import lazy
__all__ = [
 'local', 'Applicaiton', 'lazy']
local = __local()
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wswrapper/__init__.py
# Compiled at: 2016-07-04 19:00:44
# Size of source mod 2**32: 147 bytes
from .RFC6455 import *
from .httpParser import *
from .wrapper import *
with open(__path__[0] + '/version', 'r') as (r):
    __version__ = r.read()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Owls/__init__.py
# Compiled at: 2018-11-11 02:42:12
# Size of source mod 2**32: 457 bytes
from __future__ import print_function
import os
owls_path = os.path.expanduser('~') + '/.owls'
if not os.path.exists(owls_path):
    os.makedirs(owls_path)
from .version import __version__
from .plot import *
from .FoamFrame import *
from .MultiFrame import *
from future.builtins import *
print('Owls Version: ' + __version__)
try:
    from mplinterface import *
except:
    print('Warning no matplotlib support')
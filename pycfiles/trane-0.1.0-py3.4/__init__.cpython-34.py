# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/trane/__init__.py
# Compiled at: 2018-04-02 06:43:38
# Size of source mod 2**32: 243 bytes
from .libinfo import __version__
from .core import *
from .utils import *
from . import ops
import logging
logname = 'trane.log'
logging.basicConfig(filename=logname, filemode='w', level=logging.DEBUG)
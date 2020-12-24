# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mai\__init__.py
# Compiled at: 2020-03-10 05:11:59
# Size of source mod 2**32: 154 bytes
from . import utils
from . import models
from . import losses
try:
    from .version import __version__
except ImportError:
    pass
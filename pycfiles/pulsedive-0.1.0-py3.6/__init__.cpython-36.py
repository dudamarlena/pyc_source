# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pulsedive/__init__.py
# Compiled at: 2019-01-10 09:04:26
# Size of source mod 2**32: 160 bytes
from .client import Pulsedive
from .exceptions import PulsediveException
VERSION = (0, 1, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))
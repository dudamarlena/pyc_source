# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pulsedive/__init__.py
# Compiled at: 2019-01-10 09:04:26
# Size of source mod 2**32: 160 bytes
from .client import Pulsedive
from .exceptions import PulsediveException
VERSION = (0, 1, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))
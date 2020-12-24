# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/topfm/__init__.py
# Compiled at: 2018-04-20 01:34:27
# Size of source mod 2**32: 334 bytes
from pathlib import Path
from enum import Enum, auto
from nicfit import getLogger
from .__about__ import __version__ as version
log = getLogger(__package__)
CACHE_D = Path().home() / '.cache' / 'TopFM'
__all__ = [
 'log', 'getLogger', 'version', 'CACHE_D']

class PromptMode(Enum):
    ON = auto()
    OFF = auto()
    FAIL = auto()
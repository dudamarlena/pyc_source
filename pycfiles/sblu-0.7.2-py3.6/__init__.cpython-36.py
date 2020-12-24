# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/__init__.py
# Compiled at: 2019-04-09 13:35:51
# Size of source mod 2**32: 398 bytes
from __future__ import absolute_import
import logging
from .config import get_config
try:
    from .version import version
except ImportError:
    version = '0.0.0'

from path import Path
__version__ = version
CONFIG = get_config()
PRMS_DIR = Path(CONFIG['prms_dir'])
logging.getLogger(__name__).addHandler(logging.NullHandler())
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/log.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 586 bytes
"""Logging utilities."""
import logging
from . import __title__
logging.basicConfig()
logger = logging.getLogger(__title__)
logger.addHandler(logging.StreamHandler())
logger.propagate = False
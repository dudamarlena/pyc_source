# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/logger.py
# Compiled at: 2016-11-27 06:27:17
"""
Logging facilities.
"""
import logging
from .pkginfo import __title__
log = logging.getLogger(__title__)
log.addHandler(logging.NullHandler())

def init_logging(verbose=False, formatstring=None):
    handler = logging.StreamHandler()
    log.addHandler(handler)
    if not formatstring:
        formatstring = '%(name)s: %(levelname)s: %(message)s'
    formatter = logging.Formatter(formatstring)
    handler.setFormatter(formatter)
    log.setLevel(logging.INFO if verbose else logging.WARNING)
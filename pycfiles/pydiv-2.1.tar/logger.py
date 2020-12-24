# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/logger.py
# Compiled at: 2016-11-27 06:27:17
__doc__ = '\nLogging facilities.\n'
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
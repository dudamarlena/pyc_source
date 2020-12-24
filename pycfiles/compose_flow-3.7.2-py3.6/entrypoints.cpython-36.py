# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/entrypoints.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 641 bytes
"""
Entrypoints module

Main console script entrypoints for the dc tool
"""
import logging, logging.config, sys
from compose_flow import errors
MIN_VERSION = (3, 6)
RUNTIME_VERSION = (sys.version_info.major, sys.version_info.minor)
if RUNTIME_VERSION < MIN_VERSION:
    sys.exit('Error: compose-flow runs on Python3.6+')
from . import settings
from .commands import Workflow

def compose_flow():
    """
    Main entrypoint
    """
    logging.config.dictConfig(settings.LOGGING)
    try:
        response = Workflow().run()
    except errors.NoSuchConfig as exc:
        response = f"Error: {exc}"

    sys.exit(response)
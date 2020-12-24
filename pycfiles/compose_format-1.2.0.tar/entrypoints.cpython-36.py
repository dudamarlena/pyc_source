# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/entrypoints.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 641 bytes
__doc__ = '\nEntrypoints module\n\nMain console script entrypoints for the dc tool\n'
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
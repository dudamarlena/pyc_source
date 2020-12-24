# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shinkei/__init__.py
# Compiled at: 2019-12-14 12:45:46
# Size of source mod 2**32: 734 bytes
__title__ = 'shinkei'
__author__ = 'Lorenzo'
__license__ = 'MIT'
__copyright__ = 'Copyright 2019 Lorenzo'
__docformat__ = 'restructedtext en'
__version__ = '0.1.6'
import logging
from . import ext
from .client import Client, connect
from .exceptions import *
from .handlers import Handler, HandlerMeta, listens_to
from .objects import MetadataPayload, Version, VersionMetadata
from .querybuilder import Node, QueryBuilder
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, _):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
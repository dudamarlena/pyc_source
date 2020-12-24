# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\kanzhun\projects\graph\graphic\src\graphic\__init__.py
# Compiled at: 2018-11-04 20:27:30
# Size of source mod 2**32: 437 bytes
from .meta import __version__
from .graph import Graph
from .shortcuts import node, link, relationship, use_neo4j
import logging
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
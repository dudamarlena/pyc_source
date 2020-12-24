# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/__init__.py
# Compiled at: 2018-05-29 14:06:18
# Size of source mod 2**32: 1739 bytes
__doc__ = '\nproducti_gestio\n~~~~~~~~~~~~~~~\nThe Main module. A simple REST-API server creator.\n'
import producti_gestio.core, producti_gestio.decorator, producti_gestio.server, producti_gestio.filters
from producti_gestio.core.check import check
from producti_gestio.filters import Filters, Filter
from producti_gestio.server import Server
from producti_gestio.decorator.wrapper import Decorator
__author__: str = 'pyTeens'
__license__: str = 'GNU GENERAL PUBLIC LICENSE'
__url__: str = 'https://github.com/pyTeens/producti-gestio'
__version__: str = '0.7.2'
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/__init__.py
# Compiled at: 2018-05-29 14:06:18
# Size of source mod 2**32: 1739 bytes
"""
producti_gestio
~~~~~~~~~~~~~~~
The Main module. A simple REST-API server creator.
"""
import producti_gestio.core, producti_gestio.decorator, producti_gestio.server, producti_gestio.filters
from producti_gestio.core.check import check
from producti_gestio.filters import Filters, Filter
from producti_gestio.server import Server
from producti_gestio.decorator.wrapper import Decorator
__author__: str = 'pyTeens'
__license__: str = 'GNU GENERAL PUBLIC LICENSE'
__url__: str = 'https://github.com/pyTeens/producti-gestio'
__version__: str = '0.7.2'
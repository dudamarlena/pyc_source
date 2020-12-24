# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\gemstones\gemstone\build\lib\gemstone\__init__.py
# Compiled at: 2017-03-27 13:07:14
# Size of source mod 2**32: 1031 bytes
"""
Build microservices with Python
"""
from gemstone.core.microservice import MicroService
from gemstone.core.decorators import private_api_method, public_method, event_handler, requires_handler_reference, async_method, exposed_method
from gemstone.core.handlers import TornadoJsonRpcHandler, GemstoneCustomHandler
from gemstone.client.remote_service import RemoteService
from gemstone.core.container import Container
from gemstone.util import as_completed, first_completed, make_callbacks
__author__ = 'Vlad Calin'
__email__ = 'vlad.s.calin@gmail.com'
__version__ = '0.10.1'
__all__ = [
 'MicroService',
 'RemoteService',
 'Container',
 'public_method',
 'private_api_method',
 'event_handler',
 'requires_handler_reference',
 'exposed_method',
 'TornadoJsonRpcHandler',
 'GemstoneCustomHandler',
 'as_completed',
 'first_completed',
 'make_callbacks']
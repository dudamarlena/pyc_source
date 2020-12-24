# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/polyinterface/__init__.py
# Compiled at: 2020-04-13 17:37:50
# Size of source mod 2**32: 451 bytes
from .polylogger import LOG_HANDLER, LOGGER
from .polyinterface import Interface, Node, Controller, unload_interface, get_network_interface
__version__ = '2.0.40'
__description__ = 'UDI Polyglot v2 Interface'
__url__ = 'https://github.com/UniversalDevicesInc/polyglot-v2-python-interface'
__author__ = 'James Milne'
__authoremail__ = 'milne.james@gmail.com'
__license__ = 'MIT'
LOGGER.info('{} {} Starting...'.format(__description__, __version__))
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
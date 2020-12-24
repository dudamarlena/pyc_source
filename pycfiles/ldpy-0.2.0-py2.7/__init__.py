# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ldpy/__init__.py
# Compiled at: 2015-11-04 02:45:20
__version__ = '0.2.0'
__date__ = '2014/11/01'
__license__ = 'Apache Software License 2.0'
__url__ = 'http://github.com/wikier/ldpy'
__contact__ = 'sergio@wikier.org'
__agent__ = 'ldpy %s (http://github.com/wikier/ldpy)' % __version__
__docformat__ = 'restructuredtext en'
import logging
_LOGGER = logging.getLogger('ldpy')
_LOGGER.info('LDPy Version: %s' % __version__)
from client import Client
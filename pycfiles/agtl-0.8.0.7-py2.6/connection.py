# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/connection.py
# Compiled at: 2011-04-23 08:59:57
import logging
logger = logging.getLogger('connection')
offline = False
_conic_connection = None
try:
    import conic
except ImportError:
    pass

def _conic_connection_changed(connection, event, magic=None):
    global offline
    status = event.get_status()
    if status == conic.STATUS_CONNECTED:
        offline = False
        logger.debug('Going online')
    elif status in [conic.STATUS_DISCONNECTED, conic.STATUS_DISCONNECTING]:
        offline = True
        logger.debug('Going offline')
    else:
        logger.debug('Not touching offline mode.')


def init():
    global _conic_connection
    try:
        conic
    except NameError:
        logger.debug('Not using conic library')
    else:
        _conic_connection = conic.Connection()
        _conic_connection.connect('connection-event', _conic_connection_changed)
        _conic_connection.set_property('automatic-connection-events', True)
        logger.debug('Connection events initialized')
# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
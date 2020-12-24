# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/broker/cli/setup_application.py
# Compiled at: 2016-06-27 03:37:50
# Size of source mod 2**32: 329 bytes
from xbus.broker.cli import get_config
from xbus.broker.model import setup_app
__author__ = 'faide'

def setup_xbusbroker():
    """ a simple cmd line that will create a default db
    """
    setup_app(get_config())
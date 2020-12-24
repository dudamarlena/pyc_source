# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weresync/daemon/daemon.py
# Compiled at: 2019-06-15 13:38:01
# Size of source mod 2**32: 1490 bytes
"""Runs the daemon and exposes the necessary methods to the interface
functions.

See also :mod:`weresync.interface.dbus_client`:"""
from weresync.daemon.copier import DriveCopier
from gi.repository import GLib
from pydbus import SystemBus
import weresync.utils as utils
import logging
DEFAULT_DAEMON_LOG_LOCATION = '/var/log/weresync/weresync.log'
LOGGER = logging.getLogger(__name__)

def run():
    """Function which starts the daemon and publishes the
    :class:`~weresync.daemon.copier.DriveCopier` over dbus."""
    utils.start_logging_handler(DEFAULT_DAEMON_LOG_LOCATION)
    utils.enable_localization()
    with SystemBus() as (bus):
        with bus.publish('net.manilas.weresync.DriveCopier', DriveCopier()):
            GLib.idle_add(lambda : LOGGER.debug('Starting GLib loop'))
            loop = GLib.MainLoop()
            loop.run()


if __name__ == '__main__':
    run()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weresync/interface/dbus_client.py
# Compiled at: 2019-06-15 13:23:18
# Size of source mod 2**32: 2729 bytes
"""Connects the interface applications (cli and gui) with the backend daemon.

See also :mod:`weresync.daemon.daemon`"""
from pydbus import SystemBus
from gi.repository import GLib
import threading, gi.repository.GLib
try:
    bus = SystemBus()
    drive_copier = bus.get('net.manilas.weresync.DriveCopier')
    copy_drive = drive_copier.CopyDrive
    error = None
except gi.repository.GLib.Error as e:
    try:
        error = e
        copy_drive = False
    finally:
        e = None
        del e

def _unthreaded_subscribe_to_signals(partition_status_callback, copy_status_callback, boot_status_callback):
    drive_copier.PartitionStatus.connect(partition_status_callback)
    drive_copier.CopyStatus.connect(copy_status_callback)
    drive_copier.BootStatus.connect(boot_status_callback)
    loop = GLib.MainLoop()
    loop.run()


def subscribe_to_signals(partition_status_callback, copy_status_callback, boot_status_callback):
    """Subscribes to the weresync callbacks to get information from the daemon.

    :param partition_status_callback: A function which takes a float between 0
                                      and 1 which represents the progress on
                                      formatting partitions.
    :param copy_status_callback: A function which takes an integer representing
                                 the partition being copied and a float between
                                 0 and 1 representing the progress on the copy.
    :param boot_status_callback: A function which takes a boolean. If passed
                                 False the bootloader has not finished
                                 installing. If True it has."""
    thread = threading.Thread(target=_unthreaded_subscribe_to_signals,
      args=(
     partition_status_callback, copy_status_callback,
     boot_status_callback))
    thread.daemon = True
    thread.start()
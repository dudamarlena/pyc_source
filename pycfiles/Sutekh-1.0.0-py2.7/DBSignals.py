# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/DBSignals.py
# Compiled at: 2019-12-11 16:37:48
"""Wrappers around SQLObject signals needed to keep card sets and the card
collection in sync."""
from sqlobject.events import Signal, listen, RowUpdateSignal, RowDestroySignal, RowCreatedSignal
try:
    from sqlobject.include.pydispatch import dispatcher
except ImportError:
    from pydispatch import dispatcher

from .BaseTables import PhysicalCardSet

class ChangedSignal(Signal):
    """Syncronisation signal for card sets.

       Needs to be sent after changes are commited to the database, so card
       sets can reload properly.
       Used so card sets always reflect correct available counts.
       """
    pass


def send_changed_signal(oCardSet, oPhysCard, iChange, cClass=PhysicalCardSet):
    """Sent when card counts change, as card sets may need to update."""
    cClass.sqlmeta.send(ChangedSignal, oCardSet, oPhysCard, iChange)


def listen_changed(fListener, cClass):
    """Listens for the changed_signal."""
    listen(fListener, cClass, ChangedSignal)


def listen_row_destroy(fListener, cClass):
    """listen for the row destroyed signal sent when a card set is deleted."""
    listen(fListener, cClass, RowDestroySignal)


def listen_row_update(fListener, cClass):
    """listen for the row updated signal sent when a card set is modified."""
    listen(fListener, cClass, RowUpdateSignal)


def listen_row_created(fListener, cClass):
    """listen for the row created signal sent when a new set is created."""
    listen(fListener, cClass, RowCreatedSignal)


def disconnect_changed(fListener, cClass):
    """Disconnects from the changed_signal."""
    dispatcher.disconnect(fListener, signal=ChangedSignal, sender=cClass)


def disconnect_row_destroy(fListener, cClass):
    """Disconnect from the row destroyed signal."""
    dispatcher.disconnect(fListener, signal=RowDestroySignal, sender=cClass)


def disconnect_row_created(fListener, cClass):
    """Disconnect from the row created signal."""
    dispatcher.disconnect(fListener, signal=RowCreatedSignal, sender=cClass)


def disconnect_row_update(fListener, cClass):
    """Disconnect the row updated signal."""
    dispatcher.disconnect(fListener, signal=RowUpdateSignal, sender=cClass)
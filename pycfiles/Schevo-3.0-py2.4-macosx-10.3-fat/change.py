# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/change.py
# Compiled at: 2007-03-21 14:34:41
"""Change notification support.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
import louie
from schevo.signal import TransactionExecuted
CREATE = 1
DELETE = 2
UPDATE = 3

class _CriteriaSignal(louie.Signal):
    """A special signal used internally by Distributors to associate
    specific criteria with a unique object."""
    __module__ = __name__


class Distributor(object):
    __module__ = __name__

    def __init__(self, db, auto_distribute=False):
        louie.connect(self.transaction_executed, TransactionExecuted, sender=db)
        self.auto_distribute = auto_distribute
        self._changes = []
        self._criteria_signals = {}

    def distribute(self):
        """Distribute changes to receivers."""
        send = louie.send
        c_s_get = self._criteria_signals.get
        changes = normalize(self._changes)
        for change in changes:
            criteria_list = [
             change, tuple(change[:2]), tuple(change[:1]), ()]
            for criteria in criteria_list:
                signal = c_s_get(criteria, None)
                if signal is not None:
                    send(signal, change=change)

        self._changes = []
        return

    def subscribe(self, receiver, *criteria):
        """Start watching criteria, notifying a receiver."""
        signal = self._criteria_signal(criteria)
        louie.connect(receiver, signal)

    def unsubscribe(self, receiver):
        """Stop notifying a receiver about any criteria."""
        for signal in self._criteria_signals.itervalues():
            try:
                louie.disconnect(receiver, signal)
            except louie.error.DispatcherKeyError:
                pass

    def transaction_executed(self, transaction):
        self._changes.extend(transaction._changes)
        if self.auto_distribute:
            self.distribute()

    def _criteria_signal(self, criteria):
        signal = self._criteria_signals.setdefault(criteria, _CriteriaSignal())
        return signal


def normalize(changes):
    """Return a normalized version of changes, removing symmetry."""
    changes = set(changes)
    creates = set(((ext, oid) for (typ, ext, oid) in changes if typ == CREATE))
    deletes = set(((ext, oid) for (typ, ext, oid) in changes if typ == DELETE))
    updates = set(((ext, oid) for (typ, ext, oid) in changes if typ == UPDATE))
    create_then_deletes = deletes.intersection(creates)
    update_then_deletes = deletes.intersection(updates)
    creates -= create_then_deletes
    deletes -= create_then_deletes
    updates -= update_then_deletes
    updates -= creates
    result = set(((CREATE, ext, oid) for (ext, oid) in creates))
    result.update(set(((DELETE, ext, oid) for (ext, oid) in deletes)))
    result.update(set(((UPDATE, ext, oid) for (ext, oid) in updates)))
    return sorted(result)


class Summary(object):
    __module__ = __name__

    def __init__(self):
        self.creates = {}
        self.deletes = {}
        self.updates = {}


def summarize(tx):
    """Return a summary of changes."""
    changes = set(tx.sys.changes)
    creates = set(((ext, oid) for (typ, ext, oid) in changes if typ == CREATE))
    deletes = set(((ext, oid) for (typ, ext, oid) in changes if typ == DELETE))
    updates = set(((ext, oid) for (typ, ext, oid) in changes if typ == UPDATE))
    create_then_deletes = deletes.intersection(creates)
    update_then_deletes = deletes.intersection(updates)
    creates -= create_then_deletes
    deletes -= create_then_deletes
    updates -= update_then_deletes
    updates -= creates
    summary = Summary()
    for (ext, oid) in creates:
        summary.creates.setdefault(ext, set()).add(oid)

    for (ext, oid) in deletes:
        summary.deletes.setdefault(ext, set()).add(oid)

    for (ext, oid) in updates:
        summary.updates.setdefault(ext, set()).add(oid)

    return summary


optimize.bind_all(sys.modules[__name__])
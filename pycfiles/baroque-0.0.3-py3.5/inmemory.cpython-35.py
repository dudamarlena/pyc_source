# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/persistence/inmemory.py
# Compiled at: 2017-03-23 16:32:56
# Size of source mod 2**32: 1670 bytes
from .backend import PersistenceBackend

class DictBackend(PersistenceBackend):
    __doc__ = 'An in-memory :obj:`baroque.persistence.backend.ConfigurationBackend`:\n    implementation backed by Python dict\n\n    '

    def __init__(self):
        self._db = dict()

    def create(self, event):
        assert event is not None
        if event.id is None:
            return
        self._db.setdefault(event.id, event)

    def read(self, event_id):
        return self._db.get(event_id, None)

    def update(self, event):
        assert event is not None
        if event.id is None:
            return
        if event.id in self._db:
            self._db[event.id] = event

    def delete(self, event_id):
        if event_id is None:
            return
        self._db.pop(event_id, None)

    def __len__(self):
        return len(self._db)

    def __contains__(self, event):
        return event.id in self._db

    def __iter__(self):
        return (e for e in self._db)

    def __getitem__(self, event_id):
        return self.read(event_id)

    def keys(self):
        """Gives the key set of this collection-like object.

        Returns:
            set

        """
        return self._db.keys()

    def values(self):
        """Gives the value set of this collection-like object.

        Returns:
            set

        """
        return self._db.values()

    def clear(self):
        """Clears all the key-value pairs of this collection-like object."""
        self._db.clear()

    def __repr__(self):
        return '<{}.{} - storing {} events>'.format(__name__, self.__class__.__name__, len(self))
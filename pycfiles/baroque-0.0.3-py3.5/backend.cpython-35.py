# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/persistence/backend.py
# Compiled at: 2017-03-23 16:35:33
# Size of source mod 2**32: 799 bytes


class PersistenceBackend:

    def create(self, event):
        """Persists an event.

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be persisted

        """
        pass

    def read(self, event_id):
        """Loads an event.

        Args:
            event_id (str): the identifier of the event to be loaded

        Returns:
            :obj:`baroque.entities.event.Event`

        """
        pass

    def update(self, event):
        """Updates the event.

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be updated

        """
        pass

    def delete(self, event_id):
        """Deletes an event.

        Args:
            event_id (str): the identifier of the event to be deleted

        """
        pass
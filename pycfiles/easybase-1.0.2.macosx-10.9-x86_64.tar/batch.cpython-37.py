# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wgzhao/Codes/easybase/py3/lib/python3.7/site-packages/easybase/batch.py
# Compiled at: 2019-12-20 08:50:49
# Size of source mod 2**32: 4308 bytes
from collections import defaultdict
import logging
from numbers import Integral
import six
from HBase_thrift import BatchMutation, Mutation
logger = logging.getLogger(__name__)

class Batch(object):
    __doc__ = 'Batch mutation class.\n\n    This class cannot be instantiated directly; use :py:meth:`Table.batch`\n    instead.\n    '

    def __init__(self, table, timestamp=None, batch_size=None, transaction=False, wal=True):
        """Initialise a new Batch instance."""
        if not timestamp is None:
            if not isinstance(timestamp, Integral):
                raise TypeError("'timestamp' must be an integer or None")
        if batch_size is not None:
            if transaction:
                raise TypeError("'transaction' cannot be used when 'batch_size' is specified")
            if not batch_size > 0:
                raise ValueError("'batch_size' must be > 0")
        self._table = table
        self._batch_size = batch_size
        self._timestamp = timestamp
        self._transaction = transaction
        self._wal = wal
        self._families = None
        self._reset_mutations()

    def _reset_mutations(self):
        """Reset the internal mutation buffer."""
        self._mutations = defaultdict(list)
        self._mutation_count = 0

    def send(self):
        """Send the batch to the server."""
        bms = [BatchMutation(row, m) for row, m in six.iteritems(self._mutations)]
        if not bms:
            return
        else:
            logger.debug("Sending batch for '%s' (%d mutations on %d rows)", self._table.name, self._mutation_count, len(bms))
            if self._timestamp is None:
                self._table.connection.client.mutateRows(self._table.name, bms, {})
            else:
                self._table.connection.client.mutateRowsTs(self._table.name, bms, self._timestamp, {})
        self._reset_mutations()

    def put(self, row, data, wal=None):
        """Store data in the table.

        See :py:meth:`Table.put` for a description of the `row`, `data`,
        and `wal` arguments. The `wal` argument should normally not be
        used; its only use is to override the batch-wide value passed to
        :py:meth:`Table.batch`.
        """
        if wal is None:
            wal = self._wal
        self._mutations[row].extend((Mutation(isDelete=False, column=column, value=value, writeToWAL=wal) for column, value in six.iteritems(data)))
        self._mutation_count += len(data)
        if self._batch_size:
            if self._mutation_count >= self._batch_size:
                self.send()

    def delete(self, row, columns=None, wal=None):
        """Delete data from the table.

        See :py:meth:`Table.put` for a description of the `row`, `data`,
        and `wal` arguments. The `wal` argument should normally not be
        used; its only use is to override the batch-wide value passed to
        :py:meth:`Table.batch`.
        """
        if columns is None:
            if self._families is None:
                self._families = self._table._column_family_names()
            columns = self._families
        else:
            if wal is None:
                wal = self._wal
            self._mutations[row].extend((Mutation(isDelete=True, column=column, writeToWAL=wal) for column in columns))
            self._mutation_count += len(columns)
            if self._batch_size and self._mutation_count >= self._batch_size:
                self.send()

    def __enter__(self):
        """Called upon entering a ``with`` block"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Called upon exiting a ``with`` block"""
        if self._transaction:
            if exc_type is not None:
                return
        self.send()
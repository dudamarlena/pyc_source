# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hs2client/commons.py
# Compiled at: 2018-05-31 09:14:09
import abc, collections, time, numbers
from future.utils import with_metaclass
from past.builtins import basestring
from itertools import islice

class ParamEscaper(object):

    def escape_args(self, parameters):
        if isinstance(parameters, dict):
            return {k:self.escape_item(v) for k, v in parameters.items()}
        if isinstance(parameters, (list, tuple)):
            return tuple(self.escape_item(x) for x in parameters)
        raise ValueError(('Unsupported param format: {}').format(parameters))

    def escape_number(self, item):
        return item

    def escape_string(self, item):
        if isinstance(item, bytes):
            item = item.decode('utf-8')
        return ("'{}'").format(item.replace("'", "''"))

    def escape_sequence(self, item):
        l = map(str, map(self.escape_item, item))
        return '(' + (',').join(l) + ')'

    def escape_item(self, item):
        if item is None:
            return 'NULL'
        else:
            if isinstance(item, numbers.Real):
                return self.escape_number(item)
            if isinstance(item, basestring):
                return self.escape_string(item)
            if isinstance(item, collections.Iterable):
                return self.escape_sequence(item)
            raise ValueError(('Unsupported object {}').format(item))
            return


class DBAPICursor(with_metaclass(abc.ABCMeta, object)):
    """Base class for some common DB-API logic"""
    _STATE_NONE = 0
    _STATE_RUNNING = 1
    _STATE_FINISHED = 2

    def __init__(self, poll_interval=1):
        self._poll_interval = poll_interval
        self._reset_state()
        self.lastrowid = None
        return

    def _reset_state(self):
        """Reset state about the previous query in preparation for running another query"""
        self._rownumber = 0
        self._state = self._STATE_NONE
        self._data = collections.deque()
        self._columns = None
        return

    def _fetch_while(self, fn):
        while fn():
            self._fetch_more()
            if fn():
                time.sleep(self._poll_interval)

    @abc.abstractproperty
    def description(self):
        raise NotImplementedError

    def close(self):
        """By default, do nothing"""
        pass

    @abc.abstractmethod
    def _fetch_more(self):
        """Get more results, append it to ``self._data``, and update ``self._state``."""
        raise NotImplementedError

    @property
    def rowcount(self):
        """By default, return -1 to indicate that this is not supported."""
        return -1

    @abc.abstractmethod
    def execute(self, operation, parameters=None):
        """Prepare and execute a database operation (query or command).
        Parameters may be provided as sequence or mapping and will be bound to variables in the
        operation. Variables are specified in a database-specific notation (see the module's
        ``paramstyle`` attribute for details).
        Return values are not defined.
        """
        raise NotImplementedError

    def executemany(self, operation, seq_of_parameters):
        """Prepare a database operation (query or command) and then execute it against all parameter
        sequences or mappings found in the sequence ``seq_of_parameters``.
        Only the final result set is retained.
        Return values are not defined.
        """
        for parameters in seq_of_parameters[:-1]:
            self.execute(operation, parameters)
            while self._state != self._STATE_FINISHED:
                self._fetch_more()

        if seq_of_parameters:
            self.execute(operation, seq_of_parameters[(-1)])

    def fetchone(self):
        """Fetch the next row of a query result set, returning a single sequence, or ``None`` when
        no more data is available.
        An :py:class:`~pyhive.exc.Error` (or subclass) exception is raised if the previous call to
        :py:meth:`execute` did not produce any result set or no call was issued yet.
        """
        if self._state == self._STATE_NONE:
            raise ValueError('No query yet')
        self._fetch_while(lambda : not self._data and self._state != self._STATE_FINISHED)
        if not self._data:
            return
        else:
            self._rownumber += 1
            return self._data.popleft()
            return

    def fetchmany(self, size=None):
        """Fetch the next set of rows of a query result, returning a sequence of sequences (e.g. a
        list of tuples). An empty sequence is returned when no more rows are available.
        The number of rows to fetch per call is specified by the parameter. If it is not given, the
        cursor's arraysize determines the number of rows to be fetched. The method should try to
        fetch as many rows as indicated by the size parameter. If this is not possible due to the
        specified number of rows not being available, fewer rows may be returned.
        An :py:class:`~pyhive.exc.Error` (or subclass) exception is raised if the previous call to
        :py:meth:`execute` did not produce any result set or no call was issued yet.
        """
        if size is None:
            size = self.arraysize
        return list(islice(iter(self.fetchone, None), size))

    def fetchall(self):
        """Fetch all (remaining) rows of a query result, returning them as a sequence of sequences
        (e.g. a list of tuples).
        An :py:class:`~pyhive.exc.Error` (or subclass) exception is raised if the previous call to
        :py:meth:`execute` did not produce any result set or no call was issued yet.
        """
        return list(iter(self.fetchone, None))

    @property
    def arraysize(self):
        """This read/write attribute specifies the number of rows to fetch at a time with
        :py:meth:`fetchmany`. It defaults to 1 meaning to fetch a single row at a time.
        """
        return self._arraysize

    @arraysize.setter
    def arraysize(self, value):
        self._arraysize = value

    def setinputsizes(self, sizes):
        """Does nothing by default"""
        pass

    def setoutputsize(self, size, column=None):
        """Does nothing by default"""
        pass

    @property
    def rownumber(self):
        """This read-only attribute should provide the current 0-based index of the cursor in the
        result set.
        The index can be seen as index of the cursor in a sequence (the result set). The next fetch
        operation will fetch the row indexed by ``rownumber`` in that sequence.
        """
        return self._rownumber

    def __next__(self):
        """Return the next row from the currently executing SQL statement using the same semantics
        as :py:meth:`fetchone`. A ``StopIteration`` exception is raised when the result set is
        exhausted.
        """
        one = self.fetchone()
        if one is None:
            raise StopIteration
        else:
            return one
        return

    next = __next__

    def __iter__(self):
        """Return self to make cursors compatible to the iteration protocol."""
        return self
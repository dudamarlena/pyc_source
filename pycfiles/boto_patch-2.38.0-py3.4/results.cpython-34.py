# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/dynamodb2/results.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6602 bytes


class ResultSet(object):
    __doc__ = "\n    A class used to lazily handle page-to-page navigation through a set of\n    results.\n\n    It presents a transparent iterator interface, so that all the user has\n    to do is use it in a typical ``for`` loop (or list comprehension, etc.)\n    to fetch results, even if they weren't present in the current page of\n    results.\n\n    This is used by the ``Table.query`` & ``Table.scan`` methods.\n\n    Example::\n\n        >>> users = Table('users')\n        >>> results = ResultSet()\n        >>> results.to_call(users.query, username__gte='johndoe')\n        # Now iterate. When it runs out of results, it'll fetch the next page.\n        >>> for res in results:\n        ...     print res['username']\n\n    "

    def __init__(self, max_page_size=None):
        super(ResultSet, self).__init__()
        self.the_callable = None
        self.call_args = []
        self.call_kwargs = {}
        self._results = []
        self._offset = -1
        self._results_left = True
        self._last_key_seen = None
        self._fetches = 0
        self._max_page_size = max_page_size
        self._limit = None

    @property
    def first_key(self):
        return 'exclusive_start_key'

    def _reset(self):
        """
        Resets the internal state of the ``ResultSet``.

        This prevents results from being cached long-term & consuming
        excess memory.

        Largely internal.
        """
        self._results = []
        self._offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        self._offset += 1
        if self._offset >= len(self._results):
            if self._results_left is False:
                raise StopIteration()
            self.fetch_more()
            while not len(self._results) and self._results_left:
                self.fetch_more()

        if self._offset < len(self._results):
            if self._limit is not None:
                self._limit -= 1
                if self._limit < 0:
                    raise StopIteration()
                return self._results[self._offset]
        raise StopIteration()

    next = __next__

    def to_call(self, the_callable, *args, **kwargs):
        """
        Sets up the callable & any arguments to run it with.

        This is stored for subsequent calls so that those queries can be
        run without requiring user intervention.

        Example::

            # Just an example callable.
            >>> def squares_to(y):
            ...     for x in range(1, y):
            ...         yield x**2
            >>> rs = ResultSet()
            # Set up what to call & arguments.
            >>> rs.to_call(squares_to, y=3)

        """
        if not callable(the_callable):
            raise ValueError('You must supply an object or function to be called.')
        self._limit = kwargs.pop('limit', None)
        if self._limit is not None:
            if self._limit < 0:
                self._limit = None
        self.the_callable = the_callable
        self.call_args = args
        self.call_kwargs = kwargs

    def fetch_more(self):
        """
        When the iterator runs out of results, this method is run to re-execute
        the callable (& arguments) to fetch the next page.

        Largely internal.
        """
        self._reset()
        args = self.call_args[:]
        kwargs = self.call_kwargs.copy()
        if self._last_key_seen is not None:
            kwargs[self.first_key] = self._last_key_seen
        if self._limit:
            if self._max_page_size and self._max_page_size > self._limit:
                self._max_page_size = self._limit
        if self._max_page_size is not None:
            kwargs['limit'] = self._max_page_size
        else:
            if self._limit is not None:
                kwargs['limit'] = self._limit
            results = self.the_callable(*args, **kwargs)
            self._fetches += 1
            new_results = results.get('results', [])
            self._last_key_seen = results.get('last_key', None)
            if len(new_results):
                self._results.extend(results['results'])
            if self._limit is not None:
                if self._limit >= 0:
                    limit = self._limit
                    limit -= len(results['results'])
                    if limit <= 0:
                        self._results_left = False
        if self._last_key_seen is None:
            self._results_left = False


class BatchGetResultSet(ResultSet):

    def __init__(self, *args, **kwargs):
        self._keys_left = kwargs.pop('keys', [])
        self._max_batch_get = kwargs.pop('max_batch_get', 100)
        super(BatchGetResultSet, self).__init__(*args, **kwargs)

    def fetch_more(self):
        self._reset()
        args = self.call_args[:]
        kwargs = self.call_kwargs.copy()
        kwargs['keys'] = self._keys_left[:self._max_batch_get]
        self._keys_left = self._keys_left[self._max_batch_get:]
        if len(self._keys_left) <= 0:
            self._results_left = False
        results = self.the_callable(*args, **kwargs)
        if not len(results.get('results', [])):
            return
        self._results.extend(results['results'])
        for offset, key_data in enumerate(results.get('unprocessed_keys', [])):
            self._keys_left.insert(offset, key_data)

        if len(self._keys_left) > 0:
            self._results_left = True
        if self.call_kwargs.get('limit'):
            self.call_kwargs['limit'] -= len(results['results'])
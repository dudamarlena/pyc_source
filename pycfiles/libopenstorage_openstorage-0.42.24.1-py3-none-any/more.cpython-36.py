# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/more-itertools/more_itertools/more.py
# Compiled at: 2020-01-10 16:25:36
# Size of source mod 2**32: 83966 bytes
import warnings
from collections import Counter, defaultdict, deque
from collections.abc import Sequence
from functools import partial, wraps
from heapq import merge
from itertools import chain, compress, count, cycle, dropwhile, groupby, islice, repeat, starmap, takewhile, tee, zip_longest
from operator import itemgetter, lt, gt, sub
from sys import maxsize
from time import monotonic
from .recipes import consume, flatten, powerset, take, unique_everseen
__all__ = [
 'adjacent',
 'always_iterable',
 'always_reversible',
 'bucket',
 'chunked',
 'circular_shifts',
 'collapse',
 'collate',
 'consecutive_groups',
 'consumer',
 'count_cycle',
 'difference',
 'distinct_combinations',
 'distinct_permutations',
 'distribute',
 'divide',
 'exactly_n',
 'filter_except',
 'first',
 'groupby_transform',
 'ilen',
 'interleave_longest',
 'interleave',
 'intersperse',
 'islice_extended',
 'iterate',
 'ichunked',
 'last',
 'locate',
 'lstrip',
 'make_decorator',
 'map_except',
 'map_reduce',
 'numeric_range',
 'one',
 'only',
 'padded',
 'partitions',
 'set_partitions',
 'peekable',
 'repeat_last',
 'replace',
 'rlocate',
 'rstrip',
 'run_length',
 'seekable',
 'SequenceView',
 'side_effect',
 'sliced',
 'sort_together',
 'split_at',
 'split_after',
 'split_before',
 'split_when',
 'split_into',
 'spy',
 'stagger',
 'strip',
 'substrings',
 'substrings_indexes',
 'time_limited',
 'unique_to_each',
 'unzip',
 'windowed',
 'with_iter',
 'zip_offset']
_marker = object()

def chunked(iterable, n):
    """Break *iterable* into lists of length *n*:

        >>> list(chunked([1, 2, 3, 4, 5, 6], 3))
        [[1, 2, 3], [4, 5, 6]]

    If the length of *iterable* is not evenly divisible by *n*, the last
    returned list will be shorter:

        >>> list(chunked([1, 2, 3, 4, 5, 6, 7, 8], 3))
        [[1, 2, 3], [4, 5, 6], [7, 8]]

    To use a fill-in value instead, see the :func:`grouper` recipe.

    :func:`chunked` is useful for splitting up a computation on a large number
    of keys into batches, to be pickled and sent off to worker processes. One
    example is operations on rows in MySQL, which does not implement
    server-side cursors properly and would otherwise load the entire dataset
    into RAM on the client.

    """
    return iter(partial(take, n, iter(iterable)), [])


def first(iterable, default=_marker):
    """Return the first item of *iterable*, or *default* if *iterable* is
    empty.

        >>> first([0, 1, 2, 3])
        0
        >>> first([], 'some default')
        'some default'

    If *default* is not provided and there are no items in the iterable,
    raise ``ValueError``.

    :func:`first` is useful when you have a generator of expensive-to-retrieve
    values and want any arbitrary one. It is marginally shorter than
    ``next(iter(iterable), default)``.

    """
    try:
        return next(iter(iterable))
    except StopIteration:
        if default is _marker:
            raise ValueError('first() was called on an empty iterable, and no default value was provided.')
        return default


def last(iterable, default=_marker):
    """Return the last item of *iterable*, or *default* if *iterable* is
    empty.

        >>> last([0, 1, 2, 3])
        3
        >>> last([], 'some default')
        'some default'

    If *default* is not provided and there are no items in the iterable,
    raise ``ValueError``.
    """
    try:
        try:
            return iterable[(-1)]
        except (TypeError, AttributeError, KeyError):
            return deque(iterable, maxlen=1)[0]

    except IndexError:
        if default is _marker:
            raise ValueError('last() was called on an empty iterable, and no default value was provided.')
        return default


class peekable:
    __doc__ = 'Wrap an iterator to allow lookahead and prepending elements.\n\n    Call :meth:`peek` on the result to get the value that will be returned\n    by :func:`next`. This won\'t advance the iterator:\n\n        >>> p = peekable([\'a\', \'b\'])\n        >>> p.peek()\n        \'a\'\n        >>> next(p)\n        \'a\'\n\n    Pass :meth:`peek` a default value to return that instead of raising\n    ``StopIteration`` when the iterator is exhausted.\n\n        >>> p = peekable([])\n        >>> p.peek(\'hi\')\n        \'hi\'\n\n    peekables also offer a :meth:`prepend` method, which "inserts" items\n    at the head of the iterable:\n\n        >>> p = peekable([1, 2, 3])\n        >>> p.prepend(10, 11, 12)\n        >>> next(p)\n        10\n        >>> p.peek()\n        11\n        >>> list(p)\n        [11, 12, 1, 2, 3]\n\n    peekables can be indexed. Index 0 is the item that will be returned by\n    :func:`next`, index 1 is the item after that, and so on:\n    The values up to the given index will be cached.\n\n        >>> p = peekable([\'a\', \'b\', \'c\', \'d\'])\n        >>> p[0]\n        \'a\'\n        >>> p[1]\n        \'b\'\n        >>> next(p)\n        \'a\'\n\n    Negative indexes are supported, but be aware that they will cache the\n    remaining items in the source iterator, which may require significant\n    storage.\n\n    To check whether a peekable is exhausted, check its truth value:\n\n        >>> p = peekable([\'a\', \'b\'])\n        >>> if p:  # peekable has items\n        ...     list(p)\n        [\'a\', \'b\']\n        >>> if not p:  # peekable is exhaused\n        ...     list(p)\n        []\n\n    '

    def __init__(self, iterable):
        self._it = iter(iterable)
        self._cache = deque()

    def __iter__(self):
        return self

    def __bool__(self):
        try:
            self.peek()
        except StopIteration:
            return False
        else:
            return True

    def peek(self, default=_marker):
        """Return the item that will be next returned from ``next()``.

        Return ``default`` if there are no items left. If ``default`` is not
        provided, raise ``StopIteration``.

        """
        if not self._cache:
            try:
                self._cache.append(next(self._it))
            except StopIteration:
                if default is _marker:
                    raise
                return default

        return self._cache[0]

    def prepend(self, *items):
        """Stack up items to be the next ones returned from ``next()`` or
        ``self.peek()``. The items will be returned in
        first in, first out order::

            >>> p = peekable([1, 2, 3])
            >>> p.prepend(10, 11, 12)
            >>> next(p)
            10
            >>> list(p)
            [11, 12, 1, 2, 3]

        It is possible, by prepending items, to "resurrect" a peekable that
        previously raised ``StopIteration``.

            >>> p = peekable([])
            >>> next(p)
            Traceback (most recent call last):
              ...
            StopIteration
            >>> p.prepend(1)
            >>> next(p)
            1
            >>> next(p)
            Traceback (most recent call last):
              ...
            StopIteration

        """
        self._cache.extendleft(reversed(items))

    def __next__(self):
        if self._cache:
            return self._cache.popleft()
        else:
            return next(self._it)

    def _get_slice(self, index):
        step = 1 if index.step is None else index.step
        if step > 0:
            start = 0 if index.start is None else index.start
            stop = maxsize if index.stop is None else index.stop
        else:
            if step < 0:
                start = -1 if index.start is None else index.start
                stop = -maxsize - 1 if index.stop is None else index.stop
            else:
                raise ValueError('slice step cannot be zero')
        if start < 0 or stop < 0:
            self._cache.extend(self._it)
        else:
            n = min(max(start, stop) + 1, maxsize)
            cache_len = len(self._cache)
        if n >= cache_len:
            self._cache.extend(islice(self._it, n - cache_len))
        return list(self._cache)[index]

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._get_slice(index)
        else:
            cache_len = len(self._cache)
            if index < 0:
                self._cache.extend(self._it)
            else:
                if index >= cache_len:
                    self._cache.extend(islice(self._it, index + 1 - cache_len))
            return self._cache[index]


def collate(*iterables, **kwargs):
    """Return a sorted merge of the items from each of several already-sorted
    *iterables*.

        >>> list(collate('ACDZ', 'AZ', 'JKL'))
        ['A', 'A', 'C', 'D', 'J', 'K', 'L', 'Z', 'Z']

    Works lazily, keeping only the next value from each iterable in memory. Use
    :func:`collate` to, for example, perform a n-way mergesort of items that
    don't fit in memory.

    If a *key* function is specified, the iterables will be sorted according
    to its result:

        >>> key = lambda s: int(s)  # Sort by numeric value, not by string
        >>> list(collate(['1', '10'], ['2', '11'], key=key))
        ['1', '2', '10', '11']

    If the *iterables* are sorted in descending order, set *reverse* to
    ``True``:

        >>> list(collate([5, 3, 1], [4, 2, 0], reverse=True))
        [5, 4, 3, 2, 1, 0]

    If the elements of the passed-in iterables are out of order, you might get
    unexpected results.

    On Python 3.5+, this function is an alias for :func:`heapq.merge`.

    """
    warnings.warn('collate is no longer part of more_itertools, use heapq.merge', DeprecationWarning)
    return merge(*iterables, **kwargs)


def consumer(func):
    """Decorator that automatically advances a PEP-342-style "reverse iterator"
    to its first yield point so you don't have to call ``next()`` on it
    manually.

        >>> @consumer
        ... def tally():
        ...     i = 0
        ...     while True:
        ...         print('Thing number %s is %s.' % (i, (yield)))
        ...         i += 1
        ...
        >>> t = tally()
        >>> t.send('red')
        Thing number 0 is red.
        >>> t.send('fish')
        Thing number 1 is fish.

    Without the decorator, you would have to call ``next(t)`` before
    ``t.send()`` could be used.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return wrapper


def ilen(iterable):
    """Return the number of items in *iterable*.

        >>> ilen(x for x in range(1000000) if x % 3 == 0)
        333334

    This consumes the iterable, so handle with care.

    """
    counter = count()
    deque((zip(iterable, counter)), maxlen=0)
    return next(counter)


def iterate(func, start):
    """Return ``start``, ``func(start)``, ``func(func(start))``, ...

        >>> from itertools import islice
        >>> list(islice(iterate(lambda x: 2*x, 1), 10))
        [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

    """
    while True:
        yield start
        start = func(start)


def with_iter(context_manager):
    """Wrap an iterable in a ``with`` statement, so it closes once exhausted.

    For example, this will close the file when the iterator is exhausted::

        upper_lines = (line.upper() for line in with_iter(open('foo')))

    Any context manager which returns an iterable is a candidate for
    ``with_iter``.

    """
    with context_manager as (iterable):
        yield from iterable
    if False:
        yield None


def one--- This code section failed: ---

 L. 507         0  LOAD_GLOBAL              iter
                2  LOAD_FAST                'iterable'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'it'

 L. 509         8  SETUP_EXCEPT         22  'to 22'

 L. 510        10  LOAD_GLOBAL              next
               12  LOAD_FAST                'it'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  STORE_FAST               'first_value'
               18  POP_BLOCK        
               20  JUMP_FORWARD         54  'to 54'
             22_0  COME_FROM_EXCEPT      8  '8'

 L. 511        22  DUP_TOP          
               24  LOAD_GLOBAL              StopIteration
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    52  'to 52'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 512        36  LOAD_FAST                'too_short'
               38  JUMP_IF_TRUE_OR_POP    46  'to 46'
               40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 'too few items in iterable (expected 1)'
               44  CALL_FUNCTION_1       1  '1 positional argument'
             46_0  COME_FROM            38  '38'
               46  RAISE_VARARGS_1       1  'exception'
               48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM            20  '20'

 L. 514        54  SETUP_EXCEPT         68  'to 68'

 L. 515        56  LOAD_GLOBAL              next
               58  LOAD_FAST                'it'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  STORE_FAST               'second_value'
               64  POP_BLOCK        
               66  JUMP_FORWARD         88  'to 88'
             68_0  COME_FROM_EXCEPT     54  '54'

 L. 516        68  DUP_TOP          
               70  LOAD_GLOBAL              StopIteration
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE    86  'to 86'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 517        82  POP_EXCEPT       
               84  JUMP_FORWARD        112  'to 112'
               86  END_FINALLY      
             88_0  COME_FROM            66  '66'

 L. 520        88  LOAD_STR                 'Expected exactly one item in iterable, but got {!r}, {!r}, and perhaps more.'
               90  LOAD_ATTR                format

 L. 521        92  LOAD_FAST                'first_value'
               94  LOAD_FAST                'second_value'
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  STORE_FAST               'msg'

 L. 523       100  LOAD_FAST                'too_long'
              102  JUMP_IF_TRUE_OR_POP   110  'to 110'
              104  LOAD_GLOBAL              ValueError
              106  LOAD_FAST                'msg'
              108  CALL_FUNCTION_1       1  '1 positional argument'
            110_0  COME_FROM           102  '102'
              110  RAISE_VARARGS_1       1  'exception'
            112_0  COME_FROM            84  '84'

 L. 525       112  LOAD_FAST                'first_value'
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RAISE_VARARGS_1' instruction at offset 46


def distinct_permutations(iterable):
    """Yield successive distinct permutations of the elements in *iterable*.

        >>> sorted(distinct_permutations([1, 0, 1]))
        [(0, 1, 1), (1, 0, 1), (1, 1, 0)]

    Equivalent to ``set(permutations(iterable))``, except duplicates are not
    generated and thrown away. For larger input sequences this is much more
    efficient.

    Duplicate permutations arise when there are duplicated elements in the
    input iterable. The number of items returned is
    `n! / (x_1! * x_2! * ... * x_n!)`, where `n` is the total number of
    items input, and each `x_i` is the count of a distinct item in the input
    sequence.

    """

    def make_new_permutations(pool, e):
        """Internal helper function.
        The output permutations are built up by adding element *e* to the
        current *permutations* at every possible position.
        The key idea is to keep repeated elements (reverse) ordered:
        if e1 == e2 and e1 is before e2 in the iterable, then all permutations
        with e1 before e2 are ignored.

        """
        for perm in pool:
            for j in range(len(perm)):
                yield perm[:j] + (e,) + perm[j:]
                if perm[j] == e:
                    break
            else:
                yield perm + (e,)

    permutations = [()]
    for e in iterable:
        permutations = make_new_permutations(permutations, e)

    return (tuple(t) for t in permutations)


def intersperse(e, iterable, n=1):
    """Intersperse filler element *e* among the items in *iterable*, leaving
    *n* items between each filler element.

        >>> list(intersperse('!', [1, 2, 3, 4, 5]))
        [1, '!', 2, '!', 3, '!', 4, '!', 5]

        >>> list(intersperse(None, [1, 2, 3, 4, 5], n=2))
        [1, 2, None, 3, 4, None, 5]

    """
    if n == 0:
        raise ValueError('n must be > 0')
    else:
        if n == 1:
            return islice(interleave(repeat(e), iterable), 1, None)
        else:
            filler = repeat([e])
            chunks = chunked(iterable, n)
            return flatten(islice(interleave(filler, chunks), 1, None))


def unique_to_each(*iterables):
    """Return the elements from each of the input iterables that aren't in the
    other input iterables.

    For example, suppose you have a set of packages, each with a set of
    dependencies::

        {'pkg_1': {'A', 'B'}, 'pkg_2': {'B', 'C'}, 'pkg_3': {'B', 'D'}}

    If you remove one package, which dependencies can also be removed?

    If ``pkg_1`` is removed, then ``A`` is no longer necessary - it is not
    associated with ``pkg_2`` or ``pkg_3``. Similarly, ``C`` is only needed for
    ``pkg_2``, and ``D`` is only needed for ``pkg_3``::

        >>> unique_to_each({'A', 'B'}, {'B', 'C'}, {'B', 'D'})
        [['A'], ['C'], ['D']]

    If there are duplicates in one input iterable that aren't in the others
    they will be duplicated in the output. Input order is preserved::

        >>> unique_to_each("mississippi", "missouri")
        [['p', 'p'], ['o', 'u', 'r']]

    It is assumed that the elements of each iterable are hashable.

    """
    pool = [list(it) for it in iterables]
    counts = Counter(chain.from_iterable(map(set, pool)))
    uniques = {element for element in counts if counts[element] == 1}
    return [list(filter(uniques.__contains__, it)) for it in pool]


def windowed(seq, n, fillvalue=None, step=1):
    """Return a sliding window of width *n* over the given iterable.

        >>> all_windows = windowed([1, 2, 3, 4, 5], 3)
        >>> list(all_windows)
        [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    When the window is larger than the iterable, *fillvalue* is used in place
    of missing values::

        >>> list(windowed([1, 2, 3], 4))
        [(1, 2, 3, None)]

    Each window will advance in increments of *step*:

        >>> list(windowed([1, 2, 3, 4, 5, 6], 3, fillvalue='!', step=2))
        [(1, 2, 3), (3, 4, 5), (5, 6, '!')]

    To slide into the iterable's items, use :func:`chain` to add filler items
    to the left:

        >>> iterable = [1, 2, 3, 4]
        >>> n = 3
        >>> padding = [None] * (n - 1)
        >>> list(windowed(chain(padding, iterable), 3))
        [(None, None, 1), (None, 1, 2), (1, 2, 3), (2, 3, 4)]

    """
    if n < 0:
        raise ValueError('n must be >= 0')
    elif n == 0:
        yield tuple()
        return
    else:
        if step < 1:
            raise ValueError('step must be >= 1')
        it = iter(seq)
        window = deque([], n)
        append = window.append
        for _ in range(n):
            append(next(it, fillvalue))

        yield tuple(window)
        i = 0
        for item in it:
            append(item)
            i = (i + 1) % step
            if i % step == 0:
                yield tuple(window)

        if i % step:
            if step - i < n:
                for _ in range(step - i):
                    append(fillvalue)

                yield tuple(window)


def substrings(iterable):
    """Yield all of the substrings of *iterable*.

        >>> [''.join(s) for s in substrings('more')]
        ['m', 'o', 'r', 'e', 'mo', 'or', 're', 'mor', 'ore', 'more']

    Note that non-string iterables can also be subdivided.

        >>> list(substrings([0, 1, 2]))
        [(0,), (1,), (2,), (0, 1), (1, 2), (0, 1, 2)]

    """
    seq = []
    for item in iter(iterable):
        seq.append(item)
        yield (item,)

    seq = tuple(seq)
    item_count = len(seq)
    for n in range(2, item_count + 1):
        for i in range(item_count - n + 1):
            yield seq[i:i + n]


def substrings_indexes(seq, reverse=False):
    """Yield all substrings and their positions in *seq*

    The items yielded will be a tuple of the form ``(substr, i, j)``, where
    ``substr == seq[i:j]``.

    This function only works for iterables that support slicing, such as
    ``str`` objects.

    >>> for item in substrings_indexes('more'):
    ...    print(item)
    ('m', 0, 1)
    ('o', 1, 2)
    ('r', 2, 3)
    ('e', 3, 4)
    ('mo', 0, 2)
    ('or', 1, 3)
    ('re', 2, 4)
    ('mor', 0, 3)
    ('ore', 1, 4)
    ('more', 0, 4)

    Set *reverse* to ``True`` to yield the same items in the opposite order.

    """
    r = range(1, len(seq) + 1)
    if reverse:
        r = reversed(r)
    return ((seq[i:i + L], i, i + L) for L in r for i in range(len(seq) - L + 1))


class bucket:
    __doc__ = "Wrap *iterable* and return an object that buckets it iterable into\n    child iterables based on a *key* function.\n\n        >>> iterable = ['a1', 'b1', 'c1', 'a2', 'b2', 'c2', 'b3']\n        >>> s = bucket(iterable, key=lambda x: x[0])\n        >>> a_iterable = s['a']\n        >>> next(a_iterable)\n        'a1'\n        >>> next(a_iterable)\n        'a2'\n        >>> list(s['b'])\n        ['b1', 'b2', 'b3']\n\n    The original iterable will be advanced and its items will be cached until\n    they are used by the child iterables. This may require significant storage.\n\n    By default, attempting to select a bucket to which no items belong  will\n    exhaust the iterable and cache all values.\n    If you specify a *validator* function, selected buckets will instead be\n    checked against it.\n\n        >>> from itertools import count\n        >>> it = count(1, 2)  # Infinite sequence of odd numbers\n        >>> key = lambda x: x % 10  # Bucket by last digit\n        >>> validator = lambda x: x in {1, 3, 5, 7, 9}  # Odd digits only\n        >>> s = bucket(it, key=key, validator=validator)\n        >>> 2 in s\n        False\n        >>> list(s[2])\n        []\n\n    "

    def __init__(self, iterable, key, validator=None):
        self._it = iter(iterable)
        self._key = key
        self._cache = defaultdict(deque)
        self._validator = validator or (lambda x: True)

    def __contains__(self, value):
        if not self._validator(value):
            return False
        else:
            try:
                item = next(self[value])
            except StopIteration:
                return False
            else:
                self._cache[value].appendleft(item)
            return True

    def _get_values(self, value):
        """
        Helper to yield items from the parent iterator that match *value*.
        Items that don't match are stored in the local cache as they
        are encountered.
        """
        while True:
            if self._cache[value]:
                yield self._cache[value].popleft()
            else:
                while True:
                    try:
                        item = next(self._it)
                    except StopIteration:
                        return
                    else:
                        item_value = self._key(item)
                    if item_value == value:
                        yield item
                        break
                    elif self._validator(item_value):
                        self._cache[item_value].append(item)

    def __getitem__(self, value):
        if not self._validator(value):
            return iter(())
        else:
            return self._get_values(value)


def spy(iterable, n=1):
    """Return a 2-tuple with a list containing the first *n* elements of
    *iterable*, and an iterator with the same items as *iterable*.
    This allows you to "look ahead" at the items in the iterable without
    advancing it.

    There is one item in the list by default:

        >>> iterable = 'abcdefg'
        >>> head, iterable = spy(iterable)
        >>> head
        ['a']
        >>> list(iterable)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    You may use unpacking to retrieve items instead of lists:

        >>> (head,), iterable = spy('abcdefg')
        >>> head
        'a'
        >>> (first, second), iterable = spy('abcdefg', 2)
        >>> first
        'a'
        >>> second
        'b'

    The number of items requested can be larger than the number of items in
    the iterable:

        >>> iterable = [1, 2, 3, 4, 5]
        >>> head, iterable = spy(iterable, 10)
        >>> head
        [1, 2, 3, 4, 5]
        >>> list(iterable)
        [1, 2, 3, 4, 5]

    """
    it = iter(iterable)
    head = take(n, it)
    return (
     head, chain(head, it))


def interleave(*iterables):
    """Return a new iterable yielding from each iterable in turn,
    until the shortest is exhausted.

        >>> list(interleave([1, 2, 3], [4, 5], [6, 7, 8]))
        [1, 4, 6, 2, 5, 7]

    For a version that doesn't terminate after the shortest iterable is
    exhausted, see :func:`interleave_longest`.

    """
    return chain.from_iterable(zip(*iterables))


def interleave_longest(*iterables):
    """Return a new iterable yielding from each iterable in turn,
    skipping any that are exhausted.

        >>> list(interleave_longest([1, 2, 3], [4, 5], [6, 7, 8]))
        [1, 4, 6, 2, 5, 7, 3, 8]

    This function produces the same output as :func:`roundrobin`, but may
    perform better for some inputs (in particular when the number of iterables
    is large).

    """
    i = chain.from_iterable(zip_longest(*iterables, **{'fillvalue': _marker}))
    return (x for x in i if x is not _marker)


def collapse(iterable, base_type=None, levels=None):
    """Flatten an iterable with multiple levels of nesting (e.g., a list of
    lists of tuples) into non-iterable types.

        >>> iterable = [(1, 2), ([3, 4], [[5], [6]])]
        >>> list(collapse(iterable))
        [1, 2, 3, 4, 5, 6]

    Binary and text strings are not considered iterable and
    will not be collapsed.

    To avoid collapsing other types, specify *base_type*:

        >>> iterable = ['ab', ('cd', 'ef'), ['gh', 'ij']]
        >>> list(collapse(iterable, base_type=tuple))
        ['ab', ('cd', 'ef'), 'gh', 'ij']

    Specify *levels* to stop flattening after a certain level:

    >>> iterable = [('a', ['b']), ('c', ['d'])]
    >>> list(collapse(iterable))  # Fully flattened
    ['a', 'b', 'c', 'd']
    >>> list(collapse(iterable, levels=1))  # Only one level flattened
    ['a', ['b'], 'c', ['d']]

    """

    def walk(node, level):
        if levels is not None and level > levels or isinstance(node, (str, bytes)) or base_type is not None and isinstance(node, base_type):
            yield node
            return
        try:
            tree = iter(node)
        except TypeError:
            yield node
            return
        else:
            for child in tree:
                yield from walk(child, level + 1)

    yield from walk(iterable, 0)
    if False:
        yield None


def side_effect(func, iterable, chunk_size=None, before=None, after=None):
    """Invoke *func* on each item in *iterable* (or on each *chunk_size* group
    of items) before yielding the item.

    `func` must be a function that takes a single argument. Its return value
    will be discarded.

    *before* and *after* are optional functions that take no arguments. They
    will be executed before iteration starts and after it ends, respectively.

    `side_effect` can be used for logging, updating progress bars, or anything
    that is not functionally "pure."

    Emitting a status message:

        >>> from more_itertools import consume
        >>> func = lambda item: print('Received {}'.format(item))
        >>> consume(side_effect(func, range(2)))
        Received 0
        Received 1

    Operating on chunks of items:

        >>> pair_sums = []
        >>> func = lambda chunk: pair_sums.append(sum(chunk))
        >>> list(side_effect(func, [0, 1, 2, 3, 4, 5], 2))
        [0, 1, 2, 3, 4, 5]
        >>> list(pair_sums)
        [1, 5, 9]

    Writing to a file-like object:

        >>> from io import StringIO
        >>> from more_itertools import consume
        >>> f = StringIO()
        >>> func = lambda x: print(x, file=f)
        >>> before = lambda: print(u'HEADER', file=f)
        >>> after = f.close
        >>> it = [u'a', u'b', u'c']
        >>> consume(side_effect(func, it, before=before, after=after))
        >>> f.closed
        True

    """
    try:
        if before is not None:
            before()
        else:
            if chunk_size is None:
                for item in iterable:
                    func(item)
                    yield item

            else:
                for chunk in chunked(iterable, chunk_size):
                    func(chunk)
                    yield from chunk

    finally:
        if after is not None:
            after()


def sliced(seq, n):
    """Yield slices of length *n* from the sequence *seq*.

        >>> list(sliced((1, 2, 3, 4, 5, 6), 3))
        [(1, 2, 3), (4, 5, 6)]

    If the length of the sequence is not divisible by the requested slice
    length, the last slice will be shorter.

        >>> list(sliced((1, 2, 3, 4, 5, 6, 7, 8), 3))
        [(1, 2, 3), (4, 5, 6), (7, 8)]

    This function will only work for iterables that support slicing.
    For non-sliceable iterables, see :func:`chunked`.

    """
    return takewhile(bool, (seq[i:i + n] for i in count(0, n)))


def split_at(iterable, pred):
    """Yield lists of items from *iterable*, where each list is delimited by
    an item where callable *pred* returns ``True``. The lists do not include
    the delimiting items.

        >>> list(split_at('abcdcba', lambda x: x == 'b'))
        [['a'], ['c', 'd', 'c'], ['a']]

        >>> list(split_at(range(10), lambda n: n % 2 == 1))
        [[0], [2], [4], [6], [8], []]
    """
    buf = []
    for item in iterable:
        if pred(item):
            yield buf
            buf = []
        else:
            buf.append(item)

    yield buf


def split_before(iterable, pred):
    """Yield lists of items from *iterable*, where each list ends just before
    an item for which callable *pred* returns ``True``:

        >>> list(split_before('OneTwo', lambda s: s.isupper()))
        [['O', 'n', 'e'], ['T', 'w', 'o']]

        >>> list(split_before(range(10), lambda n: n % 3 == 0))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    """
    buf = []
    for item in iterable:
        if pred(item):
            if buf:
                yield buf
                buf = []
        buf.append(item)

    yield buf


def split_after(iterable, pred):
    """Yield lists of items from *iterable*, where each list ends with an
    item where callable *pred* returns ``True``:

        >>> list(split_after('one1two2', lambda s: s.isdigit()))
        [['o', 'n', 'e', '1'], ['t', 'w', 'o', '2']]

        >>> list(split_after(range(10), lambda n: n % 3 == 0))
        [[0], [1, 2, 3], [4, 5, 6], [7, 8, 9]]

    """
    buf = []
    for item in iterable:
        buf.append(item)
        if pred(item) and buf:
            yield buf
            buf = []

    if buf:
        yield buf


def split_when(iterable, pred):
    """Split *iterable* into pieces based on the output of *pred*.
    *pred* should be a function that takes successive pairs of items and
    returns ``True`` if the iterable should be split in between them.

    For example, to find runs of increasing numbers, split the iterable when
    element ``i`` is larger than element ``i + 1``:

        >>> list(split_when([1, 2, 3, 3, 2, 5, 2, 4, 2], lambda x, y: x > y))
        [[1, 2, 3, 3], [2, 5], [2, 4], [2]]
    """
    it = iter(iterable)
    try:
        cur_item = next(it)
    except StopIteration:
        return
    else:
        buf = [
         cur_item]
        for next_item in it:
            if pred(cur_item, next_item):
                yield buf
                buf = []
            buf.append(next_item)
            cur_item = next_item

        yield buf


def split_into(iterable, sizes):
    """Yield a list of sequential items from *iterable* of length 'n' for each
    integer 'n' in *sizes*.

        >>> list(split_into([1,2,3,4,5,6], [1,2,3]))
        [[1], [2, 3], [4, 5, 6]]

    If the sum of *sizes* is smaller than the length of *iterable*, then the
    remaining items of *iterable* will not be returned.

        >>> list(split_into([1,2,3,4,5,6], [2,3]))
        [[1, 2], [3, 4, 5]]

    If the sum of *sizes* is larger than the length of *iterable*, fewer items
    will be returned in the iteration that overruns *iterable* and further
    lists will be empty:

        >>> list(split_into([1,2,3,4], [1,2,3,4]))
        [[1], [2, 3], [4], []]

    When a ``None`` object is encountered in *sizes*, the returned list will
    contain items up to the end of *iterable* the same way that itertools.slice
    does:

        >>> list(split_into([1,2,3,4,5,6,7,8,9,0], [2,3,None]))
        [[1, 2], [3, 4, 5], [6, 7, 8, 9, 0]]

    :func:`split_into` can be useful for grouping a series of items where the
    sizes of the groups are not uniform. An example would be where in a row
    from a table, multiple columns represent elements of the same feature
    (e.g. a point represented by x,y,z) but, the format is not the same for
    all columns.
    """
    it = iter(iterable)
    for size in sizes:
        if size is None:
            yield list(it)
            return
        yield list(islice(it, size))


def padded(iterable, fillvalue=None, n=None, next_multiple=False):
    """Yield the elements from *iterable*, followed by *fillvalue*, such that
    at least *n* items are emitted.

        >>> list(padded([1, 2, 3], '?', 5))
        [1, 2, 3, '?', '?']

    If *next_multiple* is ``True``, *fillvalue* will be emitted until the
    number of items emitted is a multiple of *n*::

        >>> list(padded([1, 2, 3, 4], n=3, next_multiple=True))
        [1, 2, 3, 4, None, None]

    If *n* is ``None``, *fillvalue* will be emitted indefinitely.

    """
    it = iter(iterable)
    if n is None:
        yield from chain(it, repeat(fillvalue))
    else:
        if n < 1:
            raise ValueError('n must be at least 1')
        else:
            item_count = 0
            for item in it:
                yield item
                item_count += 1

            remaining = (n - item_count) % n if next_multiple else n - item_count
            for _ in range(remaining):
                yield fillvalue


def repeat_last(iterable, default=None):
    """After the *iterable* is exhausted, keep yielding its last element.

        >>> list(islice(repeat_last(range(3)), 5))
        [0, 1, 2, 2, 2]

    If the iterable is empty, yield *default* forever::

        >>> list(islice(repeat_last(range(0), 42), 5))
        [42, 42, 42, 42, 42]

    """
    item = _marker
    for item in iterable:
        yield item

    final = default if item is _marker else item
    yield from repeat(final)


def distribute(n, iterable):
    """Distribute the items from *iterable* among *n* smaller iterables.

        >>> group_1, group_2 = distribute(2, [1, 2, 3, 4, 5, 6])
        >>> list(group_1)
        [1, 3, 5]
        >>> list(group_2)
        [2, 4, 6]

    If the length of *iterable* is not evenly divisible by *n*, then the
    length of the returned iterables will not be identical:

        >>> children = distribute(3, [1, 2, 3, 4, 5, 6, 7])
        >>> [list(c) for c in children]
        [[1, 4, 7], [2, 5], [3, 6]]

    If the length of *iterable* is smaller than *n*, then the last returned
    iterables will be empty:

        >>> children = distribute(5, [1, 2, 3])
        >>> [list(c) for c in children]
        [[1], [2], [3], [], []]

    This function uses :func:`itertools.tee` and may require significant
    storage. If you need the order items in the smaller iterables to match the
    original iterable, see :func:`divide`.

    """
    if n < 1:
        raise ValueError('n must be at least 1')
    children = tee(iterable, n)
    return [islice(it, index, None, n) for index, it in enumerate(children)]


def stagger(iterable, offsets=(-1, 0, 1), longest=False, fillvalue=None):
    """Yield tuples whose elements are offset from *iterable*.
    The amount by which the `i`-th item in each tuple is offset is given by
    the `i`-th item in *offsets*.

        >>> list(stagger([0, 1, 2, 3]))
        [(None, 0, 1), (0, 1, 2), (1, 2, 3)]
        >>> list(stagger(range(8), offsets=(0, 2, 4)))
        [(0, 2, 4), (1, 3, 5), (2, 4, 6), (3, 5, 7)]

    By default, the sequence will end when the final element of a tuple is the
    last item in the iterable. To continue until the first element of a tuple
    is the last item in the iterable, set *longest* to ``True``::

        >>> list(stagger([0, 1, 2, 3], longest=True))
        [(None, 0, 1), (0, 1, 2), (1, 2, 3), (2, 3, None), (3, None, None)]

    By default, ``None`` will be used to replace offsets beyond the end of the
    sequence. Specify *fillvalue* to use some other value.

    """
    children = tee(iterable, len(offsets))
    return zip_offset(*children, offsets=offsets, longest=longest, fillvalue=fillvalue)


def zip_offset(*iterables, offsets, longest=False, fillvalue=None):
    """``zip`` the input *iterables* together, but offset the `i`-th iterable
    by the `i`-th item in *offsets*.

        >>> list(zip_offset('0123', 'abcdef', offsets=(0, 1)))
        [('0', 'b'), ('1', 'c'), ('2', 'd'), ('3', 'e')]

    This can be used as a lightweight alternative to SciPy or pandas to analyze
    data sets in which some series have a lead or lag relationship.

    By default, the sequence will end when the shortest iterable is exhausted.
    To continue until the longest iterable is exhausted, set *longest* to
    ``True``.

        >>> list(zip_offset('0123', 'abcdef', offsets=(0, 1), longest=True))
        [('0', 'b'), ('1', 'c'), ('2', 'd'), ('3', 'e'), (None, 'f')]

    By default, ``None`` will be used to replace offsets beyond the end of the
    sequence. Specify *fillvalue* to use some other value.

    """
    if len(iterables) != len(offsets):
        raise ValueError("Number of iterables and offsets didn't match")
    staggered = []
    for it, n in zip(iterables, offsets):
        if n < 0:
            staggered.append(chain(repeat(fillvalue, -n), it))
        else:
            if n > 0:
                staggered.append(islice(it, n, None))
            else:
                staggered.append(it)

    if longest:
        return zip_longest(*staggered, **{'fillvalue': fillvalue})
    else:
        return zip(*staggered)


def sort_together(iterables, key_list=(0,), reverse=False):
    """Return the input iterables sorted together, with *key_list* as the
    priority for sorting. All iterables are trimmed to the length of the
    shortest one.

    This can be used like the sorting function in a spreadsheet. If each
    iterable represents a column of data, the key list determines which
    columns are used for sorting.

    By default, all iterables are sorted using the ``0``-th iterable::

        >>> iterables = [(4, 3, 2, 1), ('a', 'b', 'c', 'd')]
        >>> sort_together(iterables)
        [(1, 2, 3, 4), ('d', 'c', 'b', 'a')]

    Set a different key list to sort according to another iterable.
    Specifying multiple keys dictates how ties are broken::

        >>> iterables = [(3, 1, 2), (0, 1, 0), ('c', 'b', 'a')]
        >>> sort_together(iterables, key_list=(1, 2))
        [(2, 3, 1), (0, 0, 1), ('a', 'c', 'b')]

    Set *reverse* to ``True`` to sort in descending order.

        >>> sort_together([(1, 2, 3), ('c', 'b', 'a')], reverse=True)
        [(3, 2, 1), ('a', 'b', 'c')]

    """
    return list(zip(*sorted(zip(*iterables),
      key=itemgetter(*key_list), reverse=reverse)))


def unzip(iterable):
    """The inverse of :func:`zip`, this function disaggregates the elements
    of the zipped *iterable*.

    The ``i``-th iterable contains the ``i``-th element from each element
    of the zipped iterable. The first element is used to to determine the
    length of the remaining elements.

        >>> iterable = [('a', 1), ('b', 2), ('c', 3), ('d', 4)]
        >>> letters, numbers = unzip(iterable)
        >>> list(letters)
        ['a', 'b', 'c', 'd']
        >>> list(numbers)
        [1, 2, 3, 4]

    This is similar to using ``zip(*iterable)``, but it avoids reading
    *iterable* into memory. Note, however, that this function uses
    :func:`itertools.tee` and thus may require significant storage.

    """
    head, iterable = spy(iter(iterable))
    if not head:
        return ()
    else:
        head = head[0]
        iterables = tee(iterable, len(head))

        def itemgetter(i):

            def getter(obj):
                try:
                    return obj[i]
                except IndexError:
                    raise StopIteration

            return getter

        return tuple(map(itemgetter(i), it) for i, it in enumerate(iterables))


def divide(n, iterable):
    """Divide the elements from *iterable* into *n* parts, maintaining
    order.

        >>> group_1, group_2 = divide(2, [1, 2, 3, 4, 5, 6])
        >>> list(group_1)
        [1, 2, 3]
        >>> list(group_2)
        [4, 5, 6]

    If the length of *iterable* is not evenly divisible by *n*, then the
    length of the returned iterables will not be identical:

        >>> children = divide(3, [1, 2, 3, 4, 5, 6, 7])
        >>> [list(c) for c in children]
        [[1, 2, 3], [4, 5], [6, 7]]

    If the length of the iterable is smaller than n, then the last returned
    iterables will be empty:

        >>> children = divide(5, [1, 2, 3])
        >>> [list(c) for c in children]
        [[1], [2], [3], [], []]

    This function will exhaust the iterable before returning and may require
    significant storage. If order is not important, see :func:`distribute`,
    which does not first pull the iterable into memory.

    """
    if n < 1:
        raise ValueError('n must be at least 1')
    seq = tuple(iterable)
    q, r = divmod(len(seq), n)
    ret = []
    for i in range(n):
        start = i * q + (i if i < r else r)
        stop = (i + 1) * q + (i + 1 if i + 1 < r else r)
        ret.append(iter(seq[start:stop]))

    return ret


def always_iterable(obj, base_type=(
 str, bytes)):
    """If *obj* is iterable, return an iterator over its items::

        >>> obj = (1, 2, 3)
        >>> list(always_iterable(obj))
        [1, 2, 3]

    If *obj* is not iterable, return a one-item iterable containing *obj*::

        >>> obj = 1
        >>> list(always_iterable(obj))
        [1]

    If *obj* is ``None``, return an empty iterable:

        >>> obj = None
        >>> list(always_iterable(None))
        []

    By default, binary and text strings are not considered iterable::

        >>> obj = 'foo'
        >>> list(always_iterable(obj))
        ['foo']

    If *base_type* is set, objects for which ``isinstance(obj, base_type)``
    returns ``True`` won't be considered iterable.

        >>> obj = {'a': 1}
        >>> list(always_iterable(obj))  # Iterate over the dict's keys
        ['a']
        >>> list(always_iterable(obj, base_type=dict))  # Treat dicts as a unit
        [{'a': 1}]

    Set *base_type* to ``None`` to avoid any special handling and treat objects
    Python considers iterable as iterable:

        >>> obj = 'foo'
        >>> list(always_iterable(obj, base_type=None))
        ['f', 'o', 'o']
    """
    if obj is None:
        return iter(())
    if base_type is not None:
        if isinstance(obj, base_type):
            return iter((obj,))
    try:
        return iter(obj)
    except TypeError:
        return iter((obj,))


def adjacent(predicate, iterable, distance=1):
    """Return an iterable over `(bool, item)` tuples where the `item` is
    drawn from *iterable* and the `bool` indicates whether
    that item satisfies the *predicate* or is adjacent to an item that does.

    For example, to find whether items are adjacent to a ``3``::

        >>> list(adjacent(lambda x: x == 3, range(6)))
        [(False, 0), (False, 1), (True, 2), (True, 3), (True, 4), (False, 5)]

    Set *distance* to change what counts as adjacent. For example, to find
    whether items are two places away from a ``3``:

        >>> list(adjacent(lambda x: x == 3, range(6), distance=2))
        [(False, 0), (True, 1), (True, 2), (True, 3), (True, 4), (True, 5)]

    This is useful for contextualizing the results of a search function.
    For example, a code comparison tool might want to identify lines that
    have changed, but also surrounding lines to give the viewer of the diff
    context.

    The predicate function will only be called once for each item in the
    iterable.

    See also :func:`groupby_transform`, which can be used with this function
    to group ranges of items with the same `bool` value.

    """
    if distance < 0:
        raise ValueError('distance must be at least 0')
    i1, i2 = tee(iterable)
    padding = [False] * distance
    selected = chain(padding, map(predicate, i1), padding)
    adjacent_to_selected = map(any, windowed(selected, 2 * distance + 1))
    return zip(adjacent_to_selected, i2)


def groupby_transform(iterable, keyfunc=None, valuefunc=None):
    """An extension of :func:`itertools.groupby` that transforms the values of
    *iterable* after grouping them.
    *keyfunc* is a function used to compute a grouping key for each item.
    *valuefunc* is a function for transforming the items after grouping.

        >>> iterable = 'AaaABbBCcA'
        >>> keyfunc = lambda x: x.upper()
        >>> valuefunc = lambda x: x.lower()
        >>> grouper = groupby_transform(iterable, keyfunc, valuefunc)
        >>> [(k, ''.join(g)) for k, g in grouper]
        [('A', 'aaaa'), ('B', 'bbb'), ('C', 'cc'), ('A', 'a')]

    *keyfunc* and *valuefunc* default to identity functions if they are not
    specified.

    :func:`groupby_transform` is useful when grouping elements of an iterable
    using a separate iterable as the key. To do this, :func:`zip` the iterables
    and pass a *keyfunc* that extracts the first element and a *valuefunc*
    that extracts the second element::

        >>> from operator import itemgetter
        >>> keys = [0, 0, 1, 1, 1, 2, 2, 2, 3]
        >>> values = 'abcdefghi'
        >>> iterable = zip(keys, values)
        >>> grouper = groupby_transform(iterable, itemgetter(0), itemgetter(1))
        >>> [(k, ''.join(g)) for k, g in grouper]
        [(0, 'ab'), (1, 'cde'), (2, 'fgh'), (3, 'i')]

    Note that the order of items in the iterable is significant.
    Only adjacent items are grouped together, so if you don't want any
    duplicate groups, you should sort the iterable by the key function.

    """
    res = groupby(iterable, keyfunc)
    if valuefunc:
        return ((k, map(valuefunc, g)) for k, g in res)
    else:
        return res


def numeric_range(*args):
    """An extension of the built-in ``range()`` function whose arguments can
    be any orderable numeric type.

    With only *stop* specified, *start* defaults to ``0`` and *step*
    defaults to ``1``. The output items will match the type of *stop*:

        >>> list(numeric_range(3.5))
        [0.0, 1.0, 2.0, 3.0]

    With only *start* and *stop* specified, *step* defaults to ``1``. The
    output items will match the type of *start*:

        >>> from decimal import Decimal
        >>> start = Decimal('2.1')
        >>> stop = Decimal('5.1')
        >>> list(numeric_range(start, stop))
        [Decimal('2.1'), Decimal('3.1'), Decimal('4.1')]

    With *start*, *stop*, and *step*  specified the output items will match
    the type of ``start + step``:

        >>> from fractions import Fraction
        >>> start = Fraction(1, 2)  # Start at 1/2
        >>> stop = Fraction(5, 2)  # End at 5/2
        >>> step = Fraction(1, 2)  # Count by 1/2
        >>> list(numeric_range(start, stop, step))
        [Fraction(1, 2), Fraction(1, 1), Fraction(3, 2), Fraction(2, 1)]

    If *step* is zero, ``ValueError`` is raised. Negative steps are supported:

        >>> list(numeric_range(3, -1, -1.0))
        [3.0, 2.0, 1.0, 0.0]

    Be aware of the limitations of floating point numbers; the representation
    of the yielded numbers may be surprising.

    ``datetime.datetime`` objects can be used for *start* and *stop*, if *step*
    is a ``datetime.timedelta`` object:

        >>> import datetime
        >>> start = datetime.datetime(2019, 1, 1)
        >>> stop = datetime.datetime(2019, 1, 3)
        >>> step = datetime.timedelta(days=1)
        >>> items = numeric_range(start, stop, step)
        >>> next(items)
        datetime.datetime(2019, 1, 1, 0, 0)
        >>> next(items)
        datetime.datetime(2019, 1, 2, 0, 0)

    """
    argc = len(args)
    if argc == 1:
        stop, = args
        start = type(stop)(0)
        step = 1
    else:
        if argc == 2:
            start, stop = args
            step = 1
        else:
            if argc == 3:
                start, stop, step = args
            else:
                err_msg = 'numeric_range takes at most 3 arguments, got {}'
                raise TypeError(err_msg.format(argc))
    values = (start + step * n for n in count())
    zero = type(step)(0)
    if step > zero:
        return takewhile(partial(gt, stop), values)
    if step < zero:
        return takewhile(partial(lt, stop), values)
    raise ValueError('numeric_range arg 3 must not be zero')


def count_cycle(iterable, n=None):
    """Cycle through the items from *iterable* up to *n* times, yielding
    the number of completed cycles along with each item. If *n* is omitted the
    process repeats indefinitely.

    >>> list(count_cycle('AB', 3))
    [(0, 'A'), (0, 'B'), (1, 'A'), (1, 'B'), (2, 'A'), (2, 'B')]

    """
    iterable = tuple(iterable)
    if not iterable:
        return iter(())
    else:
        counter = count() if n is None else range(n)
        return ((i, item) for i in counter for item in iterable)


def locate(iterable, pred=bool, window_size=None):
    """Yield the index of each item in *iterable* for which *pred* returns
    ``True``.

    *pred* defaults to :func:`bool`, which will select truthy items:

        >>> list(locate([0, 1, 1, 0, 1, 0, 0]))
        [1, 2, 4]

    Set *pred* to a custom function to, e.g., find the indexes for a particular
    item.

        >>> list(locate(['a', 'b', 'c', 'b'], lambda x: x == 'b'))
        [1, 3]

    If *window_size* is given, then the *pred* function will be called with
    that many items. This enables searching for sub-sequences:

        >>> iterable = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
        >>> pred = lambda *args: args == (1, 2, 3)
        >>> list(locate(iterable, pred=pred, window_size=3))
        [1, 5, 9]

    Use with :func:`seekable` to find indexes and then retrieve the associated
    items:

        >>> from itertools import count
        >>> from more_itertools import seekable
        >>> source = (3 * n + 1 if (n % 2) else n // 2 for n in count())
        >>> it = seekable(source)
        >>> pred = lambda x: x > 100
        >>> indexes = locate(it, pred=pred)
        >>> i = next(indexes)
        >>> it.seek(i)
        >>> next(it)
        106

    """
    if window_size is None:
        return compress(count(), map(pred, iterable))
    else:
        if window_size < 1:
            raise ValueError('window size must be at least 1')
        it = windowed(iterable, window_size, fillvalue=_marker)
        return compress(count(), starmap(pred, it))


def lstrip(iterable, pred):
    """Yield the items from *iterable*, but strip any from the beginning
    for which *pred* returns ``True``.

    For example, to remove a set of items from the start of an iterable:

        >>> iterable = (None, False, None, 1, 2, None, 3, False, None)
        >>> pred = lambda x: x in {None, False, ''}
        >>> list(lstrip(iterable, pred))
        [1, 2, None, 3, False, None]

    This function is analogous to to :func:`str.lstrip`, and is essentially
    an wrapper for :func:`itertools.dropwhile`.

    """
    return dropwhile(pred, iterable)


def rstrip(iterable, pred):
    """Yield the items from *iterable*, but strip any from the end
    for which *pred* returns ``True``.

    For example, to remove a set of items from the end of an iterable:

        >>> iterable = (None, False, None, 1, 2, None, 3, False, None)
        >>> pred = lambda x: x in {None, False, ''}
        >>> list(rstrip(iterable, pred))
        [None, False, None, 1, 2, None, 3]

    This function is analogous to :func:`str.rstrip`.

    """
    cache = []
    cache_append = cache.append
    cache_clear = cache.clear
    for x in iterable:
        if pred(x):
            cache_append(x)
        else:
            yield from cache
            cache_clear()
            yield x


def strip(iterable, pred):
    """Yield the items from *iterable*, but strip any from the
    beginning and end for which *pred* returns ``True``.

    For example, to remove a set of items from both ends of an iterable:

        >>> iterable = (None, False, None, 1, 2, None, 3, False, None)
        >>> pred = lambda x: x in {None, False, ''}
        >>> list(strip(iterable, pred))
        [1, 2, None, 3]

    This function is analogous to :func:`str.strip`.

    """
    return rstrip(lstrip(iterable, pred), pred)


def islice_extended(iterable, *args):
    """An extension of :func:`itertools.islice` that supports negative values
    for *stop*, *start*, and *step*.

        >>> iterable = iter('abcdefgh')
        >>> list(islice_extended(iterable, -4, -1))
        ['e', 'f', 'g']

    Slices with negative values require some caching of *iterable*, but this
    function takes care to minimize the amount of memory required.

    For example, you can use a negative step with an infinite iterator:

        >>> from itertools import count
        >>> list(islice_extended(count(), 110, 99, -2))
        [110, 108, 106, 104, 102, 100]

    """
    s = slice(*args)
    start = s.start
    stop = s.stop
    if s.step == 0:
        raise ValueError('step argument must be a non-zero integer or None.')
    step = s.step or 1
    it = iter(iterable)
    if step > 0:
        start = 0 if start is None else start
        if start < 0:
            cache = deque((enumerate(it, 1)), maxlen=(-start))
            len_iter = cache[(-1)][0] if cache else 0
            i = max(len_iter + start, 0)
            if stop is None:
                j = len_iter
            else:
                if stop >= 0:
                    j = min(stop, len_iter)
                else:
                    j = max(len_iter + stop, 0)
            n = j - i
            if n <= 0:
                return
            for index, item in islice(cache, 0, n, step):
                yield item

        elif stop is not None:
            if stop < 0:
                next(islice(it, start, start), None)
                cache = deque((islice(it, -stop)), maxlen=(-stop))
                for index, item in enumerate(it):
                    cached_item = cache.popleft()
                    if index % step == 0:
                        yield cached_item
                    cache.append(item)

        else:
            yield from islice(it, start, stop, step)
    else:
        start = -1 if start is None else start
    if stop is not None and stop < 0:
        n = -stop - 1
        cache = deque((enumerate(it, 1)), maxlen=n)
        len_iter = cache[(-1)][0] if cache else 0
        if start < 0:
            i, j = start, stop
        else:
            i, j = min(start - len_iter, -1), None
        for index, item in list(cache)[i:j:step]:
            yield item

    else:
        if stop is not None:
            m = stop + 1
            next(islice(it, m, m), None)
        if start < 0:
            i = start
            n = None
        else:
            if stop is None:
                i = None
                n = start + 1
            else:
                i = None
                n = start - stop
                if n <= 0:
                    return
                cache = list(islice(it, n))
                yield from cache[i::step]


def always_reversible(iterable):
    """An extension of :func:`reversed` that supports all iterables, not
    just those which implement the ``Reversible`` or ``Sequence`` protocols.

        >>> print(*always_reversible(x for x in range(3)))
        2 1 0

    If the iterable is already reversible, this function returns the
    result of :func:`reversed()`. If the iterable is not reversible,
    this function will cache the remaining items in the iterable and
    yield them in reverse order, which may require significant storage.
    """
    try:
        return reversed(iterable)
    except TypeError:
        return reversed(list(iterable))


def consecutive_groups(iterable, ordering=lambda x: x):
    """Yield groups of consecutive items using :func:`itertools.groupby`.
    The *ordering* function determines whether two items are adjacent by
    returning their position.

    By default, the ordering function is the identity function. This is
    suitable for finding runs of numbers:

        >>> iterable = [1, 10, 11, 12, 20, 30, 31, 32, 33, 40]
        >>> for group in consecutive_groups(iterable):
        ...     print(list(group))
        [1]
        [10, 11, 12]
        [20]
        [30, 31, 32, 33]
        [40]

    For finding runs of adjacent letters, try using the :meth:`index` method
    of a string of letters:

        >>> from string import ascii_lowercase
        >>> iterable = 'abcdfgilmnop'
        >>> ordering = ascii_lowercase.index
        >>> for group in consecutive_groups(iterable, ordering):
        ...     print(list(group))
        ['a', 'b', 'c', 'd']
        ['f', 'g']
        ['i']
        ['l', 'm', 'n', 'o', 'p']

    Each group of consecutive items is an iterator that shares it source with
    *iterable*. When an an output group is advanced, the previous group is
    no longer available unless its elements are copied (e.g., into a ``list``).

        >>> iterable = [1, 2, 11, 12, 21, 22]
        >>> saved_groups = []
        >>> for group in consecutive_groups(iterable):
        ...     saved_groups.append(list(group))  # Copy group elements
        >>> saved_groups
        [[1, 2], [11, 12], [21, 22]]

    """
    for k, g in groupby((enumerate(iterable)),
      key=(lambda x: x[0] - ordering(x[1]))):
        yield map(itemgetter(1), g)


def difference(iterable, func=sub, *, initial=None):
    """By default, compute the first difference of *iterable* using
    :func:`operator.sub`.

        >>> iterable = [0, 1, 3, 6, 10]
        >>> list(difference(iterable))
        [0, 1, 2, 3, 4]

    This is the opposite of :func:`itertools.accumulate`'s default behavior:

        >>> from itertools import accumulate
        >>> iterable = [0, 1, 2, 3, 4]
        >>> list(accumulate(iterable))
        [0, 1, 3, 6, 10]
        >>> list(difference(accumulate(iterable)))
        [0, 1, 2, 3, 4]

    By default *func* is :func:`operator.sub`, but other functions can be
    specified. They will be applied as follows::

        A, B, C, D, ... --> A, func(B, A), func(C, B), func(D, C), ...

    For example, to do progressive division:

        >>> iterable = [1, 2, 6, 24, 120]  # Factorial sequence
        >>> func = lambda x, y: x // y
        >>> list(difference(iterable, func))
        [1, 2, 3, 4, 5]

    Since Python 3.8, :func:`itertools.accumulate` can be supplied with an
    *initial* keyword argument. If :func:`difference` is called with *initial*
    set to something other than ``None``, it will skip the first element when
    computing successive differences.

        >>> iterable = [100, 101, 103, 106]  # accumate([1, 2, 3], initial=100)
        >>> list(difference(iterable, initial=100))
        [1, 2, 3]

    """
    a, b = tee(iterable)
    try:
        first = [
         next(b)]
    except StopIteration:
        return iter([])
    else:
        if initial is not None:
            first = []
        return chain(first, starmap(func, zip(b, a)))


class SequenceView(Sequence):
    __doc__ = 'Return a read-only view of the sequence object *target*.\n\n    :class:`SequenceView` objects are analogous to Python\'s built-in\n    "dictionary view" types. They provide a dynamic view of a sequence\'s items,\n    meaning that when the sequence updates, so does the view.\n\n        >>> seq = [\'0\', \'1\', \'2\']\n        >>> view = SequenceView(seq)\n        >>> view\n        SequenceView([\'0\', \'1\', \'2\'])\n        >>> seq.append(\'3\')\n        >>> view\n        SequenceView([\'0\', \'1\', \'2\', \'3\'])\n\n    Sequence views support indexing, slicing, and length queries. They act\n    like the underlying sequence, except they don\'t allow assignment:\n\n        >>> view[1]\n        \'1\'\n        >>> view[1:-1]\n        [\'1\', \'2\']\n        >>> len(view)\n        4\n\n    Sequence views are useful as an alternative to copying, as they don\'t\n    require (much) extra storage.\n\n    '

    def __init__(self, target):
        if not isinstance(target, Sequence):
            raise TypeError
        self._target = target

    def __getitem__(self, index):
        return self._target[index]

    def __len__(self):
        return len(self._target)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self._target))


class seekable:
    __doc__ = 'Wrap an iterator to allow for seeking backward and forward. This\n    progressively caches the items in the source iterable so they can be\n    re-visited.\n\n    Call :meth:`seek` with an index to seek to that position in the source\n    iterable.\n\n    To "reset" an iterator, seek to ``0``:\n\n        >>> from itertools import count\n        >>> it = seekable((str(n) for n in count()))\n        >>> next(it), next(it), next(it)\n        (\'0\', \'1\', \'2\')\n        >>> it.seek(0)\n        >>> next(it), next(it), next(it)\n        (\'0\', \'1\', \'2\')\n        >>> next(it)\n        \'3\'\n\n    You can also seek forward:\n\n        >>> it = seekable((str(n) for n in range(20)))\n        >>> it.seek(10)\n        >>> next(it)\n        \'10\'\n        >>> it.seek(20)  # Seeking past the end of the source isn\'t a problem\n        >>> list(it)\n        []\n        >>> it.seek(0)  # Resetting works even after hitting the end\n        >>> next(it), next(it), next(it)\n        (\'0\', \'1\', \'2\')\n\n    The cache grows as the source iterable progresses, so beware of wrapping\n    very large or infinite iterables.\n\n    You may view the contents of the cache with the :meth:`elements` method.\n    That returns a :class:`SequenceView`, a view that updates automatically:\n\n        >>> it = seekable((str(n) for n in range(10)))\n        >>> next(it), next(it), next(it)\n        (\'0\', \'1\', \'2\')\n        >>> elements = it.elements()\n        >>> elements\n        SequenceView([\'0\', \'1\', \'2\'])\n        >>> next(it)\n        \'3\'\n        >>> elements\n        SequenceView([\'0\', \'1\', \'2\', \'3\'])\n\n    '

    def __init__(self, iterable):
        self._source = iter(iterable)
        self._cache = []
        self._index = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._index is not None:
            try:
                item = self._cache[self._index]
            except IndexError:
                self._index = None
            else:
                self._index += 1
                return item
        item = next(self._source)
        self._cache.append(item)
        return item

    def elements(self):
        return SequenceView(self._cache)

    def seek(self, index):
        self._index = index
        remainder = index - len(self._cache)
        if remainder > 0:
            consume(self, remainder)


class run_length:
    __doc__ = "\n    :func:`run_length.encode` compresses an iterable with run-length encoding.\n    It yields groups of repeated items with the count of how many times they\n    were repeated:\n\n        >>> uncompressed = 'abbcccdddd'\n        >>> list(run_length.encode(uncompressed))\n        [('a', 1), ('b', 2), ('c', 3), ('d', 4)]\n\n    :func:`run_length.decode` decompresses an iterable that was previously\n    compressed with run-length encoding. It yields the items of the\n    decompressed iterable:\n\n        >>> compressed = [('a', 1), ('b', 2), ('c', 3), ('d', 4)]\n        >>> list(run_length.decode(compressed))\n        ['a', 'b', 'b', 'c', 'c', 'c', 'd', 'd', 'd', 'd']\n\n    "

    @staticmethod
    def encode(iterable):
        return ((k, ilen(g)) for k, g in groupby(iterable))

    @staticmethod
    def decode(iterable):
        return chain.from_iterable(repeat(k, n) for k, n in iterable)


def exactly_n(iterable, n, predicate=bool):
    """Return ``True`` if exactly ``n`` items in the iterable are ``True``
    according to the *predicate* function.

        >>> exactly_n([True, True, False], 2)
        True
        >>> exactly_n([True, True, False], 1)
        False
        >>> exactly_n([0, 1, 2, 3, 4, 5], 3, lambda x: x < 3)
        True

    The iterable will be advanced until ``n + 1`` truthy items are encountered,
    so avoid calling it on infinite iterables.

    """
    return len(take(n + 1, filter(predicate, iterable))) == n


def circular_shifts(iterable):
    """Return a list of circular shifts of *iterable*.

        >>> circular_shifts(range(4))
        [(0, 1, 2, 3), (1, 2, 3, 0), (2, 3, 0, 1), (3, 0, 1, 2)]
    """
    lst = list(iterable)
    return take(len(lst), windowed(cycle(lst), len(lst)))


def make_decorator(wrapping_func, result_index=0):
    """Return a decorator version of *wrapping_func*, which is a function that
    modifies an iterable. *result_index* is the position in that function's
    signature where the iterable goes.

    This lets you use itertools on the "production end," i.e. at function
    definition. This can augment what the function returns without changing the
    function's code.

    For example, to produce a decorator version of :func:`chunked`:

        >>> from more_itertools import chunked
        >>> chunker = make_decorator(chunked, result_index=0)
        >>> @chunker(3)
        ... def iter_range(n):
        ...     return iter(range(n))
        ...
        >>> list(iter_range(9))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    To only allow truthy items to be returned:

        >>> truth_serum = make_decorator(filter, result_index=1)
        >>> @truth_serum(bool)
        ... def boolean_test():
        ...     return [0, 1, '', ' ', False, True]
        ...
        >>> list(boolean_test())
        [1, ' ', True]

    The :func:`peekable` and :func:`seekable` wrappers make for practical
    decorators:

        >>> from more_itertools import peekable
        >>> peekable_function = make_decorator(peekable)
        >>> @peekable_function()
        ... def str_range(*args):
        ...     return (str(x) for x in range(*args))
        ...
        >>> it = str_range(1, 20, 2)
        >>> next(it), next(it), next(it)
        ('1', '3', '5')
        >>> it.peek()
        '7'
        >>> next(it)
        '7'

    """

    def decorator(*wrapping_args, **wrapping_kwargs):

        def outer_wrapper(f):

            def inner_wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                wrapping_args_ = list(wrapping_args)
                wrapping_args_.insert(result_index, result)
                return wrapping_func(*wrapping_args_, **wrapping_kwargs)

            return inner_wrapper

        return outer_wrapper

    return decorator


def map_reduce(iterable, keyfunc, valuefunc=None, reducefunc=None):
    """Return a dictionary that maps the items in *iterable* to categories
    defined by *keyfunc*, transforms them with *valuefunc*, and
    then summarizes them by category with *reducefunc*.

    *valuefunc* defaults to the identity function if it is unspecified.
    If *reducefunc* is unspecified, no summarization takes place:

        >>> keyfunc = lambda x: x.upper()
        >>> result = map_reduce('abbccc', keyfunc)
        >>> sorted(result.items())
        [('A', ['a']), ('B', ['b', 'b']), ('C', ['c', 'c', 'c'])]

    Specifying *valuefunc* transforms the categorized items:

        >>> keyfunc = lambda x: x.upper()
        >>> valuefunc = lambda x: 1
        >>> result = map_reduce('abbccc', keyfunc, valuefunc)
        >>> sorted(result.items())
        [('A', [1]), ('B', [1, 1]), ('C', [1, 1, 1])]

    Specifying *reducefunc* summarizes the categorized items:

        >>> keyfunc = lambda x: x.upper()
        >>> valuefunc = lambda x: 1
        >>> reducefunc = sum
        >>> result = map_reduce('abbccc', keyfunc, valuefunc, reducefunc)
        >>> sorted(result.items())
        [('A', 1), ('B', 2), ('C', 3)]

    You may want to filter the input iterable before applying the map/reduce
    procedure:

        >>> all_items = range(30)
        >>> items = [x for x in all_items if 10 <= x <= 20]  # Filter
        >>> keyfunc = lambda x: x % 2  # Evens map to 0; odds to 1
        >>> categories = map_reduce(items, keyfunc=keyfunc)
        >>> sorted(categories.items())
        [(0, [10, 12, 14, 16, 18, 20]), (1, [11, 13, 15, 17, 19])]
        >>> summaries = map_reduce(items, keyfunc=keyfunc, reducefunc=sum)
        >>> sorted(summaries.items())
        [(0, 90), (1, 75)]

    Note that all items in the iterable are gathered into a list before the
    summarization step, which may require significant storage.

    The returned object is a :obj:`collections.defaultdict` with the
    ``default_factory`` set to ``None``, such that it behaves like a normal
    dictionary.

    """
    valuefunc = (lambda x: x) if valuefunc is None else valuefunc
    ret = defaultdict(list)
    for item in iterable:
        key = keyfunc(item)
        value = valuefunc(item)
        ret[key].append(value)

    if reducefunc is not None:
        for key, value_list in ret.items():
            ret[key] = reducefunc(value_list)

    ret.default_factory = None
    return ret


def rlocate(iterable, pred=bool, window_size=None):
    """Yield the index of each item in *iterable* for which *pred* returns
    ``True``, starting from the right and moving left.

    *pred* defaults to :func:`bool`, which will select truthy items:

        >>> list(rlocate([0, 1, 1, 0, 1, 0, 0]))  # Truthy at 1, 2, and 4
        [4, 2, 1]

    Set *pred* to a custom function to, e.g., find the indexes for a particular
    item:

        >>> iterable = iter('abcb')
        >>> pred = lambda x: x == 'b'
        >>> list(rlocate(iterable, pred))
        [3, 1]

    If *window_size* is given, then the *pred* function will be called with
    that many items. This enables searching for sub-sequences:

        >>> iterable = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
        >>> pred = lambda *args: args == (1, 2, 3)
        >>> list(rlocate(iterable, pred=pred, window_size=3))
        [9, 5, 1]

    Beware, this function won't return anything for infinite iterables.
    If *iterable* is reversible, ``rlocate`` will reverse it and search from
    the right. Otherwise, it will search from the left and return the results
    in reverse order.

    See :func:`locate` to for other example applications.

    """
    if window_size is None:
        try:
            len_iter = len(iterable)
            return (len_iter - i - 1 for i in locate(reversed(iterable), pred))
        except TypeError:
            pass

    return reversed(list(locate(iterable, pred, window_size)))


def replace(iterable, pred, substitutes, count=None, window_size=1):
    """Yield the items from *iterable*, replacing the items for which *pred*
    returns ``True`` with the items from the iterable *substitutes*.

        >>> iterable = [1, 1, 0, 1, 1, 0, 1, 1]
        >>> pred = lambda x: x == 0
        >>> substitutes = (2, 3)
        >>> list(replace(iterable, pred, substitutes))
        [1, 1, 2, 3, 1, 1, 2, 3, 1, 1]

    If *count* is given, the number of replacements will be limited:

        >>> iterable = [1, 1, 0, 1, 1, 0, 1, 1, 0]
        >>> pred = lambda x: x == 0
        >>> substitutes = [None]
        >>> list(replace(iterable, pred, substitutes, count=2))
        [1, 1, None, 1, 1, None, 1, 1, 0]

    Use *window_size* to control the number of items passed as arguments to
    *pred*. This allows for locating and replacing subsequences.

        >>> iterable = [0, 1, 2, 5, 0, 1, 2, 5]
        >>> window_size = 3
        >>> pred = lambda *args: args == (0, 1, 2)  # 3 items passed to pred
        >>> substitutes = [3, 4] # Splice in these items
        >>> list(replace(iterable, pred, substitutes, window_size=window_size))
        [3, 4, 5, 3, 4, 5]

    """
    if window_size < 1:
        raise ValueError('window_size must be at least 1')
    substitutes = tuple(substitutes)
    it = chain(iterable, [_marker] * (window_size - 1))
    windows = windowed(it, window_size)
    n = 0
    for w in windows:
        if pred(*w):
            if count is None or n < count:
                n += 1
                yield from substitutes
                consume(windows, window_size - 1)
                continue
            if w and w[0] is not _marker:
                yield w[0]


def partitions(iterable):
    """Yield all possible order-perserving partitions of *iterable*.

    >>> iterable = 'abc'
    >>> for part in partitions(iterable):
    ...     print([''.join(p) for p in part])
    ['abc']
    ['a', 'bc']
    ['ab', 'c']
    ['a', 'b', 'c']

    This is unrelated to :func:`partition`.

    """
    sequence = list(iterable)
    n = len(sequence)
    for i in powerset(range(1, n)):
        yield [sequence[i:j] for i, j in zip((0, ) + i, i + (n,))]


def set_partitions(iterable, k=None):
    """
    Yield the set partitions of *iterable* into *k* parts. Set partitions are
    not order-preserving.

    >>> iterable = 'abc'
    >>> for part in set_partitions(iterable, 2):
    ...     print([''.join(p) for p in part])
    ['a', 'bc']
    ['ab', 'c']
    ['b', 'ac']

    If *k* is not given, every set partition is generated.

    >>> iterable = 'abc'
    >>> for part in set_partitions(iterable):
    ...     print([''.join(p) for p in part])
    ['abc']
    ['a', 'bc']
    ['ab', 'c']
    ['b', 'ac']
    ['a', 'b', 'c']

    """
    L = list(iterable)
    n = len(L)
    if k is not None:
        if k < 1:
            raise ValueError("Can't partition in a negative or zero number of groups")
        elif k > n:
            return
    else:

        def set_partitions_helper(L, k):
            n = len(L)
            if k == 1:
                yield [
                 L]
            else:
                if n == k:
                    yield [[s] for s in L]
                else:
                    e, *M = L
                    for p in set_partitions_helper(M, k - 1):
                        yield [
                         
                          [
                           e], *p]

                    for p in set_partitions_helper(M, k):
                        for i in range(len(p)):
                            yield p[:i] + [[e] + p[i]] + p[i + 1:]

        if k is None:
            for k in range(1, n + 1):
                yield from set_partitions_helper(L, k)

        else:
            yield from set_partitions_helper(L, k)
    if False:
        yield None


def time_limited(limit_seconds, iterable):
    """
    Yield items from *iterable* until *limit_seconds* have passed.

    >>> from time import sleep
    >>> def generator():
    ...     yield 1
    ...     yield 2
    ...     sleep(0.2)
    ...     yield 3
    >>> iterable = generator()
    >>> list(time_limited(0.1, iterable))
    [1, 2]

    Note that the time is checked before each item is yielded, and iteration
    stops if  the time elapsed is greater than *limit_seconds*. If your time
    limit is 1 second, but it takes 2 seconds to generate the first item from
    the iterable, the function will run for 2 seconds and not yield anything.

    """
    if limit_seconds < 0:
        raise ValueError('limit_seconds must be positive')
    start_time = monotonic()
    for item in iterable:
        if monotonic() - start_time > limit_seconds:
            break
        yield item


def only--- This code section failed: ---

 L.2571         0  LOAD_GLOBAL              iter
                2  LOAD_FAST                'iterable'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'it'

 L.2572         8  LOAD_GLOBAL              next
               10  LOAD_FAST                'it'
               12  LOAD_FAST                'default'
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  STORE_FAST               'first_value'

 L.2574        18  SETUP_EXCEPT         32  'to 32'

 L.2575        20  LOAD_GLOBAL              next
               22  LOAD_FAST                'it'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  STORE_FAST               'second_value'
               28  POP_BLOCK        
               30  JUMP_FORWARD         52  'to 52'
             32_0  COME_FROM_EXCEPT     18  '18'

 L.2576        32  DUP_TOP          
               34  LOAD_GLOBAL              StopIteration
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    50  'to 50'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.2577        46  POP_EXCEPT       
               48  JUMP_FORWARD         76  'to 76'
               50  END_FINALLY      
             52_0  COME_FROM            30  '30'

 L.2580        52  LOAD_STR                 'Expected exactly one item in iterable, but got {!r}, {!r}, and perhaps more.'
               54  LOAD_ATTR                format

 L.2581        56  LOAD_FAST                'first_value'
               58  LOAD_FAST                'second_value'
               60  CALL_FUNCTION_2       2  '2 positional arguments'
               62  STORE_FAST               'msg'

 L.2583        64  LOAD_FAST                'too_long'
               66  JUMP_IF_TRUE_OR_POP    74  'to 74'
               68  LOAD_GLOBAL              ValueError
               70  LOAD_FAST                'msg'
               72  CALL_FUNCTION_1       1  '1 positional argument'
             74_0  COME_FROM            66  '66'
               74  RAISE_VARARGS_1       1  'exception'
             76_0  COME_FROM            48  '48'

 L.2585        76  LOAD_FAST                'first_value'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RAISE_VARARGS_1' instruction at offset 74


def ichunked(iterable, n):
    """Break *iterable* into sub-iterables with *n* elements each.
    :func:`ichunked` is like :func:`chunked`, but it yields iterables
    instead of lists.

    If the sub-iterables are read in order, the elements of *iterable*
    won't be stored in memory.
    If they are read out of order, :func:`itertools.tee` is used to cache
    elements as necessary.

    >>> from itertools import count
    >>> all_chunks = ichunked(count(), 4)
    >>> c_1, c_2, c_3 = next(all_chunks), next(all_chunks), next(all_chunks)
    >>> list(c_2)  # c_1's elements have been cached; c_3's haven't been
    [4, 5, 6, 7]
    >>> list(c_1)
    [0, 1, 2, 3]
    >>> list(c_3)
    [8, 9, 10, 11]

    """
    source = iter(iterable)
    while True:
        item = next(source, _marker)
        if item is _marker:
            return
        source, it = tee(chain([item], source))
        yield islice(it, n)
        consume(source, n)


def distinct_combinations(iterable, r):
    """Yield the distinct combinations of *r* items taken from *iterable*.

        >>> list(distinct_combinations([0, 0, 1], 2))
        [(0, 0), (0, 1)]

    Equivalent to ``set(combinations(iterable))``, except duplicates are not
    generated and thrown away. For larger input sequences this is much more
    efficient.

    """
    if r < 0:
        raise ValueError('r must be non-negative')
    else:
        if r == 0:
            yield ()
        else:
            pool = tuple(iterable)
            for i, prefix in unique_everseen((enumerate(pool)), key=(itemgetter(1))):
                for suffix in distinct_combinations(pool[i + 1:], r - 1):
                    yield (
                     prefix,) + suffix


def filter_except(validator, iterable, *exceptions):
    """Yield the items from *iterable* for which the *validator* function does
    not raise one of the specified *exceptions*.

    *validator* is called for each item in *iterable*.
    It should be a function that accepts one argument and raises an exception
    if that item is not valid.

    >>> iterable = ['1', '2', 'three', '4', None]
    >>> list(filter_except(int, iterable, ValueError, TypeError))
    ['1', '2', '4']

    If an exception other than one given by *exceptions* is raised by
    *validator*, it is raised like normal.
    """
    exceptions = tuple(exceptions)
    for item in iterable:
        try:
            validator(item)
        except exceptions:
            pass
        else:
            yield item


def map_except(function, iterable, *exceptions):
    """Transform each item from *iterable* with *function* and yield the
    result, unless *function* raises one of the specified *exceptions*.

    *function* is called to transform each item in *iterable*.
    It should be a accept one argument.

    >>> iterable = ['1', '2', 'three', '4', None]
    >>> list(map_except(int, iterable, ValueError, TypeError))
    [1, 2, 4]

    If an exception other than one given by *exceptions* is raised by
    *function*, it is raised like normal.
    """
    exceptions = tuple(exceptions)
    for item in iterable:
        try:
            yield function(item)
        except exceptions:
            pass
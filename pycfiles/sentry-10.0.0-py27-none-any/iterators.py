# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/iterators.py
# Compiled at: 2019-08-16 12:27:43
from __future__ import absolute_import
import itertools

def advance(n, iterator):
    """Advances an iterator n places."""
    next(itertools.islice(iterator, n, n), None)
    return iterator


def shingle(n, iterator):
    """    Shingle a token stream into N-grams.

    >>> list(shingle(2, ('foo', 'bar', 'baz')))
    [('foo', 'bar'), ('bar', 'baz')]
    """
    return itertools.izip(*map(lambda i__iterator: advance(i__iterator[0], i__iterator[1]), enumerate(itertools.tee(iterator, n))))


def chunked(iterator, size):
    chunk = []
    for item in iterator:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
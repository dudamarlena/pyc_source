# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/cursors.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import six
from collections import Sequence

class Cursor(object):

    def __init__(self, value, offset=0, is_prev=False, has_results=None):
        self.value = int(value)
        self.offset = int(offset)
        self.is_prev = bool(is_prev)
        self.has_results = has_results

    def __str__(self):
        return '%s:%s:%s' % (self.value, self.offset, int(self.is_prev))

    def __eq__(self, other):
        return all(getattr(self, attr) == getattr(other, attr) for attr in ('value',
                                                                            'offset',
                                                                            'is_prev',
                                                                            'has_results'))

    def __repr__(self):
        return '<%s: value=%s offset=%s is_prev=%s>' % (
         type(self).__name__,
         self.value,
         self.offset,
         int(self.is_prev))

    def __nonzero__(self):
        return self.has_results

    @classmethod
    def from_string(cls, value):
        bits = value.split(':')
        if len(bits) != 3:
            raise ValueError
        try:
            bits = (
             float(bits[0]), int(bits[1]), int(bits[2]))
        except (TypeError, ValueError):
            raise ValueError

        return cls(*bits)


class CursorResult(Sequence):

    def __init__(self, results, next, prev, hits=None, max_hits=None):
        self.results = results
        self.next = next
        self.prev = prev
        self.hits = hits
        self.max_hits = max_hits

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return iter(self.results)

    def __getitem__(self, key):
        return self.results[key]

    def __repr__(self):
        return '<%s: results=%s>' % (type(self).__name__, len(self.results))


def _build_next_values(cursor, results, key, limit, is_desc):
    value = cursor.value
    offset = cursor.offset
    is_prev = cursor.is_prev
    num_results = len(results)
    if not value and num_results:
        value = int(key(results[0]))
    if is_prev:
        return (value, 0, True)
    if not num_results:
        return (value, offset, False)
    has_next = num_results > limit
    next_value = int(key(results[(-1)]))
    if next_value == value:
        next_offset = offset + limit
        return (
         next_value, next_offset, has_next)
    next_offset = 0
    result_iter = reversed(results)
    if has_next:
        six.next(result_iter)
    for result in result_iter:
        result_value = int(key(result))
        is_larger = result_value >= next_value
        is_smaller = result_value <= next_value
        if is_desc and is_smaller or not is_desc and is_larger:
            next_offset += 1
        else:
            break

    return (
     next_value, next_offset, has_next)


def _build_prev_values(cursor, results, key, limit, is_desc):
    value = cursor.value
    offset = cursor.offset
    is_prev = cursor.is_prev
    num_results = len(results)
    if is_prev:
        has_prev = num_results > limit
    else:
        has_prev = value or offset
    first_prev_index = 1 if is_prev and has_prev else 0
    prev_value = int(key(results[first_prev_index], for_prev=True)) if results else 0
    prev_offset = offset if is_prev else 0
    if not (is_prev and num_results):
        return (prev_value, prev_offset, has_prev)
    if prev_value == value:
        prev_offset = offset + limit
        return (
         prev_value, prev_offset, has_prev)
    prev_offset = 0
    result_iter = iter(results)
    if has_prev:
        six.next(result_iter)
    six.next(result_iter)
    for result in result_iter:
        result_value = int(key(result, for_prev=True))
        is_larger = result_value >= prev_value
        is_smaller = result_value <= prev_value
        if is_desc and is_larger or not is_desc and is_smaller:
            prev_offset += 1
        else:
            break

    return (
     prev_value, prev_offset, has_prev)


def build_cursor(results, key, limit=100, is_desc=False, cursor=None, hits=None, max_hits=None, on_results=None):
    if cursor is None:
        cursor = Cursor(0, 0, 0)
    next_value, next_offset, has_next = _build_next_values(cursor=cursor, results=results, key=key, limit=limit, is_desc=is_desc)
    prev_value, prev_offset, has_prev = _build_prev_values(cursor=cursor, results=results, key=key, limit=limit, is_desc=is_desc)
    if cursor.is_prev and has_prev:
        results = results[1:]
    elif not cursor.is_prev:
        results = results[:limit]
    next_cursor = Cursor(next_value or 0, next_offset, False, has_next)
    prev_cursor = Cursor(prev_value or 0, prev_offset, True, has_prev)
    if on_results:
        results = on_results(results)
    return CursorResult(results=results, next=next_cursor, prev=prev_cursor, hits=hits, max_hits=max_hits)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/functional.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import six
from django.utils.functional import empty

def extract_lazy_object(lo):
    """
    Unwrap a LazyObject and return the inner object. Whatever that may be.

    ProTip: This is relying on `django.utils.functional.empty`, which may
    or may not be removed in the future. It's 100% undocumented.
    """
    if not hasattr(lo, '_wrapped'):
        return lo
    if lo._wrapped is empty:
        lo._setup()
    return lo._wrapped


def apply_values(function, mapping):
    """    Applies ``function`` to a sequence containing all of the values in the
    provided mapping, returing a new mapping with the values replaced with
    the results of the provided function.

    >>> apply_values(
    ...   lambda values: map(u'{} fish'.format, values),
    ...   {1: 'red', 2: 'blue'},
    ... )
    {1: u'red fish', 2: u'blue fish'}
    """
    if not mapping:
        return {}
    keys, values = zip(*mapping.items())
    return dict(zip(keys, function(values)))


def compact(seq):
    """
    Removes ``None`` values from various sequence-based data structures.

    dict:
        Removes keys with a corresponding ``None`` value.

    list:
        Removes ``None`` valules.

    >>> compact({'foo': 'bar', 'baz': None})
    {'foo': 'bar'}

    >>> compact([1, None, 2])
    [1, 2]
    """
    if isinstance(seq, dict):
        return {k:v for k, v in six.iteritems(seq) if v is not None if v is not None}
    else:
        if isinstance(seq, list):
            return [ k for k in seq if k is not None ]
        return
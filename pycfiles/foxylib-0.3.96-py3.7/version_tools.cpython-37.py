# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/version/version_tools.py
# Compiled at: 2019-12-06 12:48:35
# Size of source mod 2**32: 3465 bytes
import warnings
from functools import wraps
from future.utils import lmap
from nose.tools import assert_greater

class VersionToolkit:

    @classmethod
    def _strip_prefix_v(cls, v):
        if not v:
            return v
        if v[0].lower() != 'v':
            return v
        return v[1:]

    @classmethod
    def version_str2int_list(cls, v):
        s = cls._strip_prefix_v(v)
        l = lmap(int, s.split('.'))
        return l

    @classmethod
    def compare(cls, v1, v2):
        l1, l2 = lmap(cls.version_str2int_list, [v1, v2])
        n = max(len(l1), len(l2))
        for i in range(n):
            if i >= len(l1):
                return -1
                if i >= len(l2):
                    return 1
                if l1[i] < l2[i]:
                    return -1
                if l1[i] > l2[i]:
                    return 1

        return 0

    @classmethod
    def version2parent(cls, v):
        l = v.split('.')
        assert_greater(len(l), 1)
        return '.'.join(l[:-1])

    class CheckBeforeRunError(Exception):
        pass

    @classmethod
    def check_before_use(cls, func=None, reason=None):

        def wrapper(f_IN):

            @wraps(f_IN)
            def wrapped(*args, **kwargs):
                raise cls.CheckBeforeRunError(reason)

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    class NotWorkingError(Exception):
        pass

    @classmethod
    def not_working(cls, func=None, reason=None):

        def wrapper(f_IN):

            @wraps(f_IN)
            def wrapped(*args, **kwargs):
                raise cls.NotWorkingError(reason)

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    class RemovedError(Exception):
        pass

    @classmethod
    def removed(cls, func=None, reason=None):

        def wrapper(f_IN):

            @wraps(f_IN)
            def wrapped(*args, **kwargs):
                raise cls.RemovedError(reason)

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    class DeprecatedError(Exception):
        pass

    @classmethod
    def deprecated(cls, func=None, version_current=None, version_tos=None, reason=None):

        def wrapper(f_IN):

            @wraps(f_IN)
            def wrapped(*args, **kwargs):
                if cls.compare(version_current, version_tos) >= 0:
                    raise cls.DeprecatedError(reason)
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(('Call to deprecated function {}.'.format(func.__name__)), category=DeprecationWarning,
                  stacklevel=2)
                warnings.simplefilter('default', DeprecationWarning)
                return func(*args, **kwargs)

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    class InactiveError(Exception):
        pass

    @classmethod
    def inactive(cls, func=None, reason=None):

        def wrapper(f):

            @wraps(f)
            def wrapped(*args, **kwargs):
                raise cls.InactiveError(reason)

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    class IncompleteError(Exception):
        pass

    @classmethod
    def incomplete(cls, func=None, reason=None):

        def wrapper(f):

            @wraps(f)
            def wrapped(*args, **kwargs):
                raise cls.IncompleteError(reason)

            return wrapped

        if func:
            return wrapper(func)
        return wrapper
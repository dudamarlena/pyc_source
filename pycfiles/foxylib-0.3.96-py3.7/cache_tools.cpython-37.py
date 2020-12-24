# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/cache/cache_tools.py
# Compiled at: 2019-12-09 00:23:12
# Size of source mod 2**32: 6000 bytes
import json, os, sys
from datetime import datetime
from functools import wraps, partial, lru_cache
import dill, six
from frozendict import frozendict
from future.utils import lfilter
from nose.tools import assert_is_not_none
from foxylib.tools.file.file_tools import FileToolkit
from foxylib.tools.log.logger_tools import FoxylibLogger

class CacheToolkit:

    @classmethod
    def func_pair_identical(cls):
        f = lambda x: x
        return (f, f)

    class JSON:

        @classmethod
        def func_pair(cls):
            return (cls.serialize, cls.deserialize)

        @classmethod
        def normalize(cls, j):
            if isinstance(j, dict):
                return frozendict({k:cls.normalize(v) for k, v in sorted(j.items())})
            if isinstance(j, (list, set)):
                return tuple([cls.normalize(x) for x in j])
            return j

        @classmethod
        def serialize(cls, v):
            return cls.serialize_natural(v)

        @classmethod
        def deserialize(cls, s):
            return cls.deserialize_natural(s)

        @classmethod
        def serialize_natural(cls, j):
            return cls.normalize(j)

        @classmethod
        def deserialize_natural(cls, s):
            return s

        @classmethod
        def serialize_dill(cls, j):
            return dill.dumps(cls.normalize(j))

        @classmethod
        def deserialize_dill(cls, s):
            return dill.loads(s)

    @classmethod
    def cache2hashable(cls, func=None, cache=None, f_pair=None):
        assert_is_not_none(cache)
        assert_is_not_none(f_pair)
        f_serialize, f_deserialize = f_pair

        def wrapper(func):

            def deserialize_and_func(*args, **kwargs):
                logger = FoxylibLogger.func2logger(deserialize_and_func)
                _args = tuple([f_deserialize(arg) for arg in args])
                _kwargs = {k:f_deserialize(v) for k, v in six.viewitems(kwargs)}
                return func(*_args, **_kwargs)

            cached_func = cache(deserialize_and_func)

            @wraps(func)
            def wrapped(*args, **kwargs):
                logger = FoxylibLogger.func2logger(wrapped)
                _args = tuple([f_serialize(arg) for arg in args])
                _kwargs = {k:f_serialize(v) for k, v in kwargs.items()}
                return cached_func(*_args, **_kwargs)

            wrapped.cache_info = cached_func.cache_info
            wrapped.cache_clear = cached_func.cache_clear
            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    @classmethod
    def cache2timed(cls, func=None, cache=None, timedelta=None):
        assert_is_not_none(cache)
        assert_is_not_none(timedelta)

        def dt_pivot2outdated(dt_pivot):
            if not dt_pivot:
                return True
            dt_now = datetime.now()
            return dt_now - dt_pivot > timedelta

        def wrapper(f):
            dt_pivot = None
            cached_func = cache(f)

            @wraps(f)
            def wrapped(*_, **__):
                nonlocal dt_pivot
                if dt_pivot2outdated(dt_pivot):
                    cached_func.cache_clear()
                    dt_pivot = datetime.now()
                v = cached_func(*_, **__)
                return v

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    @classmethod
    def f_or_file2utf8(cls, f, filepath):
        logger = FoxylibLogger.func2logger(cls.f_or_file2utf8)
        FileToolkit.dirpath2mkdirs(os.path.dirname(filepath))
        utf8 = FileToolkit.filepath2utf8(filepath)
        if utf8:
            return utf8
        utf8 = f()
        if utf8 is not None:
            FileToolkit.utf82file(utf8, filepath)
        return utf8

    @classmethod
    def f_utf82filed(cls, func=None, f_filepath=None):
        assert_is_not_none(f_filepath)

        def wrapper(f):

            @wraps(f)
            def wrapped(*_, **__):
                f_partial = partial(f, *_, **__)
                filepath = f_filepath(*_, **__)
                return cls.f_or_file2utf8(f_partial, filepath)

            return wrapped

        if func:
            return wrapper(func)
        return wrapper

    @classmethod
    def f_or_file2iter(cls, f, filepath):
        logger = FoxylibLogger.func2logger(cls.f_or_file2iter)
        f_str = lambda : '\n'.join(list(f()))
        utf8 = cls.f_or_file2utf8(f_str, filepath)
        if utf8 is None:
            return
        return utf8.splitlines()

    @classmethod
    def f_iter2filed(cls, func=None, f_filepath=None):
        assert_is_not_none(f_filepath)

        def wrapper(f):

            @wraps(f)
            def wrapped(*_, **__):
                f_partial = partial(f, *_, **__)
                filepath = f_filepath(*_, **__)
                l = cls.f_or_file2iter(f_partial, filepath)
                return l

            return wrapped

        if func:
            return wrapper(func)
        return wrapper


f_or_file2utf8 = CacheToolkit.f_or_file2utf8
f_utf82filed = CacheToolkit.f_utf82filed
f_or_file2iter = CacheToolkit.f_or_file2iter
f_iter2filed = CacheToolkit.f_iter2filed
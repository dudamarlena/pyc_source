# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/singleton.py
# Compiled at: 2019-04-10 20:40:59
# Size of source mod 2**32: 1483 bytes
import weakref

class CachedSpam(object):
    """CachedSpam"""
    settings_uuid_field = None
    _cache = None

    def __init__(self, *args, **kwargs):
        msg = "Can't instantiate directly, use {}.new(...) instead.".format(self.__class__.__name__)
        raise RuntimeError(msg)

    def __real_init__(self, *args, **kwargs):
        msg = 'You have to implement ``def __real_init__(self, ...)`` like you implement ``def __init__(self, ...)``!'
        raise NotImplementedError(msg)

    @classmethod
    def _init_cache(cls):
        if cls._cache is None:
            cls._cache = weakref.WeakValueDictionary()

    @classmethod
    def new(cls, *args, **kwargs):
        cls._init_cache()
        if cls.settings_uuid_field is None:
            msg = 'You have to specify `CachedSpam.settings_uuid_field`!'
            raise NotImplementedError(msg)
        if cls.settings_uuid_field not in kwargs:
            msg = "Can't find '{}' in {} Please use `CachedSpam.new({}=xxx)`".format(cls.settings_uuid_field, kwargs, cls.settings_uuid_field)
            raise SyntaxError(msg)
        uuid = kwargs[cls.settings_uuid_field]
        if uuid in cls._cache:
            return cls._cache[uuid]
        else:
            self = cls.__new__(cls)
            (self.__real_init__)(*args, **kwargs)
            cls._cache[uuid] = self
            return self
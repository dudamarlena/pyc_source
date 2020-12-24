# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/featureflow/persistence.py
# Compiled at: 2019-03-01 22:03:23
# Size of source mod 2**32: 1231 bytes
from .data import UuidProvider, StringDelimitedKeyBuilder, InMemoryDatabase

class PersistenceSettings(object):
    id_provider = UuidProvider()
    key_builder = StringDelimitedKeyBuilder()
    database = InMemoryDatabase(key_builder=key_builder)

    @classmethod
    def clone(cls, id_provider=None, key_builder=None, database=None):
        ip = id_provider
        kb = key_builder
        db = database

        class Settings(PersistenceSettings):
            id_provider = ip or cls.id_provider
            key_builder = kb or cls.key_builder
            database = db or cls.database

        return Settings


def simple_in_memory_settings(cls):
    """
    Decorator that returns a class that "persists" data in-memory.  Mostly
     useful for testing
    :param cls: the class whose features should be persisted in-memory
    :return: A new class that will persist features in memory
    """

    class Settings(PersistenceSettings):
        id_provider = UuidProvider()
        key_builder = StringDelimitedKeyBuilder()
        database = InMemoryDatabase(key_builder=key_builder)

    class Model(cls, Settings):
        pass

    Model.__name__ = cls.__name__
    Model.__module__ = cls.__module__
    return Model
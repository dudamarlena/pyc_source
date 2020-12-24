# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/featureflow/test_multiprocessing.py
# Compiled at: 2019-03-01 22:03:23
# Size of source mod 2**32: 1162 bytes
import unittest2
from .feature import Feature, JSONFeature
from .lmdbstore import LmdbDatabase
from .model import BaseModel
from .persistence import PersistenceSettings, UuidProvider, StringDelimitedKeyBuilder
from .test_integration import TextStream, Tokenizer, WordCount
from tempfile import mkdtemp
from multiprocessing import Pool

class Settings(PersistenceSettings):
    id_provider = UuidProvider()
    key_builder = StringDelimitedKeyBuilder()
    database = LmdbDatabase(path=(mkdtemp()),
      map_size=10000000,
      key_builder=key_builder)


class D(BaseModel, Settings):
    stream = Feature(TextStream, store=True)
    words = Feature(Tokenizer, needs=stream, store=False)
    count = JSONFeature(WordCount, needs=words, store=True)


def get_count(_):
    return len(list(D.database.iter_ids()))


class MultiProcessTests(unittest2.TestCase):

    def test_can_list_ids_from_multiple_processes(self):
        D.process(stream='Here is some text')
        D.process(stream='Here is some more')
        pool = Pool(4)
        counts = pool.map(get_count, [_ for _ in range(10)])
        self.assertSequenceEqual([2] * 10, counts)
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_adapters/test_redis.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = "\n\n  redis adapter tests\n  ~~~~~~~~~~~~~~~~~~~\n\n  tests canteen's redis adapter.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n"
from canteen import model
from canteen.model.adapter import redis as rapi
from canteen_tests.test_adapters import test_abstract
try:
    import fakeredis
except ImportError:
    fakeredis = None

if fakeredis:

    class RedisSetupTeardown(object):
        """ Packages Redis setup and teardown methods. """

        def test_adapter_mode(self):
            """ Test the adapter's internal mode against what we expect it to be """
            assert self.__abstract__ or self.subject().__testing__ is True
            assert self.subject().EngineConfig.mode == self.mode

        def test_put_entity(self):
            """ Test saving a basic entity to Redis with `RedisAdapter` """

            class SampleEntity(model.Model):
                """ quick sample entity """
                __adapter__ = rapi.RedisAdapter
                string = (
                 str, {'indexed': False})
                number = (int, {'indexed': False})

            s = SampleEntity(key=model.Key(SampleEntity, 'sample'), string='hi', number=5)
            x = s.put(adapter=self.subject())
            assert s.string == 'hi'
            assert s.number == 5
            assert x.kind == 'SampleEntity'
            assert x.id == 'sample'
            return (
             s, x, SampleEntity)

        def test_delete_entity(self):
            """ Test deleting a basic entity from Redis with `RedisAdapter` """
            s, x, SampleEntity = self.test_put_entity()
            s.delete(adapter=self.subject())
            ss = SampleEntity.get(x, adapter=self.subject())
            assert not ss, "should have deleted entity but instead got '%s'" % ss


    class RedisAdapterTopLevelBlobTests(test_abstract.DirectedGraphAdapterTests, RedisSetupTeardown):
        """ Tests `model.adapter.redis.Redis` in ``toplevel_blob`` mode """
        __abstract__ = False
        subject = rapi.RedisAdapter
        mode = rapi.RedisMode.toplevel_blob

        @classmethod
        def setUpClass(cls):
            """ Set Redis into testing mode. """
            rapi._mock_redis = fakeredis.FakeStrictRedis()
            rapi._mock_redis.flushall()
            rapi.RedisAdapter.__testing__ = True
            rapi.RedisAdapter.EngineConfig.mode = rapi.RedisMode.toplevel_blob

        @classmethod
        def tearDownClass(cls):
            """ Set Redis back into non-testing mode. """
            rapi._mock_redis = fakeredis.FakeStrictRedis()
            rapi._mock_redis.flushall()
            rapi.RedisAdapter.__testing__ = False
            rapi.RedisAdapter.EngineConfig.mode = rapi.RedisMode.toplevel_blob


    class RedisAdapterHashKindBlobTests(test_abstract.DirectedGraphAdapterTests, RedisSetupTeardown):
        """ Tests `model.adapter.redis.Redis` in ``hashkind_blob`` mode """
        __abstract__ = False
        subject = rapi.RedisAdapter
        mode = rapi.RedisMode.hashkind_blob

        @classmethod
        def setUpClass(cls):
            """ Set Redis into testing mode. """
            rapi.RedisAdapter.__testing__ = True
            rapi.RedisAdapter.EngineConfig.mode = rapi.RedisMode.hashkind_blob

        @classmethod
        def tearDownClass(cls):
            """ Set Redis back into non-testing mode. """
            rapi.RedisAdapter.__testing__ = False
            rapi.RedisAdapter.EngineConfig.mode = rapi.RedisMode.toplevel_blob


    class RedisAdapterHashKeyBlobTests(test_abstract.DirectedGraphAdapterTests, RedisSetupTeardown):
        """ Tests `model.adapter.redis.Redis` in ``hashkey_blob`` mode """
        __abstract__ = False
        subject = rapi.RedisAdapter
        mode = rapi.RedisMode.hashkey_blob

        @classmethod
        def setUpClass(cls):
            """ Set Redis into testing mode. """
            rapi.RedisAdapter.__testing__ = True
            rapi.RedisAdapter.EngineConfig.mode = rapi.RedisMode.hashkey_blob

        @classmethod
        def tearDownClass(cls):
            """ Set Redis back into non-testing mode. """
            rapi.RedisAdapter.__testing__ = False
            rapi.RedisAdapter.EngineConfig.mode = rapi.RedisMode.toplevel_blob


else:
    print 'Warning! Redis not found, skipping Redis testsuite.'
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/shardmonster/tests/test_sharder.py
# Compiled at: 2016-06-16 06:14:05
from mock import Mock
from shardmonster import api, sharder
from shardmonster.tests.base import ShardingTestCase

class TestSharder(ShardingTestCase):

    def setUp(self):
        api.activate_caching(0.5)
        super(TestSharder, self).setUp()

    def tearDown(self):
        api.activate_caching(0)
        super(TestSharder, self).tearDown()

    def test_basic_copy(self):
        api.set_shard_at_rest('dummy', 1, 'dest1/test_sharding')
        doc1 = {'x': 1, 'y': 1}
        doc1['_id'] = self.db1.dummy.insert(doc1)
        api.start_migration('dummy', 1, 'dest2/test_sharding')
        manager = Mock(insert_throttle=None)
        sharder._do_copy('dummy', 1, manager)
        doc2, = self.db2.dummy.find({})
        self.assertEquals(doc1, doc2)
        return

    def test_sync_after_copy(self):
        api.set_shard_at_rest('dummy', 1, 'dest1/test_sharding')
        api.start_migration('dummy', 1, 'dest2/test_sharding')
        doc1 = {'x': 1, 'y': 1}
        doc1['_id'] = self.db1.dummy.insert(doc1)
        self.db2.dummy.insert(doc1)
        initial_oplog_pos = sharder._get_oplog_pos('dummy', 1)
        self.db1.dummy.update({'x': 1}, {'$inc': {'y': 1}})
        api.set_shard_to_migration_status('dummy', 1, api.ShardStatus.MIGRATING_SYNC)
        sharder._sync_from_oplog('dummy', 1, initial_oplog_pos)
        doc2, = self.db2.dummy.find({})
        self.assertEquals(2, doc2['y'])

    def test_delete_after_migration(self):
        api.set_shard_at_rest('dummy', 1, 'dest1/test_sharding')
        api.start_migration('dummy', 1, 'dest2/test_sharding')
        doc1 = {'x': 1, 'y': 1}
        doc1['_id'] = self.db1.dummy.insert(doc1)
        self.db2.dummy.insert(doc1)
        api.set_shard_to_migration_status('dummy', 1, api.ShardStatus.POST_MIGRATION_DELETE)
        manager = Mock(delete_throttle=None)
        sharder._delete_source_data('dummy', 1, manager)
        self.assertEquals(0, self.db1.dummy.find({}).count())
        doc1_actual, = self.db2.dummy.find({})
        self.assertEquals(doc1, doc1_actual)
        return

    def test_sync_ignores_other_collection(self):
        api.set_shard_at_rest('dummy', 1, 'dest1/test_sharding')
        api.start_migration('dummy', 1, 'dest2/test_sharding')
        doc1 = {'x': 1, 'y': 1}
        doc1['_id'] = self.db1.dummy.insert(doc1)
        self.db2.dummy.insert(doc1)
        initial_oplog_pos = sharder._get_oplog_pos('dummy', 1)
        self.db1.other_coll.insert(doc1)
        self.db1.other_coll.update({'x': 1}, {'$inc': {'y': 1}})
        api.set_shard_to_migration_status('dummy', 1, api.ShardStatus.MIGRATING_SYNC)
        sharder._sync_from_oplog('dummy', 1, initial_oplog_pos)
        doc2, = self.db2.dummy.find({})
        self.assertEquals(1, doc2['y'])

    def test_sync_uses_correct_connection(self):
        """This tests for a bug found during a rollout. The connection for the
        metadata was assumed to be the same connection as the source data was
        going to be coming from. This is *not* always the case.
        """
        api.set_shard_at_rest('dummy', 1, 'dest2/test_sharding')
        api.start_migration('dummy', 1, 'dest1/test_sharding')
        doc1 = {'x': 1, 'y': 1}
        doc1['_id'] = self.db1.dummy.insert(doc1)
        self.db2.dummy.insert(doc1)
        initial_oplog_pos = sharder._get_oplog_pos('dummy', 1)
        self.db2.dummy.update({'x': 1}, {'$inc': {'y': 1}})
        api.set_shard_to_migration_status('dummy', 1, api.ShardStatus.MIGRATING_SYNC)
        sharder._sync_from_oplog('dummy', 1, initial_oplog_pos)
        doc2, = self.db1.dummy.find({})
        self.assertEquals(2, doc2['y'])
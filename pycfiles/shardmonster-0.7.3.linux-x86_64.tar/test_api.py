# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/shardmonster/tests/test_api.py
# Compiled at: 2016-08-05 04:34:07
from shardmonster.api import ensure_realm_exists, set_shard_at_rest, start_migration, where_is
from shardmonster.metadata import _get_realm_for_collection, _get_realm_coll
from shardmonster.tests.base import ShardingTestCase

class TestRealm(ShardingTestCase):

    def test_ensure_realm_exists(self):
        with self.assertRaises(Exception) as (catcher):
            realm = _get_realm_for_collection('some_collection')
        self.assertEquals(catcher.exception.message, 'Realm for collection some_collection does not exist')
        ensure_realm_exists('some_realm', 'some_field', 'some_collection')
        realm = _get_realm_for_collection('some_collection')
        self.assertEquals('some_realm', realm['name'])
        ensure_realm_exists('some_realm', 'some_field', 'some_collection')
        realm = _get_realm_for_collection('some_collection')
        self.assertEquals('some_realm', realm['name'])
        coll = _get_realm_coll()
        self.assertEquals(2, coll.count())

    def test_ensure_changing_realm_breaks(self):
        ensure_realm_exists('some_realm', 'some_field', 'some_collection')
        with self.assertRaises(Exception) as (catcher):
            ensure_realm_exists('some_realm', 'some_other_field', 'some_collection')
        self.assertEquals(catcher.exception.message, 'Cannot change realm')

    def test_one_realm_per_collection(self):
        ensure_realm_exists('some_realm', 'some_field', 'some_collection')
        with self.assertRaises(Exception) as (catcher):
            ensure_realm_exists('some_other_realm', 'some_other_field', 'some_collection')
        self.assertEquals(catcher.exception.message, 'Realm for collection some_collection already exists')

    def test_cannot_move_to_same_location(self):
        ensure_realm_exists('some_realm', 'some_field', 'some_collection')
        set_shard_at_rest('some_realm', 1, 'dest1/db')
        with self.assertRaises(Exception) as (catcher):
            start_migration('some_realm', 1, 'dest1/db')
        self.assertEquals(catcher.exception.message, 'Shard is already at dest1/db')

    def test_set_shard_at_rest_bad_location(self):
        ensure_realm_exists('some_realm', 'some_field', 'some_collection')
        with self.assertRaises(Exception) as (catcher):
            set_shard_at_rest('some_realm', 1, 'bad-cluster/db')
        self.assertEquals(catcher.exception.message, 'Cluster bad-cluster has not been configured')

    def test_set_shard_at_rest_when_already_at_rest(self):
        ensure_realm_exists('some_realm', 'some_field', 'some_collection')
        set_shard_at_rest('some_realm', 1, 'dest1/db')
        with self.assertRaises(Exception) as (catcher):
            set_shard_at_rest('some_realm', 1, 'dest2/db')
        self.assertEquals(catcher.exception.message, 'Shard with key 1 has already been placed. Use force=true if you really want to do this')
        set_shard_at_rest('some_realm', 1, 'dest2/db', force=True)

    def test_where_is(self):
        ensure_realm_exists('some_realm', 'some_field', 'some_collection')
        set_shard_at_rest('some_realm', 1, 'dest2/db')
        self.assertEquals('dest2/db', where_is('some_collection', 1))
        with self.assertRaises(Exception) as (catcher):
            self.assertEquals('dest1/db', where_is('some_collection', 2))
        self.assertEquals(catcher.exception.message, 'Shard key 2 not placed for some_realm')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/shardmonster/tests/test_connection.py
# Compiled at: 2016-06-16 06:14:04
from shardmonster.connection import get_cluster_uri, _get_cluster_coll, ensure_cluster_exists
from shardmonster.tests.base import ShardingTestCase

class TestCluster(ShardingTestCase):

    def test_ensure_cluster_exists(self):
        with self.assertRaises(Exception) as (catcher):
            uri = get_cluster_uri('best-cluster')
        self.assertEquals(catcher.exception.message, 'Cluster best-cluster has not been configured')
        ensure_cluster_exists('best-cluster', 'mongodb://localhost:27017')
        uri = get_cluster_uri('best-cluster')
        self.assertEquals('mongodb://localhost:27017', uri)
        ensure_cluster_exists('best-cluster', 'mongodb://localhost:27017')
        uri = get_cluster_uri('best-cluster')
        self.assertEquals('mongodb://localhost:27017', uri)
        coll = _get_cluster_coll()
        self.assertEquals(3, coll.count())
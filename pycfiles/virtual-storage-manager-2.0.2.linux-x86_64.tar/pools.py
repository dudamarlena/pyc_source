# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/pools.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging, time
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'pools'

    def basic(self, pool):
        return {'pool': {'id': pool['id'], 
                    'poolId': pool['pool_id'], 
                    'name': pool['name'], 
                    'status': pool['status'], 
                    'recipeId': pool['recipe_id'], 
                    'tag': pool['tag']}}

    def show(self, pool):
        pool_dict = {'pool': {'id': pool['id'], 
                    'poolId': pool['pool_id'], 
                    'pool_id': pool['pool_id'], 
                    'name': pool['name'], 
                    'storageGroup': self._get_storage_group(pool), 
                    'replica_storage_group': pool.get('replica_storage_group'), 
                    'ruleset': pool.get('ruleset'), 
                    'status': pool.get('status'), 
                    'recipeId': pool.get('recipe_id'), 
                    'pgNum': pool.get('pg_num'), 
                    'pgpNum': pool.get('pgp_num'), 
                    'size': pool.get('size'), 
                    'minSize': pool.get('min_size'), 
                    'crushRuleset': pool.get('crush_ruleset'), 
                    'crashRelayInterval': pool.get('crash_replay_interval'), 
                    'createdDate': pool.get('created_at'), 
                    'clusterId': pool.get('cluster_id'), 
                    'createdBy': pool.get('created_by'), 
                    'tag': pool.get('tag'), 
                    'num_bytes': pool.get('num_bytes'), 
                    'num_objects': pool.get('num_objects'), 
                    'num_object_clones': pool.get('num_object_clones'), 
                    'num_objects_degraded': pool.get('num_objects_degraded'), 
                    'num_objects_unfound': pool.get('num_objects_unfound'), 
                    'read_bytes_sec': pool.get('read_bytes_sec'), 
                    'write_bytes_sec': pool.get('write_bytes_sec'), 
                    'op_per_sec': pool.get('op_per_sec'), 
                    'num_read': pool.get('num_read'), 
                    'num_read_kb': pool.get('num_read_kb'), 
                    'num_write': pool.get('num_write'), 
                    'num_write_kb': pool.get('num_write_kb'), 
                    'erasure_code_status': pool.get('ec_status') if pool.get('ec_status') != 'default' else None, 
                    'cache_tier_status': pool.get('cache_tier_status'), 
                    'quota': pool.get('quota')}}
        try:
            pool_dict['pool']['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(pool['updated_at'], '%Y-%m-%dT%H:%M:%S.000000'))
        except:
            pool_dict['pool']['updated_at'] = ''

        return pool_dict

    def index(self, pools):
        return self._list_view(self.basic, pools)

    def detail(self, pools):
        return self._list_view(self.show, pools)

    def _list_view(self, func, pools):
        pool_list = [ func(pool)['pool'] for pool in pools ]
        pool_dict = dict(pool=pool_list)
        return pool_dict

    def _get_storage_group(self, pool):
        storage_group = pool.get('storage_group')
        if storage_group:
            return storage_group.get('name')
        else:
            return
            return
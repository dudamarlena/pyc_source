# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_table.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 5040 bytes
import logging
from pgobserver_gatherer.gatherer_base import GathererBase
from pgobserver_gatherer.id_cache import IdCache
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

class TableStatsGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.TABLE)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.TABLE][0]] * 60
        self.columns_to_store = ['tsd_timestamp', 'tsd_host_id', 'tsd_table_id', 'tsd_table_size', 'tsd_index_size',
         'tsd_seq_scans', 'tsd_index_scans', 'tsd_tup_ins', 'tsd_tup_upd', 'tsd_tup_del',
         'tsd_tup_hot_upd']
        self.datastore_table_name = 'monitor_data.table_size_data'
        self.use_approximation = settings.get('useTableSizeApproximation') == 1
        self.cache_table_name = 'monitor_data.tables'
        self.cache_id_column = 't_id'
        self.cache_host_id_column = 't_host_id'
        self.cache_key_columns = ['t_schema', 't_name']
        self.table_id_cache = IdCache(self.cache_table_name, self.cache_id_column, self.cache_key_columns, self.cache_host_id_column, self.host_id)

    def gather_data(self):
        data = []
        sql_get = "\n            SELECT\n              now() as tsd_timestamp,\n              {host_id} as tsd_host_id,\n              schemaname as t_schema,\n              relname as t_name,\n              pg_table_size(relid) as tsd_table_size,\n              pg_indexes_size(relid) as tsd_index_size,\n              seq_scan as tsd_seq_scans,\n              idx_scan as tsd_index_scans,\n              n_tup_ins as tsd_tup_ins,\n              n_tup_upd as tsd_tup_upd,\n              n_tup_hot_upd as tsd_tup_hot_upd,\n              n_tup_del as tsd_tup_del\n            FROM\n              pg_stat_user_tables\n            WHERE\n              NOT schemaname LIKE ANY (array[E'tmp%', E'temp%', E'%api\\_r%'])\n              --AND relname = 't1'\n            ".format(host_id=self.host_id)
        if self.use_approximation:
            sql_get = "\n                SELECT\n                  now() as tsd_timestamp,\n                  {host_id} as tsd_host_id,\n                  schemaname as t_schema,\n                  ut.relname as t_name,\n                  (c.relpages + coalesce(ctd.relpages,0) + cti.relpages)::int8 * 8192 as tsd_table_size,\n                  (select sum(relpages) from pg_class ci join pg_index on indexrelid =  ci.oid where indrelid = c.oid)::int8 * 8192 as tsd_index_size,\n                  seq_scan as tsd_seq_scans\n                  # idx_scan as tsd_index_scans,\n                  # n_tup_ins as tsd_tup_ins,\n                  # n_tup_upd as tsd_tup_upd,\n                  # n_tup_hot_upd as tsd_tup_hot_upd,\n                  # n_tup_del as tsd_tup_del\n                FROM\n                  pg_stat_user_tables ut\n                  JOIN\n                  pg_class c ON c.oid = ut.relid\n                  LEFT JOIN\n                  pg_class ctd ON ctd.oid = c.reltoastrelid\n                  LEFT JOIN\n                  pg_class cti ON cti.oid = ctd.reltoastidxid\n                WHERE\n                  not ut.schemaname like any (array[E'tmp%', E'temp%', E'%api\\_r%'])\n                ".format(host_id=self.host_id)
        try:
            data = datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get)
        except Exception as e:
            if 'reltoastidxid does not exist' in str(e):
                logging.error('[%s][%s] - useTableSizeApproximation not available for >9.4', self.host_name, self.gatherer_name)
                return []
            raise e

        return data

    def store_data(self, data):
        logging.info('[%s][%s] running custom store_data() for %s rows', self.host_name, self.gatherer_name, len(data))
        if len(self.table_id_cache.cache) == 0:
            self.table_id_cache.refresh_from_db()
        new_tables = [x for x in data if not self.table_id_cache.has((x['t_schema'], x['t_name']))]
        logging.debug('[%s][%s] %s new tables found', self.host_name, self.gatherer_name, len(new_tables))
        if new_tables:
            for x in new_tables:
                self.table_id_cache.put((x['t_schema'], x['t_name']))

        for d in data:
            d['tsd_table_id'] = self.table_id_cache.get((d['t_schema'], d['t_name']))

        super().store_data(data)
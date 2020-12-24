# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_table_io.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 2847 bytes
import logging
from pgobserver_gatherer.gatherer_base import GathererBase
from pgobserver_gatherer.id_cache import IdCache
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

class TableIOStatsGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.TABLEIO)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.TABLEIO][0]] * 60
        self.columns_to_store = ['tio_timestamp', 'tio_host_id', 'tio_table_id', 'tio_heap_read', 'tio_heap_hit',
         'tio_idx_read', 'tio_idx_hit']
        self.datastore_table_name = 'monitor_data.table_io_data'
        self.cache_table_name = 'monitor_data.tables'
        self.cache_id_column = 't_id'
        self.cache_host_id_column = 't_host_id'
        self.cache_key_columns = ['t_schema', 't_name']
        self.table_id_cache = IdCache(self.cache_table_name, self.cache_id_column, self.cache_key_columns, self.cache_host_id_column, self.host_id)

    def gather_data(self):
        sql_get = "\n            SELECT\n              now() as tio_timestamp,\n              {host_id} as tio_host_id,\n              schemaname as t_schema,\n              relname as t_name,\n              heap_blks_read as tio_heap_read,\n              heap_blks_hit as tio_heap_hit,\n              idx_blks_read as tio_idx_read,\n              idx_blks_hit as tio_idx_hit\n            FROM\n              pg_statio_user_tables\n            WHERE\n              NOT schemaname LIKE ANY (array[E'tmp%', E'temp%', E'%api\\_r%'])\n              AND (heap_blks_read > 0 or heap_blks_hit > 0 or idx_blks_read > 0 or idx_blks_hit > 0)\n            ".format(host_id=self.host_id)
        return datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get)

    def store_data(self, data):
        logging.info('[%s][%s] running custom store_data() for %s rows', self.host_name, self.gatherer_name, len(data))
        if len(self.table_id_cache.cache) == 0:
            self.table_id_cache.refresh_from_db()
        new_tables = [x for x in data if not self.table_id_cache.has((x['t_schema'], x['t_name']))]
        logging.debug('[%s][%s] %s new tables found', self.host_name, self.gatherer_name, len(new_tables))
        for x in new_tables:
            self.table_id_cache.put((x['t_schema'], x['t_name']))

        for d in data:
            d['tio_table_id'] = self.table_id_cache.get((d['t_schema'], d['t_name']))

        super().store_data(data)
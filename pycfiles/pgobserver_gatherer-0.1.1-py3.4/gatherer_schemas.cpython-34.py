# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_schemas.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 3342 bytes
from pgobserver_gatherer.gatherer_base import GathererBase
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

class SchemaStatsGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.SCHEMAS)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.SCHEMAS][0]] * 60
        self.columns_to_store = ['sud_timestamp', 'sud_host_id', 'sud_schema_name', 'sud_sproc_calls', 'sud_seq_scans',
         'sud_idx_scans', 'sud_tup_ins', 'sud_tup_upd', 'sud_tup_del']
        self.datastore_table_name = 'monitor_data.schema_usage_data'

    def gather_data(self):
        sql_get = "\n            with q_sproc_calls as (\n\n                  select\n                        nspname as schemaname,\n                        coalesce(sum(calls),0) as sproc_calls\n                  from\n                        pg_namespace n\n                        left join\n                        pg_stat_user_functions f on f.schemaname = n.nspname\n                  where\n                        not nspname like any (array['pg_toast%', 'pg_temp%' ,'pgq%', '%utils%'])\n                        and nspname not in ('pg_catalog', 'information_schema', '_v', 'zz_utils', 'zz_commons')\n                  group by\n                        nspname\n            ),\n            q_table_stats as (\n                  select\n                        nspname as schemaname,\n                        sum(seq_scan) as seq_scan,\n                        sum(idx_scan) as idx_scan,\n                        sum(n_tup_ins) as n_tup_ins,\n                        sum(n_tup_upd) as n_tup_upd,\n                        sum(n_tup_del) as n_tup_del\n                  from\n                        pg_namespace n\n                        left join\n                        pg_stat_all_tables t on t.schemaname = n.nspname\n                  where\n                        not nspname like any (array['pg_toast%', 'pg_temp%' ,'pgq%'])\n                        and nspname not in ('pg_catalog', 'information_schema', '_v', 'zz_utils', 'zz_commons')\n                  group by\n                        nspname\n            )\n            select\n                  now() as sud_timestamp,\n                  {host_id} as sud_host_id,\n                  coalesce(t.schemaname,p.schemaname) as sud_schema_name,\n                  coalesce(p.sproc_calls,0) as sud_sproc_calls,\n                  coalesce(t.seq_scan,0) as sud_seq_scans,\n                  coalesce(t.idx_scan,0) as sud_idx_scans,\n                  coalesce(t.n_tup_ins,0) as sud_tup_ins,\n                  coalesce(t.n_tup_upd,0) as sud_tup_upd,\n                  coalesce(t.n_tup_del,0) as sud_tup_del\n            from\n                  q_table_stats t\n                  full outer join\n                  q_sproc_calls p on p.schemaname = t.schemaname\n            order by\n                  2;\n            ".format(host_id=self.host_id)
        data = datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get)
        return data
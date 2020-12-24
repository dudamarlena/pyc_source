# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_kpi.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 3910 bytes
from pgobserver_gatherer.gatherer_base import GathererBase
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

class KPIGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.KPI)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.KPI][0]] * 60
        self.columns_to_store = ['kpi_timestamp', 'kpi_host_id', 'kpi_load_1min', 'kpi_active_backends',
         'kpi_blocked_backends', 'kpi_oldest_tx_s', 'kpi_tps', 'kpi_rollbacks', 'kpi_blks_read',
         'kpi_blks_hit', 'kpi_temp_bytes', 'kpi_wal_location_b', 'kpi_seq_scans', 'kpi_ins',
         'kpi_upd', 'kpi_del', 'kpi_sproc_calls', 'kpi_blk_read_time', 'kpi_blk_write_time',
         'kpi_deadlocks']
        self.datastore_table_name = 'monitor_data.kpi_data'

    def gather_data(self):
        sql_get = "\n            WITH q_stat_tables AS (\n              SELECT * FROM pg_stat_all_tables\n              WHERE NOT schemaname LIKE any(array[E'pg\\_%'])\n            ),\n            q_iud_sums_persistent AS (\n              SELECT\n                sum(n_tup_ins) AS ins,\n                sum(n_tup_upd) AS upd,\n                sum(n_tup_del) AS del\n              FROM\n                q_stat_tables t\n                JOIN\n                pg_class c on c.oid = t.relid\n                WHERE c.relpersistence = 'p'\n            )\n            SELECT\n              {host_id} AS kpi_host_id,\n              now() AS kpi_timestamp,\n              {load_1min} AS kpi_load_1min,\n              numbackends AS kpi_numbackends,\n              (select count(1) from pg_stat_activity where datid = d.datid and state = 'active' and pid != pg_backend_pid()) AS kpi_active_backends,\n              (select count(1) from pg_stat_activity where datid = d.datid and waiting) AS kpi_blocked_backends,\n              (select round(extract(epoch from now()) - extract(epoch from (select xact_start from pg_stat_activity\n                where datid = d.datid order by xact_start limit 1))))::int AS kpi_oldest_tx_s,  -- should filter out autovacuum?\n              xact_commit + xact_rollback AS kpi_tps,\n              xact_rollback AS kpi_rollbacks,\n              blks_read AS kpi_blks_read,\n              blks_hit AS kpi_blks_hit,\n              temp_bytes AS kpi_temp_bytes,\n              (select pg_xlog_location_diff(pg_current_xlog_location(), '0/0')) AS kpi_wal_location_b,\n              (select sum(seq_scan) from q_stat_tables) AS kpi_seq_scans,\n              ins AS kpi_ins,\n              upd AS kpi_upd,\n              del AS kpi_del,\n              (select sum(calls) from pg_stat_user_functions where not schemaname like any(array[E'pg\\_%', 'information_schema'])) AS kpi_sproc_calls,\n              blk_read_time AS kpi_blk_read_time,\n              blk_write_time AS kpi_blk_write_time,\n              deadlocks AS kpi_deadlocks\n              --pg_database_size(d.datname) AS db_size_b\n            FROM\n              pg_stat_database d\n              JOIN\n              q_iud_sums_persistent on true\n            WHERE\n              datname = current_database()\n            "
        return datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get.format(host_id=self.host_id, load_1min='(select load_1min from zz_utils.get_load_average())' if self.have_zz_utils else 'null'))
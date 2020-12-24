# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_connection.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 2147 bytes
from pgobserver_gatherer.gatherer_base import GathererBase
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

class ConnectionStatsGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.CONNS)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.CONNS][0]] * 60
        self.columns_to_store = ['scd_timestamp', 'scd_host_id', 'scd_total', 'scd_active',
         'scd_waiting', 'scd_longest_session_seconds', 'scd_longest_tx_seconds',
         'scd_longest_query_seconds']
        self.datastore_table_name = 'monitor_data.stat_connection_data'

    def gather_data(self):
        sql_get = "\n        with sa_snapshot as (\n          select * from pg_stat_activity where pid != pg_backend_pid() and not query like 'autovacuum:%'\n        )\n        select\n          now() as scd_timestamp,\n          {host_id} as scd_host_id,\n          (select count(*) from sa_snapshot) as scd_total,\n          (select count(*) from sa_snapshot where state = 'active') as scd_active,\n          (select count(*) from sa_snapshot where waiting) as scd_waiting,\n          (select extract(epoch from (now() - backend_start))::int\n            from sa_snapshot order by backend_start limit 1) as scd_longest_session_seconds,\n          (select extract(epoch from (now() - xact_start))::int\n            from sa_snapshot where xact_start is not null order by xact_start limit 1) as scd_longest_tx_seconds,\n          (select extract(epoch from max(now() - query_start))::int\n            from sa_snapshot where state = 'active') as scd_longest_query_seconds\n        ".format(host_id=self.host_id)
        data = datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get)
        return data
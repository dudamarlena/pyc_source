# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_locks.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 5967 bytes
import re
from pgobserver_gatherer.gatherer_base import GathererBase
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS
QUERY_CLEANUP_REGEX = re.compile('\\s+')

class BlockingLocksGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.LOCKS)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.LOCKS][0]] * 60
        self.columns_to_store_processes = [
         'bp_host_id', 'bp_timestamp', 'datid', 'datname', 'pid',
         'usesysid', 'usename', 'application_name', 'client_addr', 'client_hostname',
         'client_port', 'backend_start', 'xact_start', 'query_start', 'state_change',
         'waiting', 'state', 'query']
        self.datastore_table_name_processes = 'monitor_data.blocking_processes'

    def gather_data(self):
        latest_timestamps = self.get_latest_timestamps()
        data_locks = self.gather_data_locks(latest_timestamps['locks'])
        data_processes = self.gather_data_processes(latest_timestamps['processes'])
        if data_locks or data_processes:
            return [(data_locks, data_processes)]
        else:
            return []

    def store_data(self, data):
        data_locks, data_processes = data[0]
        if data_locks or data_processes:
            if data_locks:
                super().store_data(data_locks, self.columns_to_store_locks, self.datastore_table_name_locks)
            if data_processes:
                super().store_data(data_processes, self.columns_to_store_processes, self.datastore_table_name_processes)

    def get_latest_timestamps(self):
        sql = "\n            select coalesce((select bp_timestamp from monitor_data.blocking_processes\n                                where bp_host_id = %s order by bp_timestamp desc limit 1),\n                             now() - '1 days'::interval) as tz\n            union all\n            select coalesce((select bl_timestamp from monitor_data.blocking_locks\n                                where bl_host_id = %s order by bl_timestamp desc limit 1),\n                            now() - '1 days'::interval) as tz\n        "
        data = datadb.execute(sql, (self.host_id, self.host_id))
        return {'processes': data[0]['tz'],  'locks': data[1]['tz']}

    def gather_data_locks(self, timestamp_from):
        return []

    def gather_data_processes(self, timestamp_from):
        sql_get_processes = '\n            select\n              %s as bp_host_id,\n              bp_timestamp,\n              datid::int,\n              datname,\n              pid,\n              usesysid::int,\n              usename::text,\n              application_name,\n              client_addr,\n              client_hostname,\n              client_port,\n              backend_start::text,\n              xact_start::text,\n              query_start::text,\n              state_change::text,\n              waiting,\n              state,\n              query\n            from\n              z_blocking.blocking_processes\n            where\n              bp_timestamp > %s\n            order by\n              bp_timestamp\n        '
        data = datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get_processes, (self.host_id, timestamp_from))
        for d in data:
            d['query'] = QUERY_CLEANUP_REGEX.sub(' ', d['query'])

        return data
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_database.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 2855 bytes
from pgobserver_gatherer.gatherer_base import GathererBase
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

class DatabaseGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.DB)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.DB][0]] * 60
        self.columns_to_store = ['sdd_host_id', 'sdd_timestamp', 'sdd_numbackends', 'sdd_xact_commit', 'sdd_xact_rollback',
         'sdd_blks_read', 'sdd_blks_hit', 'sdd_temp_files', 'sdd_temp_bytes', 'sdd_deadlocks',
         'sdd_blk_read_time', 'sdd_blk_write_time']
        self.datastore_table_name = 'monitor_data.stat_database_data'

    def gather_data(self):
        sql_91 = 'select\n                      %s as sdd_host_id,\n                      now() as sdd_timestamp,\n                      numbackends as sdd_numbackends,\n                      xact_commit as sdd_xact_commit,\n                      xact_rollback as sdd_xact_rollback,\n                      blks_read as sdd_blks_read,\n                      blks_hit as sdd_blks_hit,\n                      null as sdd_temp_files,\n                      null as sdd_temp_bytes,\n                      deadlocks as sdd_deadlocks,\n                      blk_read_time::int8 as sdd_blk_read_time,\n                      blk_write_time::int8 as sdd_blk_write_time\n                    from\n                      pg_stat_database\n                    where\n                      datname = current_database()\n                        '
        sql_92 = 'select\n                      %s as sdd_host_id,\n                      now() as sdd_timestamp,\n                      numbackends as sdd_numbackends,\n                      xact_commit as sdd_xact_commit,\n                      xact_rollback as sdd_xact_rollback,\n                      blks_read as sdd_blks_read,\n                      blks_hit as sdd_blks_hit,\n                      temp_files as sdd_temp_files,\n                      temp_bytes as sdd_temp_bytes,\n                      deadlocks as sdd_deadlocks,\n                      blk_read_time::int8 as sdd_blk_read_time,\n                      blk_write_time::int8 as sdd_blk_write_time\n                    from\n                      pg_stat_database\n                    where\n                      datname = current_database()\n                        '
        return datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_91 if self.pg_server_version_num < 90200 else sql_92, (self.host_id,))
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_bgwriter.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 2222 bytes
from pgobserver_gatherer.gatherer_base import GathererBase
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

class BgwriterGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.BGWRITER)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.BGWRITER][0]] * 60
        self.columns_to_store = ['sbd_timestamp', 'sbd_host_id', 'sbd_checkpoints_timed', 'sbd_checkpoints_req',
         'sbd_checkpoint_write_time', 'sbd_checkpoint_sync_time', 'sbd_buffers_checkpoint',
         'sbd_buffers_clean', 'sbd_maxwritten_clean', 'sbd_buffers_backend',
         'sbd_buffers_backend_fsync', 'sbd_buffers_alloc', 'sbd_stats_reset']
        self.datastore_table_name = 'monitor_data.stat_bgwriter_data'

    def gather_data(self):
        sql_get = 'SELECT\n                       now() as sbd_timestamp,\n                       %s as sbd_host_id,\n                       checkpoints_timed as sbd_checkpoints_timed,\n                       checkpoints_req as sbd_checkpoints_req,\n                       checkpoint_write_time as sbd_checkpoint_write_time,\n                       checkpoint_sync_time as sbd_checkpoint_sync_time,\n                       buffers_checkpoint as sbd_buffers_checkpoint,\n                       buffers_clean as sbd_buffers_clean,\n                       maxwritten_clean as sbd_maxwritten_clean,\n                       buffers_backend as sbd_buffers_backend,\n                       buffers_backend_fsync as sbd_buffers_backend_fsync,\n                       buffers_alloc as sbd_buffers_alloc,\n                       stats_reset as sbd_stats_reset\n                     from\n                       pg_stat_bgwriter\n                        '
        data = datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get, (self.host_id,))
        return data
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp/runner/models.py
# Compiled at: 2019-11-08 04:26:21
from __future__ import unicode_literals
from kipp.utils import utcnow, get_logger
RUNSTATSMONITOR_COLLECTION_NAME = b'run_stats_monitor'

class RunStats:
    running = b'running'
    failed = b'failed'
    successed = b'successed'


class RunStatsMonitor(object):

    def __init__(self, command, args=None):
        self.connect()
        self._command = command
        self._args = args

    def connect(self):
        from Utilities.movoto.mongodbHelper import MongodbHelper
        self.mongo = MongodbHelper().connect()
        self.db = self.mongo.db
        self.collection = self.db[RUNSTATSMONITOR_COLLECTION_NAME]

    def start(self):
        d = {b'command': self._command, 
           b'updated_at': utcnow(), 
           b'created_at': utcnow(), 
           b'status': RunStats.running}
        if self._args:
            d.update({b'arguments': self._args})
        r = self.mongo.create_documents(RUNSTATSMONITOR_COLLECTION_NAME, [d])
        self.task_id = r[0]
        return self.task_id

    def success(self):
        self.mongo.update_fields(RUNSTATSMONITOR_COLLECTION_NAME, {b'_id': self.task_id}, {b'updated_at': utcnow(), b'status': RunStats.successed})

    def clean_logs_by_timedelta(self, timedelta):
        get_logger().info(b'clean_logs_by_timedelta for timedelta %s', timedelta)
        self.collection.remove({b'updated_at': {b'$lt': utcnow() + timedelta}})

    def fail(self, err_msg):
        self.mongo.update_fields(RUNSTATSMONITOR_COLLECTION_NAME, {b'_id': self.task_id}, {b'updated_at': utcnow(), b'status': RunStats.failed, b'err_msg': err_msg})

    def __del__(self):
        self.mongo.close()
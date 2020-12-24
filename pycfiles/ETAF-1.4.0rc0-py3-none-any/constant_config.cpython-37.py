# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/entity/constant_config.py
# Compiled at: 2020-05-06 02:27:06
# Size of source mod 2**32: 1538 bytes
from enum import IntEnum

class WorkMode(IntEnum):
    STANDALONE = 0
    CLUSTER = 1


class Backend(IntEnum):
    EGGROLL = 0
    SPARK = 1

    def is_eggroll(self):
        return self.value == self.EGGROLL

    def is_spark(self):
        return self.value == self.SPARK


class JobStatus(object):
    WAITING = 'waiting'
    RUNNING = 'running'
    COMPLETE = 'success'
    FAILED = 'failed'
    TIMEOUT = 'timeout'
    CANCELED = 'canceled'
    PARTIAL = 'partial'
    DELETED = 'deleted'


class TaskStatus(object):
    START = 'start'
    RUNNING = 'running'
    COMPLETE = 'success'
    FAILED = 'failed'
    TIMEOUT = 'timeout'


class ModelStorage(object):
    REDIS = 'redis'


class ModelOperation(object):
    EXPORT = 'export'
    IMPORT = 'import'
    STORE = 'store'
    RESTORE = 'restore'
    LOAD = 'load'
    BIND = 'bind'


class ProcessRole(object):
    SERVER = 'server'
    EXECUTOR = 'executor'
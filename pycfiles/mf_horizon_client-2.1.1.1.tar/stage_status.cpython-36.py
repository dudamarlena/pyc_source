# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stanley/PycharmProjects/horizon-python-client/src/mf_horizon_client/data_structures/configs/stage_status.py
# Compiled at: 2020-03-26 22:31:55
# Size of source mod 2**32: 751 bytes
import enum

class StageStatus(enum.Enum):
    __doc__ = '\n    Defines the current state of a stage, controlling whether it can be run etc.\n    Ready -     stage is available to be run as part of a pipeline.\n    Running -   stage is currently running\n    Complete -  stage has finished running and results have been saved\n    Pending -   stage is part of a pipeline which is currently running, and will be run\n                when prerequisite stages are completed. Status will then be set to\n                complete\n    Error -     An error was found when running the stage. Results may be incomplete or\n                nonexistent.\n    '
    READY = 'READY'
    RUNNING = 'RUNNING'
    COMPLETE = 'COMPLETE'
    PENDING = 'PENDING'
    ERROR = 'ERROR'
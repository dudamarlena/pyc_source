# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/entity/runtime_config.py
# Compiled at: 2020-05-06 02:27:06
# Size of source mod 2**32: 1744 bytes
import os, dotenv
from arch.api.utils.core_utils import get_lan_ip
from arch.api.utils.file_utils import get_project_base_directory
from fate_flow.entity.constant_config import ProcessRole

class RuntimeConfig(object):
    WORK_MODE = None
    BACKEND = None
    JOB_QUEUE = None
    USE_LOCAL_DATABASE = False
    HTTP_PORT = None
    JOB_SERVER_HOST = None
    IS_SERVER = False
    PROCESS_ROLE = None
    ENV = dict()

    @staticmethod
    def init_config(**kwargs):
        for k, v in kwargs.items():
            if hasattr(RuntimeConfig, k):
                setattr(RuntimeConfig, k, v)
                if k == 'HTTP_PORT':
                    setattr(RuntimeConfig, 'JOB_SERVER_HOST', '{}:{}'.format(get_lan_ip(), RuntimeConfig.HTTP_PORT))

    @staticmethod
    def init_env():
        RuntimeConfig.ENV.update(dotenv.dotenv_values(dotenv_path=(os.path.join(get_project_base_directory(), '.env'))))

    @staticmethod
    def get_env(key):
        return RuntimeConfig.ENV.get(key, None)

    @staticmethod
    def set_process_role(process_role: PROCESS_ROLE):
        RuntimeConfig.PROCESS_ROLE = process_role
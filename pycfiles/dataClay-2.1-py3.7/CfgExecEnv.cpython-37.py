# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/config/CfgExecEnv.py
# Compiled at: 2019-11-20 08:28:51
# Size of source mod 2**32: 2390 bytes
""" Class description goes here. """
import os, logging
from dataclay.commonruntime.Settings import settings
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'
logger = logging.getLogger(__name__)

def set_defaults():
    settings.tracing_enabled = False
    settings.extrae_starting_task_id = 0
    settings.server_listen_addr = '0.0.0.0'
    port_str = os.getenv('DATASERVICE_PYTHON_PORT_TCP', '6867')
    settings.server_listen_port = int(port_str)
    settings.pool_size = 4
    settings.interpreter_pool = None
    settings.cached_objects_size = 100
    settings.cached_classes_size = 1000
    settings.cached_metaclasses_size = 1000
    settings.cached_metaclass_info_size = 1000
    settings.cache_on_deploy = True
    deploy_path = os.getenv('DEPLOY_PATH', '/dataclay/deploy')
    settings.deploy_path = deploy_path
    settings.deploy_path_source = os.getenv('DEPLOY_PATH_SRC', os.path.join(deploy_path, 'source'))
    settings.storage_id = None
    settings.environment_id = None
    settings.dataservice_name = os.getenv('DATASERVICE_NAME')
    settings.dataservice_port = int(os.getenv('DATASERVICE_PYTHON_PORT_TCP', port_str))
    settings.logicmodule_host = os.getenv('LOGICMODULE_HOST', '127.0.0.1')
    settings.logicmodule_rmiport = int(os.getenv('LOGICMODULE_PORT_RMI', '1024'))
    settings.logicmodule_port = int(os.getenv('LOGICMODULE_PORT_TCP', '1034'))
    settings.loaded = True
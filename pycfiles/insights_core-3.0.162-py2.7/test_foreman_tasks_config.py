# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_foreman_tasks_config.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import foreman_tasks_config
from insights.parsers.foreman_tasks_config import ForemanTasksConfig
from insights.tests import context_wrap
FOREMAN_TASKS_CONFIG = '\nFOREMAN_USER=foreman\nBUNDLER_EXT_HOME=/usr/share/foreman\nRAILS_ENV=production\nFOREMAN_LOGGING=warn\nFOREMAN_LOGGING_SQL=warn\nFOREMAN_TASK_PARAMS="-p foreman"\nFOREMAN_LOG_DIR=/var/log/foreman\n\nRUBY_GC_MALLOC_LIMIT=4000100\nRUBY_GC_MALLOC_LIMIT_MAX=16000100\nRUBY_GC_MALLOC_LIMIT_GROWTH_FACTOR=1.1\nRUBY_GC_OLDMALLOC_LIMIT=16000100\nRUBY_GC_OLDMALLOC_LIMIT_MAX=16000100\n\n#Set the number of executors you want to run\n#EXECUTORS_COUNT=1\n\n#Set memory limit for executor process, before it\'s restarted automatically\n#EXECUTOR_MEMORY_LIMIT=2gb\n\n#Set delay before first memory polling to let executor initialize (in sec)\n#EXECUTOR_MEMORY_MONITOR_DELAY=7200 #default: 2 hours\n\n#Set memory polling interval, process memory will be checked every N seconds.\n#EXECUTOR_MEMORY_MONITOR_INTERVAL=60\n'

def test_foreman_tasks_config():
    foreman_tasks_config = ForemanTasksConfig(context_wrap(FOREMAN_TASKS_CONFIG)).data
    assert foreman_tasks_config['RAILS_ENV'] == 'production'
    assert foreman_tasks_config.get('FOREMAN_LOGGING') == 'warn'
    assert len(foreman_tasks_config) == 12


def test_foreman_tasks_config_doc_examples():
    env = {'foreman_tasks_config': ForemanTasksConfig(context_wrap(FOREMAN_TASKS_CONFIG)).data}
    failed, total = doctest.testmod(foreman_tasks_config, globs=env)
    assert failed == 0
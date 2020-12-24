# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockerfly/settings.py
# Compiled at: 2016-07-01 02:21:48
import os
here = os.path.abspath(os.path.dirname(__file__))
dockerfly_version = open(os.path.join(here, 'version.txt')).read().strip()
VAR_ROOT = '/var/dockerfly'
LOG_ROOT = os.path.join(VAR_ROOT, 'log')
DB_ROOT = os.path.join(VAR_ROOT, 'db')
RUN_ROOT = os.path.join(VAR_ROOT, 'run')
LOCK_TIMEOUT = 10
DAEMON_PROCESS_COUNT = 20
default_container_db = os.path.join(DB_ROOT, 'containers.json')
default_ippool_db = os.path.join(DB_ROOT, 'ippool.json')
dbs = [default_container_db, default_ippool_db]
TEST_MOTHER_ETH_NAME = 'ens33'
try:
    from local_settings import *
except ImportError:
    pass
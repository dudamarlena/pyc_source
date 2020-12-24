# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/settings.py
# Compiled at: 2017-11-06 21:54:55
# Size of source mod 2**32: 399 bytes
import os, logging
LISTEN_PORT = 27851
N_THREAD_WORKER = 8
N_PROCESS_WORKER = 8
CWD = os.path.dirname(__file__)
LOG_NAME = 'ramjet-driver'
LOG_DIR = '/tmp'
LOG_PATH = '{}.log'.format(os.path.join(LOG_DIR, LOG_NAME))
logger = logging.getLogger(LOG_NAME)
OK = 0
ERROR = 1
INSTALL_TASKS = [
 'heart']
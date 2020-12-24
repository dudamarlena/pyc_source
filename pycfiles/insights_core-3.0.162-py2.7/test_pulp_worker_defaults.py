# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_pulp_worker_defaults.py
# Compiled at: 2019-05-16 13:41:33
from ...parsers import pulp_worker_defaults
from ...tests import context_wrap
import doctest
pulp_worker_defaults_in_docs = '\n# Configuration file for Pulp\'s Celery workers\n\n# Define the number of worker nodes you wish to have here. This defaults to the number of processors\n# that are detected on the system if left commented here.\nPULP_CONCURRENCY=1\n\n# Configure Python\'s encoding for writing all logs, stdout and stderr\nPYTHONIOENCODING="UTF-8"\n'

def test_pulp_worker_defaults_docs():
    env = {'PulpWorkerDefaults': pulp_worker_defaults.PulpWorkerDefaults, 
       'shared': {pulp_worker_defaults.PulpWorkerDefaults: pulp_worker_defaults.PulpWorkerDefaults(context_wrap(pulp_worker_defaults_in_docs))}}
    failed, total = doctest.testmod(pulp_worker_defaults, globs=env)
    assert failed == 0
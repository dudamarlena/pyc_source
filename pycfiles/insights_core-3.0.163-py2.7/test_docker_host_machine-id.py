# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_docker_host_machine-id.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import docker_host_machine_id
from insights.tests import context_wrap
DOCKER_HOST_MACHINE_ID = '\ne6637bbb-ae92-46f8-a249-92d184c5fc24\n'

def test_docker_host_machine_id():
    machine_id = docker_host_machine_id.docker_host_machineid_parser(context_wrap(DOCKER_HOST_MACHINE_ID))
    assert machine_id.get('host_system_id') == 'e6637bbb-ae92-46f8-a249-92d184c5fc24'
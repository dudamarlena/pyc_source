# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_pid_storage.py
# Compiled at: 2020-04-03 13:49:55
# Size of source mod 2**32: 826 bytes
import pytest
from konduit.load import server_from_file
from konduit.load import store_pid, pop_pid
from konduit.server import stop_server_by_pid

@pytest.mark.unit
def test_pid_storage():
    file_path = 'yaml/konduit.yaml'
    store_pid(file_path, 123)
    pid = pop_pid(file_path)
    assert pid == 123


@pytest.mark.integration
def test_pid_creation_removal():
    file_path = 'yaml/konduit.yaml'
    running_server = server_from_file(file_path, start_server=True)
    pid = running_server.process.pid
    store_pid(file_path=file_path, pid=(running_server.process.pid))
    del running_server
    recov_pid = pop_pid(file_path=file_path)
    assert pid == recov_pid
    stop_server_by_pid(recov_pid)
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/martin/amonagent/tests/runner_test.py
# Compiled at: 2014-05-20 04:17:01
from amonagent.runner import runner

class TestRunner(object):

    def test_info_run(self):
        info_test = runner.info()
        assert isinstance(info_test, dict)
        assert 'processor' in info_test
        assert 'ip_address' in info_test
        assert 'distro' in info_test
        assert 'uptime' in info_test

    def test_system_run(self):
        system_test = runner.system()
        assert isinstance(system_test, dict)
        assert 'network' in system_test
        assert 'memory' in system_test
        assert 'cpu' in system_test
        assert 'disk' in system_test
        assert 'loadavg' in system_test

    def test_process_run(self):
        processes = runner.processes()
        assert isinstance(processes, dict)
        for process in processes:
            process_dict = processes[process]
            assert 'memory_mb' in process_dict
            assert 'cpu' in process_dict
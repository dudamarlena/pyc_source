# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/martin/amonagent/tests/modules_processes_test.py
# Compiled at: 2014-05-20 04:17:01
from amonagent.modules.processes import processes_data_collector

class TestProcessCheck(object):

    def test_processes_data(self):
        result = processes_data_collector.collect()
        for key, value in result.items():
            assert 'memory_mb' in value
            assert 'cpu' in value
            assert 'kb_write' in value
            assert 'kb_read' in value
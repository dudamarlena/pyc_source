# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/test/hydro/common/test_execution_plan.py
# Compiled at: 2014-11-23 10:45:29
__author__ = 'yanivshalev'
import unittest
from hydro.common.execution_plan import ExecutionPlan

class ExecutionPlanTest(unittest.TestCase):

    def test_add_phase(self):
        ep = ExecutionPlan()
        ep.add_phase(ExecutionPlan, 'test_phase1', metadata={'test_key1': 'test_val1'})
        ep.add_phase(ExecutionPlan, 'test_phase2', metadata={'test_key2': 'test_val2'})
        phase1, phase2 = ep
        self.assertEquals(phase1.phase_name, 'test_phase1')
        self.assertEquals(phase1.metadata, {'test_key1': 'test_val1'})
        self.assertEquals(phase1.phase_type, 'type')
        self.assertEquals(phase1._id, 0)
        self.assertEquals(phase2.phase_name, 'test_phase2')
        self.assertEquals(phase2.metadata, {'test_key2': 'test_val2'})
        self.assertEquals(phase2.phase_type, 'type')
        self.assertEquals(phase2._id, 1)
        val = eval('[' + ep.to_string().replace('\n', ',') + ']')
        val[0]['timestamp'] = 0
        val[1]['timestamp'] = 0
        to_comp = [{'timestamp': 0, 'phase_type': 'type', 'phase_name': 'test_phase1', 'id': 0, 'metadata': {'test_key1': 'test_val1'}}, {'timestamp': 0, 'phase_type': 'type', 'phase_name': 'test_phase2', 'id': 1, 'metadata': {'test_key2': 'test_val2'}}]
        self.assertEquals(val, to_comp)


if __name__ == '__main__':
    unittest.main()
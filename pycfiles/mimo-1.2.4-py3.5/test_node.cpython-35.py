# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_workflow/test_node.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 710 bytes
import unittest
from mimo import Workflow, Stream

class TestStep(unittest.TestCase):

    def test_pipe(self):
        workflow = Workflow()
        step1 = workflow.add_stream(Stream(['a'], ['b']))
        step2 = workflow.add_stream(Stream(['c'], ['d']))
        step1.pipe(step2)
        self.assertEqual(2, len(workflow.streams))
        self.assertIn(step2.input_ids['c'], workflow.graph.graph.adjacency[step1.output_ids['b']].children)

    def test_push(self):
        workflow = Workflow()
        step = workflow.add_stream(Stream(['a'], ['b']))
        step.push(0)
        self.assertEqual(0, workflow.inputs[step.input_ids['a']].get_nowait())


if __name__ == '__main__':
    unittest.main()
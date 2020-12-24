# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/test/test_problem_builder.py
# Compiled at: 2020-03-16 23:56:40
# Size of source mod 2**32: 653 bytes
import unittest, casadi.casadi as cs, opengen as og

class ProblemBuilderTestCase(unittest.TestCase):

    def test_add_sx_decision_variables(self):
        u = cs.SX.sym('u', 10)
        x = cs.SX.sym('x', 4)
        pb = og.builder.ProblemBuilder()
        pb.add_decision_variable(u, x)
        self.assertEqual(14, len(pb.decision_variables))

    def test_add_mx_decision_variables(self):
        u = cs.MX.sym('u', 10)
        x = cs.MX.sym('x', 4)
        pb = og.builder.ProblemBuilder()
        pb.add_decision_variable(u, x)
        self.assertEqual(2, len(pb.decision_variables))


if __name__ == '__main__':
    unittest.main()
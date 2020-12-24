# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\ir\edge.py
# Compiled at: 2020-01-10 07:45:30
# Size of source mod 2**32: 4975 bytes
__doc__ = '\n'
from typing import List
from pyrates import PyRatesException
from pyrates.ir.node import NodeIR
from pyrates.ir.operator import OperatorIR
__author__ = 'Daniel Rose'
__status__ = 'Development'

class EdgeIR(NodeIR):
    __slots__ = [
     '_inputs']

    def __init__(self, operators=None, values=None, template=None):
        if not operators:
            operators = {}
            values = {}
        super().__init__(operators, values, template)
        self._inputs = None

    @property
    def input(self):
        """Redirects to `self.inputs` for compatibility."""
        return self.inputs

    @property
    def input_var(self):
        return self.inputs

    @property
    def inputs(self):
        """Detect input variables of edge. This also references the operator
         the variable belongs to.

         Note: As of `0.9.0` multiple source/input variables are allowed per edge."""
        inputs = self.get_inputs()
        if len(inputs) == 0:
            return
        else:
            return inputs

    @property
    def n_inputs(self):
        """Computes number of input variables that need to be informed from outside the edge (meaning from some node).
        """
        inputs = self.get_inputs()
        return len(inputs)

    def get_inputs(self):
        """Find all input variables of operators that need to be mapped to source variables in a source node."""
        try:
            len(self._inputs)
        except TypeError:
            inputs = dict()
            for op, op_data in self.op_graph.nodes(data=True):
                for var, var_data in op_data['inputs'].items():
                    if len(var_data['sources']) == 0:
                        key = f"{op}/{var}"
                        try:
                            inputs[var].append(key)
                        except KeyError:
                            inputs[var] = [
                             key]

            self._inputs = inputs

        return self._inputs

    @property
    def output(self):
        """Detect output variable of edge, assuming only one output variable exists."""
        out_op = [op for op, out_degree in self.op_graph.out_degree if out_degree == 0]
        if len(out_op) == 1:
            out_var = self[out_op[0]].output
            return f"{out_op[0]}/{out_var}"
        if len(out_op) == 0:
            return
        raise PyRatesException('Too many or too little output operators found. Exactly one output operator and associated output variable is required per edge.')

    @property
    def output_var(self):
        return self.output

    def __hash__(self):
        raise NotImplementedError
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bms/physical/electrical.py
# Compiled at: 2020-04-02 08:37:19
# Size of source mod 2**32: 10571 bytes
__doc__ = '\n\n'
from bms import PhysicalNode, PhysicalBlock, Variable, np
from bms.blocks.continuous import Sum, Gain, Subtraction, ODE, WeightedSum, Product
from bms.blocks.nonlinear import Saturation
from bms.signals.functions import Step

class ElectricalNode(PhysicalNode):

    def __init__(self, name=''):
        PhysicalNode.__init__(self, False, True, name, 'Voltage', 'Intensity')

    def ConservativeLaw(self, flux_variables, output_variable):
        return [
         WeightedSum(flux_variables, output_variable, [-1] * len(flux_variables))]


class Ground(PhysicalBlock):

    def __init__(self, node1, name='Ground'):
        occurence_matrix = np.array([[1, 0]])
        PhysicalBlock.__init__(self, [node1], [], occurence_matrix, [], name)

    def PartialDynamicSystem(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """
        if ieq == 0:
            if variable == self.physical_nodes[0].variable:
                v = Step('Ground', 0)
                return [
                 Gain(v, variable, 1)]


class Resistor(PhysicalBlock):

    def __init__(self, node1, node2, R, name='Resistor'):
        occurence_matrix = np.array([[1, 1, 1, 0], [0, 1, 0, 1]])
        PhysicalBlock.__init__(self, [node1, node2], [
         0, 1], occurence_matrix, [], name)
        self.R = R

    def PartialDynamicSystem(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """
        if ieq == 0:
            if variable == self.physical_nodes[0].variable:
                return [
                 WeightedSum([self.physical_nodes[1].variable, self.variables[0]], variable, [1, self.R])]
            if variable == self.physical_nodes[1].variable:
                return [
                 WeightedSum([self.physical_nodes[0].variable, self.variables[0]], variable, [1, -self.R])]
            if variable == self.variables[0]:
                return [
                 WeightedSum([self.physical_nodes[0].variable, self.physical_nodes[1].variable], variable, [1 / self.R, -1 / self.R])]
        elif ieq == 1:
            if variable == self.variables[0]:
                return [
                 Gain(self.variables[1], self.variables[0], -1)]
            if variable == self.variables[1]:
                return [
                 Gain(self.variables[0], self.variables[1], -1)]


class Generator(PhysicalBlock):
    """Generator"""

    def __init__(self, node1, node2, voltage_signal, name='GeneratorGround'):
        occurence_matrix = np.array([[1, 0, 1, 0]])
        PhysicalBlock.__init__(self, [node1, node2], [
         0, 1], occurence_matrix, [], name)
        self.voltage_signal = voltage_signal

    def PartialDynamicSystem(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """
        if ieq == 0:
            if variable == self.physical_nodes[0].variable:
                return [
                 WeightedSum([self.physical_nodes[1].variable, self.voltage_signal], variable, [1, -1])]
            if variable == self.physical_nodes[1].variable:
                return [
                 WeightedSum([self.physical_nodes[0].variable, self.voltage_signal], variable, [1, 1])]


class Capacitor(PhysicalBlock):

    def __init__(self, node1, node2, C, name='Capacitor'):
        occurence_matrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1]])
        PhysicalBlock.__init__(self, [node1, node2], [
         0, 1], occurence_matrix, [], name)
        self.C = C

    def PartialDynamicSystem(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """
        if ieq == 0:
            if variable == self.physical_nodes[0].variable:
                print('1')
                Uc = Variable(hidden=True)
                block1 = ODE(self.variables[0], Uc, [1], [0, self.C])
                sub1 = Sum([self.physical_nodes[1].variable, Uc], variable)
                return [
                 block1, sub1]
            if variable == self.physical_nodes[1].variable:
                print('2')
                Uc = Variable(hidden=True)
                block1 = ODE(self.variables[0], Uc, [-1], [0, self.C])
                sum1 = Sum([self.physical_nodes[0].variable, Uc], variable)
                return [
                 block1, sum1]
        elif ieq == 1:
            if variable == self.variables[0]:
                return [
                 Gain(self.variables[1], self.variables[0], -1)]
            if variable == self.variables[1]:
                return [
                 Gain(self.variables[0], self.variables[1], -1)]


class Inductor(PhysicalBlock):

    def __init__(self, node1, node2, L, name='Inductor'):
        occurence_matrix = np.array([[1, 1, 1, 0], [0, 1, 0, 1]])
        PhysicalBlock.__init__(self, [node1, node2], [
         0, 1], occurence_matrix, [], name)
        self.L = L

    def PartialDynamicSystem(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """
        if ieq == 0:
            if variable == self.variables[0]:
                print('3')
                Uc = Variable(hidden=True)
                subs1 = Subtraction(self.physical_nodes[0].variable, self.physical_nodes[1].variable, Uc)
                block1 = ODE(Uc, variable, [1], [0, self.L])
                return [
                 block1, subs1]
        elif ieq == 1:
            if variable == self.variables[0]:
                return [
                 Gain(self.variables[1], self.variables[0], -1)]
            if variable == self.variables[1]:
                return [
                 Gain(self.variables[0], self.variables[1], -1)]
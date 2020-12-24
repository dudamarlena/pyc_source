# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bms/core.py
# Compiled at: 2020-04-02 08:37:19
# Size of source mod 2**32: 27134 bytes
__doc__ = '\nCore of BMS. All content of this file is imported by bms, and is therefore in bms\n\nThis file defines the base of BMS. \n\n'
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx, dill
from scipy.optimize import fsolve, root, minimize

class Variable:
    """Variable"""

    def __init__(self, names='variable', initial_values=[0], hidden=False):
        if type(names) == str:
            self.name = names
            self.short_name = names
        else:
            try:
                self.short_name = names[1]
                self.name = names[0]
            except:
                raise TypeError

        self.initial_values = initial_values
        self._values = np.array([])
        self.max_order = 0
        self.hidden = hidden

    def _InitValues(self, ns, ts, max_order):
        self.max_order = max_order
        self._values = self.initial_values[0] * np.ones(ns + max_order + 1)
        self._ForwardValues()

    def _ForwardValues(self):
        pass

    def _get_values(self):
        return self._values[self.max_order:]

    values = property(_get_values)


class Signal(Variable):
    """Signal"""

    def __init__(self, names):
        if type(names) == str:
            self.name = names
            self.short_name = names
        else:
            try:
                self.short_name = names[1]
                self.name = names[0]
            except:
                raise TypeError

        self._values = np.array([])
        self.max_order = 0
        self.hidden = False

    def _InitValues(self, ns, ts, max_order):
        self.max_order = max_order
        self._values = np.zeros(ns + max_order + 1)
        for i in range(ns + 1):
            self._values[i + max_order] = self.function(i * ts)

        self._ForwardValues()
        self.initial_values = [self._values[0]]

    def _ForwardValues(self):
        """
        Implementation for problems with derivative conditions on variables
        """
        pass


class Block:
    """Block"""

    def __init__(self, inputs, outputs, max_input_order, max_output_order):
        self.inputs = []
        self.outputs = []
        self.n_inputs = len(inputs)
        self.n_outputs = len(outputs)
        for variable in inputs:
            self._AddInput(variable)

        for variable in outputs:
            self._AddOutput(variable)

        self.max_input_order = max_input_order
        self.max_output_order = max_output_order
        self.max_order = max(self.max_input_order, self.max_output_order)

    def _AddInput(self, variable):
        """
        Add one more variable as an input of the block

        :param variable: variable (or signal as it is also a variable)
        """
        if isinstance(variable, Variable):
            self.inputs.append(variable)
        else:
            print('Error: ', variable.name, variable, ' given is not a variable')
            raise TypeError

    def _AddOutput(self, variable):
        """
            Add one more variable as an output of the block

            :param variable: variable (or signal as it is also a variable)
        """
        if isinstance(variable, Variable):
            self.outputs.append(variable)
        else:
            print(variable)
            raise TypeError

    def InputValues(self, it, nsteps=None):
        """
            Returns the input values at a given iteration for solving the block outputs
        """
        if nsteps == None:
            nsteps = self.max_input_order
        I = np.zeros((self.n_inputs, nsteps))
        for iv, variable in enumerate(self.inputs):
            I[iv, :] = variable._values[it - nsteps + 1:it + 1]

        return I

    def OutputValues(self, it, nsteps=None):
        if nsteps == None:
            nsteps = self.max_output_order
        O = np.zeros((self.n_outputs, nsteps))
        for iv, variable in enumerate(self.outputs):
            O[iv, :] = variable._values[it - nsteps:it]

        return O

    def Solve(self, it, ts):
        step_outputs = self.Evaluate(it, ts)
        for i, step_output in enumerate(step_outputs):
            self.outputs[i]._values[it] = step_output


class ModelError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'Model Error: ' + self.message


class DynamicSystem:
    """DynamicSystem"""

    def __init__(self, te, ns, blocks=[]):
        self.te = te
        self.ns = ns
        self.ts = self.te / float(self.ns)
        self.t = np.linspace(0, (self.te), num=(ns + 1))
        self.blocks = []
        self.variables = []
        self.signals = []
        self.max_order = 0
        for block in blocks:
            self.AddBlock(block)

        self._utd_graph = False

    def AddBlock(self, block):
        """
        Add the given block to the model and also its input/output variables
        """
        if isinstance(block, Block):
            self.blocks.append(block)
            self.max_order = max(self.max_order, block.max_input_order - 1)
            self.max_order = max(self.max_order, block.max_output_order)
            for variable in block.inputs + block.outputs:
                self._AddVariable(variable)

        else:
            print(block)
            raise TypeError
        self._utd_graph = False

    def _AddVariable(self, variable):
        """
        Add a variable to the model. Should not be used by end-user
        """
        if isinstance(variable, Signal):
            if variable not in self.signals:
                self.signals.append(variable)
        elif isinstance(variable, Variable):
            if variable not in self.variables:
                self.variables.append(variable)
        else:
            raise TypeError
        self._utd_graph = False

    def _get_Graph(self):
        if not self._utd_graph:
            self._graph = nx.DiGraph()
            for variable in self.variables:
                self._graph.add_node(variable, bipartite=0)

            for block in self.blocks:
                self._graph.add_node(block, bipartite=1)
                for variable in block.inputs:
                    self._graph.add_edge(variable, block)

                for variable in block.outputs:
                    self._graph.add_edge(block, variable)

            self._utd_graph = True
        return self._graph

    graph = property(_get_Graph)

    def _ResolutionOrder(self, variables_to_solve):
        """
        return a list of lists of tuples (block,output,ndof) to be solved

        """
        Gp = nx.DiGraph()
        for variable in self.variables:
            Gp.add_node(variable, bipartite=0)

        for block in self.blocks:
            for iov, output_variable in enumerate(block.outputs):
                Gp.add_node((block, iov), bipartite=1)
                Gp.add_edge((block, iov), output_variable)
                Gp.add_edge(output_variable, (block, iov))
                for input_variable in block.inputs:
                    if not isinstance(input_variable, Signal):
                        Gp.add_edge(input_variable, (block, iov))

        sinks = []
        sources = []
        for node in Gp.nodes():
            if Gp.out_degree(node) == 0:
                sinks.append(node)

        G2 = sources[:]
        for node in sources:
            for node2 in nx.descendants(Gp, node):
                if node2 not in G2:
                    G2.append(node2)

        if G2 != []:
            print(G2)
            raise ModelError('Overconstrained variables')
        G3 = sinks[:]
        for node in sinks:
            for node2 in nx.ancestors(Gp, node):
                if node2 not in G3:
                    G3.append(node2)

        if G3 != []:
            raise ModelError('Underconstrained variables')
        scc = list(nx.strongly_connected_components(Gp))
        if scc != []:
            C = nx.condensation(Gp, scc)
            isc_vars = []
            for isc, sc in enumerate(scc):
                for var in variables_to_solve:
                    if var in sc:
                        isc_vars.append(isc)
                        break

            ancestors_vars = isc_vars[:]
            for isc_var in isc_vars:
                for ancetre in nx.ancestors(C, isc_var):
                    if ancetre not in ancestors_vars:
                        ancestors_vars.append(ancetre)

            order_sc = [sc for sc in nx.topological_sort(C) if sc in ancestors_vars]
            order_ev = []
            for isc in order_sc:
                evs = list(scc[isc])
                eqs = []
                var = []
                for element in evs:
                    if type(element) == tuple:
                        eqs.append(element)
                    else:
                        var.append(element)

                order_ev.append((len(eqs), eqs, var))

            return order_ev
        raise ModelError

    def Simulate(self, variables_to_solve=None):
        if variables_to_solve == None:
            variables_to_solve = [variable for variable in self.variables if not variable.hidden]
        order = self._ResolutionOrder(variables_to_solve)
        for variable in self.variables + self.signals:
            variable._InitValues(self.ns, self.ts, self.max_order)

        residue = []
        for it, t in enumerate(self.t[1:]):
            for neqs, equations, variables in order:
                if neqs == 1:
                    equations[0][0].Solve(it + self.max_order + 1, self.ts)
                else:
                    x0 = [equations[i][0].outputs[equations[i][1]]._values[(it + self.max_order)] for i in range(len(equations))]

                    def r(x, equations=equations[:]):
                        for i, xi in enumerate(x):
                            equations[i][0].outputs[equations[i][1]]._values[it + self.max_order + 1] = xi

                        r = []
                        for ieq, (block, neq) in enumerate(equations):
                            r.append(x[ieq] - block.Evaluate(it + self.max_order + 1, self.ts)[neq])

                        return r

                    def f(x, equations=equations[:]):
                        for i, xi in enumerate(x):
                            equations[i][0].outputs[equations[i][1]]._values[it + self.max_order + 1] = xi

                        s = 0
                        for ieq, (block, neq) in enumerate(equations):
                            s += abs(x[ieq] - block.Evaluate(it + self.max_order + 1, self.ts)[neq])

                        return s

                    x, d, i, m = fsolve(r, x0, full_output=True)

    def VariablesValues(self, variables, t):
        """
        Returns the value of given variables at time t. 
        Linear interpolation is performed between two time steps.

        :param variables: one variable or a list of variables
        :param t: time of evaluation
        """
        if (t < self.te) | (t > 0):
            i = t // self.ts
            ti = self.ts * i
            if type(variables) == list:
                values = []
                for variable in variables:
                    values.append(variables.values[i] * ((ti - t) / self.ts + 1) + variables.values[(i + 1)] * (t - ti) / self.ts)

                return values
            return variables.values[i] * ((ti - t) / self.ts + 1) + variables.values[(i + 1)] * (t - ti) / self.ts
        else:
            raise ValueError

    def PlotVariables(self, subplots_variables=None):
        if subplots_variables == None:
            subplots_variables = [
             self.signals + self.variables]
            subplots_variables = [
             [variable for variable in self.signals + self.variables if not variable.hidden]]
        fig, axs = plt.subplots((len(subplots_variables)), sharex=True)
        if len(subplots_variables) == 1:
            axs = [
             axs]
        for isub, subplot in enumerate(subplots_variables):
            legend = []
            for variable in subplot:
                axs[isub].plot(self.t, variable.values)
                legend.append(variable.name)

            axs[isub].legend(legend, loc='best')
            axs[isub].margins(0.08)
            axs[isub].grid()

        plt.xlabel('Time')
        plt.show()

    def DrawModel(self):
        from .interface import ModelDrawer
        ModelDrawer(self)

    def Save(self, name_file):
        """
            name_file: name of the file without extension.
            The extension .bms is added by function
        """
        with open(name_file + '.bms', 'wb') as (file):
            model = dill.dump(self, file)

    def __getstate__(self):
        dic = self.__dict__.copy()
        return dic

    def __setstate__(self, dic):
        self.__dict__ = dic


def Load(file):
    """ Loads a model from specified file """
    with open(file, 'rb') as (file):
        model = dill.load(file)
        return model


class PhysicalNode:
    """PhysicalNode"""

    def __init__(self, cl_solves_potential, cl_solves_fluxes, node_name, potential_variable_name, flux_variable_name):
        self.cl_solves_potential = cl_solves_potential
        self.cl_solves_fluxes = cl_solves_fluxes
        self.name = node_name
        self.potential_variable_name = potential_variable_name
        self.flux_variable_name = flux_variable_name
        self.variable = Variable(potential_variable_name + ' ' + node_name)


class PhysicalBlock:
    """PhysicalBlock"""

    def __init__(self, physical_nodes, nodes_with_fluxes, occurence_matrix, commands, name):
        self.physical_nodes = physical_nodes
        self.name = name
        self.nodes_with_fluxes = nodes_with_fluxes
        self.occurence_matrix = occurence_matrix
        self.commands = commands
        self.variables = [Variable(physical_nodes[inode].flux_variable_name + ' from ' + physical_nodes[inode].name + ' to ' + self.name) for inode in nodes_with_fluxes]


class PhysicalSystem:
    """PhysicalSystem"""

    def __init__(self, te, ns, physical_blocks, command_blocks):
        self.te = te
        self.ns = ns
        self.physical_blocks = []
        self.physical_nodes = []
        self.variables = []
        self.command_blocks = []
        for block in physical_blocks:
            self.AddPhysicalBlock(block)

        for block in command_blocks:
            self.AddCommandBlock(block)

        self._utd_ds = False

    def AddPhysicalBlock(self, block):
        if isinstance(block, PhysicalBlock):
            self.physical_blocks.append(block)
            for node in block.physical_nodes:
                self._AddPhysicalNode(node)

        else:
            raise TypeError
        self._utd_ds = False

    def _AddPhysicalNode(self, node):
        if isinstance(node, PhysicalNode):
            if node not in self.physical_nodes:
                self.physical_nodes.append(node)
        self._utd_ds = False

    def AddCommandBlock(self, block):
        if isinstance(block, Block):
            self.command_blocks.append(block)
            for variable in block.inputs + block.outputs:
                self._AddVariable(variable)

        else:
            raise TypeError
        self._utd_ds = False

    def _AddVariable(self, variable):
        if isinstance(variable, Variable):
            if variable not in self.variables:
                self.variables.append(variable)
        self._utd_ds = False

    def GenerateDynamicSystem(self):
        G = nx.Graph()
        for node in self.physical_nodes:
            G.add_node((node.variable), bipartite=0)

        for block in self.physical_blocks:
            for variable in block.variables:
                G.add_node((node.variable), bipartite=0)

            ne, nv = block.occurence_matrix.shape
            for ie in range(ne):
                G.add_node((block, ie), bipartite=1)
                for iv in range(nv):
                    if block.occurence_matrix[(ie, iv)] == 1:
                        if iv % 2 == 0:
                            G.add_edge((
                             block, ie), block.physical_nodes[(iv // 2)].variable)
                        else:
                            G.add_edge((block, ie), block.variables[(iv // 2)])

        for node in self.physical_nodes:
            if node.cl_solves_potential:
                G.add_edge(node, node.variable)
            if node.cl_solves_fluxes:
                G.add_node(node, bipartite=1)
                for block in self.physical_blocks:
                    for inb in block.nodes_with_fluxes:
                        node_block = block.physical_nodes[inb]
                        if node == node_block:
                            G.add_edge(node, block.variables[block.nodes_with_fluxes.index(inb)])

        G2 = nx.DiGraph()
        G2.add_nodes_from(G)
        eq_out_var = {}
        for e in nx.bipartite.maximum_matching(G).items():
            if e[0].__class__.__name__ == 'Variable':
                G2.add_edge(e[1], e[0])
                eq_out_var[e[1]] = e[0]
            else:
                G2.add_edge(e[0], e[1])
                eq_out_var[e[0]] = e[1]

        for e in G.edges():
            if e[0].__class__.__name__ == 'Variable':
                G2.add_edge(e[0], e[1])
            else:
                G2.add_edge(e[1], e[0])

        sinks = []
        sources = []
        for node in G2.nodes():
            if G2.out_degree(node) == 0:
                sinks.append(node)

        if sinks != []:
            print(sinks)
            raise ModelError
        if sources != []:
            print(sources)
            raise ModelError
        model_blocks = []
        for block_node, variable in eq_out_var.items():
            if type(block_node) == tuple:
                model_blocks.extend(block_node[0].PartialDynamicSystem(block_node[1], variable))
            else:
                variables = []
                for block in self.physical_blocks:
                    try:
                        ibn = block.physical_nodes.index(block_node)
                        if ibn in block.nodes_with_fluxes:
                            variable2 = block.variables[ibn]
                            if variable2 != variable:
                                variables.append(variable2)
                    except ValueError:
                        pass

                model_blocks.extend(block_node.ConservativeLaw(variables, variable))

        model_blocks.extend(self.command_blocks)
        return DynamicSystem(self.te, self.ns, model_blocks)

    def _get_ds(self):
        if not self._utd_ds:
            self._dynamic_system = self.GenerateDynamicSystem()
            self._utd_ds = True
        return self._dynamic_system

    dynamic_system = property(_get_ds)

    def Simulate(self):
        self.dynamic_system.Simulate()
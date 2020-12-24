# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/genmechanics/dynamic_positions.py
# Compiled at: 2020-03-26 14:17:33
# Size of source mod 2**32: 58733 bytes
"""

"""
import os, webbrowser, math, random, numpy as npy, cma
from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow
import networkx as nx
from jinja2 import Environment, PackageLoader, select_autoescape
from dessia_common.core import DessiaObject
from scipy.optimize import minimize
import volmdlr as vm
from genmechanics.core import Part, Mechanism

class Parameter(DessiaObject):

    def __init__(self, lower_bound, upper_bound, periodicity=None):
        DessiaObject.__init__(self, lower_bound=lower_bound,
          upper_bound=upper_bound,
          periodicity=periodicity)

    def random_value(self):
        return random.uniform(self.lower_bound, self.upper_bound)

    def are_values_equal(self, value1, value2, tol=0.001):
        if self.periodicity is not None:
            value1 = value1 % self.periodicity
            value2 = value2 % self.periodicity
        return math.isclose(value1, value2, abs_tol=tol)

    def optimizer_bounds(self):
        if self.periodicity is not None:
            return (
             self.lower_bound - 0.5 * self.periodicity,
             self.upper_bound + 0.5 * self.periodicity)
        return (self.lower_bound, self.upper_bound)


class Linkage(DessiaObject):
    _non_serializable_attributes = [
     'part1_position_function',
     'part2_position_function',
     'part1_basis_function',
     'part2_basis_function']

    def __init__(self, part1, part1_position_function, part1_basis_function, part2, part2_position_function, part2_basis_function, positions_require_kinematic_parameters, basis_require_kinematic_parameters, kinematic_parameters, name=''):
        """

        """
        DessiaObject.__init__(self, part1=part1,
          part1_position_function=part1_position_function,
          part1_basis_function=part1_basis_function,
          part2=part2,
          part2_position_function=part2_position_function,
          part2_basis_function=part2_basis_function,
          positions_require_kinematic_parameters=positions_require_kinematic_parameters,
          basis_require_kinematic_parameters=basis_require_kinematic_parameters,
          kinematic_parameters=kinematic_parameters,
          number_kinematic_parameters=(len(kinematic_parameters)),
          name=name)

    def equivalence_hash(self):
        h = 0
        if hasattr(self, 'part1_position'):
            h += hash(self.part1_position)
        if hasattr(self, 'part2_position'):
            h += hash(self.part2_position)
        if hasattr(self, 'part1_basis'):
            h += hash(self.part1_basis)
        if hasattr(self, 'part2_basis'):
            h += hash(self.part2_basis)
        return h

    def is_equivalent(self, other_linkage):
        if self.__class__ != other_linkage.__class__:
            return False
            if hasattr(self, 'part1_position'):
                if self.part1_position != other_linkage.part1_position:
                    return False
            if hasattr(self, 'part2_position'):
                if self.part2_position != other_linkage.part2_position:
                    return False
        else:
            if hasattr(self, 'part1_basis'):
                if self.part1_basis != other_linkage.part1_basis:
                    return False
            if hasattr(self, 'part2_basis') and self.part2_basis != other_linkage.part2_basis:
                return False
        return True

    def frame(self, linkage_parameters_values, side):
        if side:
            part1_frame = self.part1_basis_function(linkage_parameters_values).to_frame(self.part1_position_function(linkage_parameters_values))
            part2_frame = -self.part2_basis_function(linkage_parameters_values).to_frame(-self.part2_position_function(linkage_parameters_values))
            return part1_frame + part2_frame
        part1_frame = -self.part1_basis_function(linkage_parameters_values).to_frame(-self.part1_position_function(linkage_parameters_values))
        part2_frame = self.part2_basis_function(linkage_parameters_values).to_frame(self.part2_position_function(linkage_parameters_values))
        return part2_frame + part1_frame

    def babylonjs(self, initial_linkage_parameters, part1_parent=None, part2_parent=None):
        part1_position = self.part1_position_function(initial_linkage_parameters)
        part2_position = self.part2_position_function(initial_linkage_parameters)
        s = ''
        if part1_parent is not None:
            s += 'var linkage_part1_mesh = BABYLON.MeshBuilder.CreateSphere("default_linkage part1", {diameter: 0.02}, scene);\n'
            s += ('linkage_part1_mesh.position = new BABYLON.Vector3({}, {}, {});\n'.format)(*part1_position.vector)
            s += 'linkage_part1_mesh.parent = {};\n'.format(part1_parent)
        if part2_parent:
            s += 'var linkage_part2_mesh = BABYLON.MeshBuilder.CreateSphere("default_linkage part2", {diameter: 0.02}, scene);\n'
            s += ('linkage_part2_mesh.position = new BABYLON.Vector3({}, {}, {});\n'.format)(*part2_position.vector)
            s += 'linkage_part2_mesh.parent = {};\n'.format(part2_parent)
        return s


class RevoluteLinkage(Linkage):
    holonomic = True

    def __init__(self, part1, part1_position, part1_basis, part2, part2_position, part2_basis, name='RevoluteLinkage'):
        """
        :param part2_basis: a basis defining orientation of linkage on part2

        """

        def part1_basis_f(q):
            return part1_basis.Rotation((part1_basis.u), (q[0]), copy=True)

        def part2_basis_f(q):
            return part2_basis

        DessiaObject.__init__(self, part1_position=part1_position,
          part2_position=part2_position,
          part1_basis=part1_basis,
          part2_basis=part2_basis)
        Linkage.__init__(self, part1,
          (lambda q: part1_position), part1_basis_f, part2,
          (lambda q: part2_position), part2_basis_f, False,
          True, [
         Parameter(0.0, 2 * math.pi, 2 * math.pi)],
          name=name)

    def babylonjs(self, initial_linkage_parameters, part1_parent=None, part2_parent=None):
        s = ''
        if part1_parent is not None:
            s += ('var path1 = [new BABYLON.Vector3({}, {}, {}), new BABYLON.Vector3({}, {}, {})];\n'.format)(*self.part1_position - 0.03 * self.part1_basis.u, *self.part1_position + 0.03 * self.part1_basis.u)
            s += 'var linkage_part1_mesh = BABYLON.MeshBuilder.CreateTube("revolute part1", {path: path1, radius: 0.01, sideOrientation:BABYLON.Mesh.DOUBLESIDE}, scene);\n'
            s += 'linkage_part1_mesh.enableEdgesRendering();\n'
            s += 'linkage_part1_mesh.edgesWidth = 0.4;\n'
            s += 'linkage_part1_mesh.edgesColor = new BABYLON.Color4(0, 0, 0, 1);\n'
            s += 'linkage_part1_mesh.parent = {};\n'.format(part1_parent)
        if part2_parent is not None:
            s += ('var path2 = [new BABYLON.Vector3({}, {}, {}), new BABYLON.Vector3({}, {}, {})];\n'.format)(*self.part2_position - 0.03 * self.part2_basis.u, *self.part2_position + 0.03 * self.part2_basis.u)
            s += 'var linkage_part2_mesh = BABYLON.MeshBuilder.CreateTube("revolute part2", {path: path2, radius: 0.015, sideOrientation:BABYLON.Mesh.DOUBLESIDE}, scene);\n'
            s += 'linkage_part2_mesh.enableEdgesRendering();\n'
            s += 'linkage_part2_mesh.edgesWidth = 0.4;\n'
            s += 'linkage_part2_mesh.edgesColor = new BABYLON.Color4(0, 0, 0, 1);\n'
            s += 'linkage_part2_mesh.parent = {};\n'.format(part2_parent)
        return s


class SlidingRevoluteLinkage(Linkage):
    holonomic = True

    def __init__(self, part1, part1_position, part1_basis, part2, part2_position, part2_basis, name='SlidingRevoluteLinkage'):
        """
        :param part2_basis: a basis defining orientation of linkage on part2
        The first kineamtic parameter is the translation, the second the rotation
        """

        def part1_position_f(q):
            return part1_position + q[0] * part1_basis.u

        def part2_position_f(q):
            return part2_position

        def part1_basis_f(q):
            return part1_basis.Rotation((part1_basis.u), (q[1]), copy=True)

        DessiaObject.__init__(self, part1_position=part1_position,
          part2_position=part2_position,
          part1_basis=part1_basis,
          part2_basis=part2_basis)
        Linkage.__init__(self, part1, part1_position_f, part1_basis_f, part2, part2_position_f, lambda q: part2_basis, True, True, [
         Parameter(0.0, 2 * math.pi, 2 * math.pi),
         Parameter(-1.0, 1.0, None)], name)

    def babylonjs(self, initial_linkage_parameters, part1_parent=None, part2_parent=None):
        s = ''
        if part1_parent is not None:
            s += ('var path1 = [new BABYLON.Vector3({}, {}, {}), new BABYLON.Vector3({}, {}, {})];\n'.format)(*self.part1_position - 0.1 * self.part1_basis.u, *self.part1_position + 0.1 * self.part1_basis.u)
            s += 'var linkage_part1_mesh = BABYLON.MeshBuilder.CreateTube("revolute part1", {path: path1, radius: 0.01, sideOrientation:BABYLON.Mesh.DOUBLESIDE}, scene);\n'
            s += 'linkage_part1_mesh.enableEdgesRendering();\n'
            s += 'linkage_part1_mesh.edgesWidth = 0.4;\n'
            s += 'linkage_part1_mesh.edgesColor = new BABYLON.Color4(0, 0, 0, 1);\n'
            s += 'linkage_part1_mesh.parent = {};\n'.format(part1_parent)
        if part2_parent is not None:
            s += ('var path2 = [new BABYLON.Vector3({}, {}, {}), new BABYLON.Vector3({}, {}, {})];\n'.format)(*self.part2_position - 0.03 * self.part2_basis.u, *self.part2_position + 0.03 * self.part2_basis.u)
            s += 'var linkage_part2_mesh = BABYLON.MeshBuilder.CreateTube("revolute part2", {path: path2, radius: 0.015, sideOrientation:BABYLON.Mesh.DOUBLESIDE}, scene);\n'
            s += 'linkage_part2_mesh.enableEdgesRendering();\n'
            s += 'linkage_part2_mesh.edgesWidth = 0.4;\n'
            s += 'linkage_part2_mesh.edgesColor = new BABYLON.Color4(0, 0, 0, 1);\n'
            s += 'linkage_part2_mesh.parent = {};\n'.format(part2_parent)
        return s


class PrismaticLinkage(Linkage):
    holonomic = True

    def __init__(self, part1, part1_position, part1_basis, part2, part2_position, part2_basis, name='PrismaticLinkage'):
        """
        :param part2_basis: a basis defining orientation of linkage on part2

        """

        def part1_position_f(q):
            return part1_position + q[0] * part1_basis.u

        def part2_position_f(q):
            return part2_position

        DessiaObject.__init__(self, part1_position=part1_position,
          part2_position=part2_position,
          part1_basis=part1_basis,
          part2_basis=part2_basis)
        Linkage.__init__(self, part1, part1_position_f, lambda q: part1_basis, part2, part2_position_f, lambda q: part2_basis, True, False, [
         Parameter(-1, 1, None)], name)

    def babylonjs(self, initial_linkage_parameters, part1_parent=None, part2_parent=None):
        bp1 = self.part1_basis_function(initial_linkage_parameters)
        bp2 = self.part2_basis_function(initial_linkage_parameters)
        s = ''
        if part1_parent is not None:
            s += 'var linkage_part1_mesh = BABYLON.MeshBuilder.CreateBox("prismatic part1", {depth:0.015, height:0.015, width:0.25}, scene);\n'
            s += 'linkage_part1_mesh.parent = {};\n'.format(part1_parent)
            s += ('linkage_part1_mesh.position = new BABYLON.Vector3({}, {}, {});\n'.format)(*self.part1_position_function(initial_linkage_parameters))
            s += ('linkage_part1_mesh.rotation = BABYLON.Vector3.RotationFromAxis(new BABYLON.Vector3({}, {}, {}),new BABYLON.Vector3({}, {}, {}), new BABYLON.Vector3({}, {}, {}));\n'.format)(*bp1.u, *bp1.v, *bp1.w)
            s += 'linkage_part1_mesh.enableEdgesRendering();\n'
            s += 'linkage_part1_mesh.edgesWidth = 0.3;\n'
            s += 'linkage_part1_mesh.edgesColor = new BABYLON.Color4(0, 0, 0, 1);\n'
        if part2_parent is not None:
            s += 'var linkage_part2_mesh = BABYLON.MeshBuilder.CreateBox("prismatic part2", {depth:0.03, height:0.03, width:0.06}, scene);\n'
            s += 'linkage_part2_mesh.parent = {};\n'.format(part2_parent)
            s += ('linkage_part2_mesh.position = new BABYLON.Vector3({}, {}, {});\n'.format)(*self.part2_position_function(initial_linkage_parameters))
            s += ('linkage_part2_mesh.rotation = BABYLON.Vector3.RotationFromAxis(new BABYLON.Vector3({}, {}, {}),new BABYLON.Vector3({}, {}, {}), new BABYLON.Vector3({}, {}, {}));\n'.format)(*bp2.u, *bp2.v, *bp2.w)
            s += 'linkage_part2_mesh.enableEdgesRendering();\n'
            s += 'linkage_part2_mesh.edgesWidth = 0.3;\n'
            s += 'linkage_part2_mesh.edgesColor = new BABYLON.Color4(0, 0, 0, 1);\n'
        return s


class LimitedBallLinkage(Linkage):
    holonomic = True

    def __init__(self, part1, part1_position, part1_basis, part2, part2_position, part2_basis, name='LimitedBallLinkage'):
        """
        Allowed movements are:
            - a rotation around part1 basis u
            - a rotation around part1 basis v
            
        """

        def part1_basis_f(q):
            return part1_basis.Rotation((part1_basis.u), (q[0]), copy=True).Rotation((part1_basis.v),
              (q[1]), copy=True)

        def part2_basis_f(q):
            return part2_basis

        DessiaObject.__init__(self, part1_position=part1_position,
          part2_position=part2_position,
          part1_basis=part1_basis,
          part2_basis=part2_basis)
        Linkage.__init__(self, part1, lambda q: part1_position, part1_basis_f, part2, lambda q: part2_position, part2_basis_f, False, True, [
         Parameter(0.0, 2 * math.pi, 2 * math.pi),
         Parameter(0.0, 2 * math.pi, 2 * math.pi)], name)


class BallLinkage(Linkage):
    holonomic = True

    def __init__(self, part1, part1_position, part1_basis, part2, part2_position, part2_basis, name='BallLinkage'):
        """

        """
        DessiaObject.__init__(self, part1_position=part1_position,
          part2_position=part2_position,
          part1_basis=part1_basis,
          part2_basis=part2_basis)
        part1_basis_f, part2_basis_f = self.basis_functions()
        Linkage.__init__(self, part1, lambda q: part1_position, part1_basis_f, part2, lambda q: part2_position, part2_basis_f, False, True, [
         Parameter(0.0, 2 * math.pi, 2 * math.pi),
         Parameter(0.0, 2 * math.pi, 2 * math.pi),
         Parameter(0.0, 2 * math.pi, 2 * math.pi)], name)

    def update_part1_point(self, new_position):
        self.part1_position = new_position
        self.part1_position_function = lambda q: new_position

    def update_part2_point(self, new_position):
        self.part2_position = new_position
        self.part2_position_function = lambda q: new_position

    def basis_functions(self):

        def part1_basis_f(q):
            return self.part1_basis.Rotation((self.part1_basis.u), (q[0]), copy=True).Rotation((self.part1_basis.v),
              (q[1]), copy=True).Rotation((self.part1_basis.w),
              (q[2]), copy=True)

        def part2_basis_f(q):
            return self.part2_basis

        return (
         part1_basis_f, part2_basis_f)


class NoConfigurationFoundError(Exception):
    pass


class MovingMechanism(Mechanism):

    def __init__(self, linkages, ground, name=''):
        Mechanism.__init__(self, linkages,
          ground,
          {}, None,
          None,
          name=name)
        self._settings_path = {}
        self.settings_graph()
        n_kp = 0
        self.kinematic_parameters_mapping = {}
        for linkage in self.linkages_kinematic_setting:
            for i in range(linkage.number_kinematic_parameters):
                self.kinematic_parameters_mapping[(linkage, i)] = n_kp + i

            n_kp += linkage.number_kinematic_parameters

    def settings_graph(self):
        graph = self.holonomic_graph.copy()
        self.opened_linkages = []
        graph_cycles = nx.cycle_basis(graph)
        while len(graph_cycles) != 0:
            ground_distance = [(l, len(nx.shortest_path(graph, l, self.ground))) for l in graph_cycles[0] if l in self.linkages if l not in self.opened_linkages if not l.positions_require_kinematic_parameters]
            linkage_to_delete = max(ground_distance, key=(lambda x: x[1]))[0]
            self.opened_linkages.append(linkage_to_delete)
            graph.remove_node(linkage_to_delete)
            graph_cycles = nx.cycle_basis(graph)

        self.linkages_kinematic_setting = [l for l in self.linkages if l not in self.opened_linkages]
        self.settings_graph = graph

    def plot_settings_graph(self):
        s = '<html>\n        <head>\n        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.0/vis.min.js"></script>\n        <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.0/vis.min.css" rel="stylesheet" type="text/css" />\n\n        <style type="text/css">\n            #mynetwork {\n                border: 1px solid lightgray;\n            }\n        </style>\n    </head>\n    <body>\n    <div id="mynetwork"></div>\n\n    <script type="text/javascript">\n    var nodes = new vis.DataSet([\n'
        index = {}
        for ipart, part in enumerate(self.parts + [self.ground]):
            index[part] = ipart
            s += "{{id: {}, label: '{}'}},\n".format(ipart, part.name)

        n = len(self.parts) + 1
        for il, linkage in enumerate(self.linkages_kinematic_setting):
            index[linkage] = n + il
            s += "{{id: {}, label: '{}'}},\n".format(n + il, linkage.name)

        s += ']);\n'
        s += 'var edges = new vis.DataSet(['
        for linkage in self.linkages_kinematic_setting:
            s += '{{from: {}, to: {}}},\n'.format(index[linkage], index[linkage.part1])
            s += '{{from: {}, to: {}}},\n'.format(index[linkage], index[linkage.part2])

        s += ']);'
        s += "\n    // create a network\n    var container = document.getElementById('mynetwork');\n\n    // provide the data in the vis format\n    var data = {\n        nodes: nodes,\n        edges: edges\n    };\n    var options = {};\n\n    // initialize your network!\n    var network = new vis.Network(container, data, options);\n</script>\n</body>\n</html>"
        with open('gm_graph_viz.html', 'w') as (file):
            file.write(s)
        webbrowser.open('file://' + os.path.realpath('gm_graph_viz.html'))

    def settings_path(self, part1, part2):
        if (
         part1, part2) in self._settings_path:
            return self._settings_path[(part1, part2)]
            if (part2, part1) in self._settings_path:
                path = [(p2, linkage, not linkage_side, p1) for p1, linkage, linkage_side, p2 in self._settings_path[(part2, part1)][::-1]]
                self._settings_path[(part1, part2)] = path
                return self._settings_path[(part1, part2)]
        else:
            path = []
            try:
                raw_path = list(nx.shortest_path(self.settings_graph, part1, part2))
            except nx.NetworkXNoPath:
                self.plot_settings_graph()
                print(part1.name, part2.name)
                raise nx.NetworkXError

        for path_part1, linkage, path_part2 in zip(raw_path[:-2:2], raw_path[1::2], raw_path[2::2] + [part2]):
            path.append((path_part1, linkage, linkage.part1 == path_part1, path_part2))

        self._settings_path[(part1, part2)] = path
        return path

    def part_global_frame(self, part, kinematic_parameters_values):
        frame = vm.OXYZ
        for part1, linkage, linkage_side, part2 in self.settings_path(self.ground, part):
            linkage_parameters_values = self.extract_linkage_parameters_values(linkage, kinematic_parameters_values)
            linkage_frame = linkage.frame(linkage_parameters_values, side=linkage_side)
            frame = frame + linkage_frame

        return frame

    def part_relative_frame(self, part, reference_part, kinematic_parameters_values):
        frame = vm.OXYZ
        for part1, linkage, linkage_side, part2 in self.settings_path(reference_part, part):
            linkage_parameters_values = self.extract_linkage_parameters_values(linkage, kinematic_parameters_values)
            linkage_frame = linkage.frame(linkage_parameters_values, side=linkage_side)
            frame = frame + linkage_frame

        return frame

    def linkage_global_position(self, linkage, global_parameter_values):
        if linkage.positions_require_kinematic_parameters:
            ql = self.extract_linkage_parameters_values(linkage, global_parameter_values)
        else:
            ql = []
        part1_frame = self.part_global_frame(linkage.part1, global_parameter_values)
        return part1_frame.OldCoordinates(linkage.part1_position_function(ql))

    def extract_linkage_parameters_values(self, linkage, global_parameter_values):
        linkage_parameters = [global_parameter_values[self.kinematic_parameters_mapping[(linkage, i)]] for i in range(linkage.number_kinematic_parameters)]
        return linkage_parameters

    def opened_linkage_gap(self, linkage, global_parameter_values):
        if linkage.positions_require_kinematic_parameters:
            ql = self.extract_linkage_parameters_values(linkage, global_parameter_values)
        else:
            ql = []
        position1 = self.part_global_frame(linkage.part1, global_parameter_values).OldCoordinates(linkage.part1_position_function(ql))
        position2 = self.part_global_frame(linkage.part2, global_parameter_values).OldCoordinates(linkage.part2_position_function(ql))
        return position2 - position1

    def opened_linkage_misalignment(self, linkage, global_parameter_values):
        ql = self.extract_linkage_parameters_values(linkage, global_parameter_values)
        basis1 = self.part_global_frame(linkage.part1, global_parameter_values).Basis()
        basis2 = self.part_global_frame(linkage.part2, global_parameter_values).Basis()
        basis = basis2 - basis1 - linkage.basis(ql)
        return basis

    def opened_linkages_residue(self, q):
        residue = 0.0
        for linkage in self.opened_linkages:
            residue += self.opened_linkage_gap(linkage, q).Norm()

        return residue

    def reduced_x_to_full_x(self, xr, basis_vector, free_parameters_dofs):
        x = basis_vector[:]
        for qrv, i in zip(xr, free_parameters_dofs):
            x[i] = qrv

        return x

    def full_x_to_reduced_x(self, x, free_parameters_dofs):
        return [x[i] for i in free_parameters_dofs]

    def geometric_closing_residue_function(self, basis_vector, free_parameters_dofs):

        def residue_function(xr):
            x = self.reduced_x_to_full_x(xr, basis_vector, free_parameters_dofs)
            return self.opened_linkages_residue(x)

        return residue_function

    def _optimization_settings(self, imposed_parameters):
        free_parameters_dofs = []
        free_parameters = []
        n_free_parameters = 0
        n_parameters = len(self.kinematic_parameters_mapping.items())
        basis_vector = [0] * n_parameters
        for i in range(n_parameters):
            if i in imposed_parameters:
                basis_vector[i] = imposed_parameters[i]
            else:
                free_parameters_dofs.append(i)
                n_free_parameters += 1

        bounds = []
        for (linkage, iparameter), idof in self.kinematic_parameters_mapping.items():
            if idof in free_parameters_dofs:
                parameter = linkage.kinematic_parameters[iparameter]
                free_parameters.append(parameter)
                bounds.append(parameter.optimizer_bounds())
            bounds_cma = [[], []]
            for bmin, bmax in bounds:
                bounds_cma[0].append(bmin)
                bounds_cma[1].append(bmax)

        return (
         basis_vector, free_parameters_dofs, free_parameters, n_free_parameters, bounds, bounds_cma)

    def find_configurations(self, imposed_parameters, number_max_configurations, number_starts=10, tol=1e-05, starting_point=None):
        basis_vector, free_parameters_dofs, free_parameters, n_free_parameters, bounds, bounds_cma = self._optimization_settings(imposed_parameters)
        geometric_closing_residue = self.geometric_closing_residue_function(basis_vector, free_parameters_dofs)
        starting_points = []
        for istart in range(number_starts):
            if starting_point is None:
                xr0 = [
                 0] * n_free_parameters
                for i, parameter in enumerate(free_parameters):
                    xr0[i] = parameter.random_value()

            else:
                xr0 = [starting_point[i] for i in free_parameters_dofs]
            xr_opt, fopt = cma.fmin(geometric_closing_residue, xr0, 0.2, options={'bounds':bounds_cma, 
             'ftarget':tol, 
             'verbose':-9, 
             'maxiter':2000})[0:2]
            if fopt <= tol:
                found_x = False
                for x in starting_points:
                    equal = True
                    for parameter, xi1, xi2 in zip(free_parameters, x, xr_opt):
                        if not parameter.are_values_equal(xi1, xi2):
                            equal = False
                            break

                    if equal:
                        found_x = True

                xopt = found_x or self.reduced_x_to_full_x(xr_opt, basis_vector, free_parameters_dofs)
                starting_points.append(xopt[:])
                yield xopt
                if len(starting_points) >= number_max_configurations:
                    break

        print('Found {} configurations'.format(len(starting_points)))
        raise NoConfigurationFoundError

    def solve_from_initial_configuration--- This code section failed: ---

 L. 769         0  LOAD_FAST                'initial_parameter_values'
                2  STORE_FAST               'x0'

 L. 770         4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'MovingMechanism.solve_from_initial_configuration.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               10  LOAD_FAST                'steps_imposed_parameters'
               12  LOAD_METHOD              items
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  GET_ITER         
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  STORE_FAST               'step_imposed_parameters'

 L. 772        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _optimization_settings
               26  LOAD_FAST                'step_imposed_parameters'
               28  CALL_METHOD_1         1  '1 positional argument'
               30  UNPACK_SEQUENCE_6     6 
               32  STORE_FAST               'basis_vector'
               34  STORE_FAST               'free_parameters_dofs'
               36  STORE_FAST               'free_parameters'
               38  STORE_FAST               'n_free_parameters'
               40  STORE_FAST               'bounds'
               42  STORE_FAST               'bounds_cma'

 L. 773        44  LOAD_FAST                'self'
               46  LOAD_METHOD              full_x_to_reduced_x
               48  LOAD_FAST                'x0'
               50  LOAD_FAST                'free_parameters_dofs'
               52  CALL_METHOD_2         2  '2 positional arguments'
               54  STORE_FAST               'xr0'

 L. 775        56  LOAD_GLOBAL              len
               58  LOAD_GLOBAL              list
               60  LOAD_FAST                'steps_imposed_parameters'
               62  LOAD_METHOD              values
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  STORE_FAST               'n_steps'

 L. 777        76  LOAD_FAST                'x0'
               78  BUILD_LIST_1          1 
               80  STORE_FAST               'qs'

 L. 779        82  LOAD_CONST               0
               84  STORE_FAST               'number_failed_steps'

 L. 780        86  LOAD_CONST               False
               88  STORE_FAST               'failed_step'

 L. 781     90_92  SETUP_LOOP          450  'to 450'
               94  LOAD_GLOBAL              range
               96  LOAD_FAST                'n_steps'
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  GET_ITER         
          102_104  FOR_ITER            448  'to 448'
              106  STORE_DEREF              'istep'

 L. 782       108  LOAD_CLOSURE             'istep'
              110  BUILD_TUPLE_1         1 
              112  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              114  LOAD_STR                 'MovingMechanism.solve_from_initial_configuration.<locals>.<dictcomp>'
              116  MAKE_FUNCTION_8          'closure'
              118  LOAD_FAST                'steps_imposed_parameters'
              120  LOAD_METHOD              items
              122  CALL_METHOD_0         0  '0 positional arguments'
              124  GET_ITER         
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  STORE_FAST               'step_imposed_parameters'

 L. 786       130  LOAD_FAST                'self'
              132  LOAD_METHOD              _optimization_settings
              134  LOAD_FAST                'step_imposed_parameters'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  UNPACK_SEQUENCE_6     6 
              140  STORE_FAST               'basis_vector'
              142  STORE_FAST               'free_parameters_dofs'
              144  STORE_FAST               'free_parameters'
              146  STORE_FAST               'n_free_parameters'
              148  STORE_FAST               'bounds'
              150  STORE_FAST               'bounds_cma'

 L. 788       152  LOAD_FAST                'self'
              154  LOAD_METHOD              geometric_closing_residue_function
              156  LOAD_FAST                'basis_vector'

 L. 789       158  LOAD_FAST                'free_parameters_dofs'
              160  CALL_METHOD_2         2  '2 positional arguments'
              162  STORE_FAST               'geometric_closing_residue'

 L. 791       164  LOAD_FAST                'n_free_parameters'
              166  LOAD_CONST               0
              168  COMPARE_OP               >
          170_172  POP_JUMP_IF_FALSE   436  'to 436'

 L. 792       174  LOAD_CONST               False
              176  STORE_FAST               'step_converged'

 L. 793       178  LOAD_CONST               1
              180  STORE_FAST               'n_tries_step'

 L. 794       182  SETUP_LOOP          328  'to 328'
              184  LOAD_FAST                'step_converged'
          186_188  POP_JUMP_IF_TRUE    326  'to 326'
              190  LOAD_FAST                'n_tries_step'
              192  LOAD_FAST                'number_step_retries'
              194  COMPARE_OP               <=
          196_198  POP_JUMP_IF_FALSE   326  'to 326'

 L. 795       200  LOAD_GLOBAL              minimize
              202  LOAD_FAST                'geometric_closing_residue'

 L. 796       204  LOAD_GLOBAL              npy
              206  LOAD_METHOD              array
              208  LOAD_FAST                'xr0'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  LOAD_CONST               0.01
              214  LOAD_GLOBAL              npy
              216  LOAD_ATTR                random
              218  LOAD_METHOD              random
              220  LOAD_FAST                'n_free_parameters'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  LOAD_CONST               0.5
              226  BINARY_SUBTRACT  
              228  BINARY_MULTIPLY  
              230  BINARY_ADD       

 L. 797       232  LOAD_CONST               0.1
              234  LOAD_FAST                'tol'
              236  BINARY_MULTIPLY  
              238  LOAD_FAST                'bounds'
              240  LOAD_CONST               ('tol', 'bounds')
              242  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              244  STORE_FAST               'result'

 L. 798       246  LOAD_FAST                'result'
              248  LOAD_ATTR                x
              250  STORE_FAST               'xr_opt'

 L. 799       252  LOAD_FAST                'result'
              254  LOAD_ATTR                fun
              256  STORE_FAST               'fopt'

 L. 800       258  LOAD_FAST                'fopt'
              260  LOAD_FAST                'tol'
              262  COMPARE_OP               >
          264_266  POP_JUMP_IF_FALSE   308  'to 308'

 L. 801       268  LOAD_GLOBAL              cma
              270  LOAD_ATTR                fmin
              272  LOAD_FAST                'geometric_closing_residue'
              274  LOAD_FAST                'xr0'
              276  LOAD_CONST               0.1

 L. 802       278  LOAD_FAST                'bounds_cma'

 L. 804       280  LOAD_CONST               -9

 L. 805       282  LOAD_FAST                'tol'

 L. 806       284  LOAD_CONST               500
              286  LOAD_CONST               ('bounds', 'verbose', 'ftarget', 'maxiter')
              288  BUILD_CONST_KEY_MAP_4     4 
              290  LOAD_CONST               ('options',)
              292  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              294  LOAD_CONST               0
              296  LOAD_CONST               2
              298  BUILD_SLICE_2         2 
              300  BINARY_SUBSCR    
              302  UNPACK_SEQUENCE_2     2 
              304  STORE_FAST               'xr_opt'
              306  STORE_FAST               'fopt'
            308_0  COME_FROM           264  '264'

 L. 807       308  LOAD_FAST                'n_tries_step'
              310  LOAD_CONST               1
              312  INPLACE_ADD      
              314  STORE_FAST               'n_tries_step'

 L. 808       316  LOAD_FAST                'fopt'
              318  LOAD_FAST                'tol'
              320  COMPARE_OP               <
              322  STORE_FAST               'step_converged'
              324  JUMP_BACK           184  'to 184'
            326_0  COME_FROM           196  '196'
            326_1  COME_FROM           186  '186'
              326  POP_BLOCK        
            328_0  COME_FROM_LOOP      182  '182'

 L. 809       328  LOAD_FAST                'step_converged'
          330_332  POP_JUMP_IF_FALSE   380  'to 380'

 L. 810       334  LOAD_FAST                'xr_opt'
              336  LOAD_CONST               None
              338  LOAD_CONST               None
              340  BUILD_SLICE_2         2 
              342  BINARY_SUBSCR    
              344  STORE_FAST               'xr0'

 L. 811       346  LOAD_FAST                'self'
              348  LOAD_METHOD              reduced_x_to_full_x
              350  LOAD_FAST                'xr_opt'
              352  LOAD_FAST                'basis_vector'
              354  LOAD_FAST                'free_parameters_dofs'
              356  CALL_METHOD_3         3  '3 positional arguments'
              358  STORE_FAST               'x'

 L. 813       360  LOAD_FAST                'qs'
              362  LOAD_METHOD              append
              364  LOAD_FAST                'x'
              366  LOAD_CONST               None
              368  LOAD_CONST               None
              370  BUILD_SLICE_2         2 
              372  BINARY_SUBSCR    
              374  CALL_METHOD_1         1  '1 positional argument'
              376  POP_TOP          
              378  JUMP_FORWARD        434  'to 434'
            380_0  COME_FROM           330  '330'

 L. 815       380  LOAD_GLOBAL              print
              382  LOAD_STR                 '@istep {}: residue: {}'
              384  LOAD_METHOD              format
              386  LOAD_DEREF               'istep'
              388  LOAD_FAST                'fopt'
              390  CALL_METHOD_2         2  '2 positional arguments'
              392  CALL_FUNCTION_1       1  '1 positional argument'
              394  POP_TOP          

 L. 816       396  LOAD_FAST                'number_failed_steps'
              398  LOAD_CONST               1
              400  INPLACE_ADD      
              402  STORE_FAST               'number_failed_steps'

 L. 817       404  LOAD_FAST                'number_failed_steps'
              406  LOAD_FAST                'max_failed_steps'
              408  COMPARE_OP               >=
          410_412  POP_JUMP_IF_FALSE   446  'to 446'

 L. 818       414  LOAD_GLOBAL              print
              416  LOAD_STR                 'Failed {} steps, stopping configuration computation'
              418  LOAD_METHOD              format
              420  LOAD_FAST                'max_failed_steps'
              422  CALL_METHOD_1         1  '1 positional argument'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  POP_TOP          

 L. 819       428  LOAD_CONST               True
              430  STORE_FAST               'failed_step'

 L. 820       432  BREAK_LOOP       
            434_0  COME_FROM           378  '378'
              434  JUMP_BACK           102  'to 102'
            436_0  COME_FROM           170  '170'

 L. 824       436  LOAD_FAST                'qs'
              438  LOAD_METHOD              append
              440  LOAD_FAST                'basis_vector'
              442  CALL_METHOD_1         1  '1 positional argument'
              444  POP_TOP          
            446_0  COME_FROM           410  '410'
              446  JUMP_BACK           102  'to 102'
              448  POP_BLOCK        
            450_0  COME_FROM_LOOP       90  '90'

 L. 825       450  LOAD_FAST                'failed_step'
          452_454  POP_JUMP_IF_TRUE    468  'to 468'

 L. 826       456  LOAD_GLOBAL              MechanismConfigurations
              458  LOAD_FAST                'self'
              460  LOAD_FAST                'steps_imposed_parameters'
              462  LOAD_FAST                'qs'
              464  CALL_FUNCTION_3       3  '3 positional arguments'
              466  RETURN_VALUE     
            468_0  COME_FROM           452  '452'

Parse error at or near `POP_BLOCK' instruction at offset 448


def istep_from_value_on_list(list_, value):
    for ipoint, (point1, point2) in enumerate(zip(list_[:-1], list_[1:])):
        interval = sorted((point1, point2))
        if interval[0] <= value:
            if value <= interval[1]:
                alpha = (value - point1) / (point2 - point1)
                if alpha < 0 or alpha > 1:
                    raise ValueError
            return ipoint + alpha

    values = [p for p in list_]
    min_values = min(values)
    max_values = max(values)
    raise ValueError('Specified value not found in list_: {} not in [{}, {}]'.format(value, min_values, max_values))


def istep_from_value_on_trajectory(trajectory, value, axis):
    for ipoint, (point1, point2) in enumerate(zip(trajectory[:-1], trajectory[1:])):
        interval = sorted((point1[axis], point2[axis]))
        if interval[0] <= value:
            if value <= interval[1]:
                alpha = (value - point1[axis]) / (point2[axis] - point1[axis])
                if alpha < 0 or alpha > 1:
                    raise ValueError
            return ipoint + alpha

    values = [p[axis] for p in trajectory]
    min_values = min(values)
    max_values = max(values)
    raise ValueError('Specified value not found in trajectory: {} not in [{}, {}]'.format(value, min_values, max_values))


def point_from_istep_on_trajectory(trajectory, istep):
    istep1 = int(istep)
    if istep1 == istep:
        return trajectory[int(istep)]
    alpha = istep - istep1
    point1 = trajectory[istep1]
    point2 = trajectory[(istep1 + 1)]
    return (1 - alpha) * point1 + alpha * point2


def trajectory_point_from_value(trajectory, value, axis):
    for ipoint, (point1, point2) in enumerate(zip(trajectory[:-1], trajectory[1:])):
        interval = sorted((point1[axis], point2[axis]))
        if interval[0] <= value and value < interval[1]:
            alpha = (value - point1[axis]) / (point2[axis] - point1[axis])
            return (1 - alpha) * point1 + alpha * point2


def trajectory_derivative(trajectory, istep, delta_istep):
    istep1 = istep - 0.5 * delta_istep
    istep2 = istep + 0.5 * delta_istep
    if istep1 < 0:
        istep1 = 0
        istep2 = delta_istep
    if istep2 > len(trajectory) - 1:
        istep2 = len(trajectory) - 1
        istep1 = istep2 - delta_istep
        if istep1 < 0:
            raise ValueError('Delta istep is too large!')
    point1 = point_from_istep_on_trajectory(trajectory, istep1)
    point2 = point_from_istep_on_trajectory(trajectory, istep2)
    return point2 - point1


class MechanismConfigurations(DessiaObject):

    def __init__(self, mechanism, steps_imposed_parameters, steps):
        number_steps = len(steps)
        DessiaObject.__init__(self, mechanism=mechanism,
          steps_imposed_parameters=steps_imposed_parameters,
          steps=steps,
          number_steps=number_steps)
        if not self.is_valid():
            raise ValueError
        self.trajectories = {}

    def is_valid(self):
        nparam_mechanism = len(self.mechanism.kinematic_parameters_mapping)
        for istep, step in enumerate(self.steps):
            if len(step) != nparam_mechanism:
                print('Step n°{} has incorrect length'.format(istep))
                return False

        return True

    def opened_linkages_residue(self):
        residues = []
        for step in self.steps:
            residues.append(self.mechanism.opened_linkages_residue(step))

        return residues

    def interpolate_step(self, istep):
        """
        :param istep: can be a float
        """
        istep1 = int(istep)
        alpha = istep - istep1
        if alpha == 0.0:
            return self.steps[istep1]
        return [(1 - alpha) * s1 + alpha * s2 for s1, s2 in zip(self.steps[istep1], self.steps[(istep1 + 1)])]

    def plot_kinematic_parameters(self, linkage1, kinematic_parameter1, linkage2, kinematic_parameter2):
        x = []
        y = []
        dof1 = self.mechanism.kinematic_parameters_mapping[(linkage1, kinematic_parameter1)]
        dof2 = self.mechanism.kinematic_parameters_mapping[(linkage2, kinematic_parameter2)]
        for step in self.steps:
            x.append(step[dof1])
            y.append(step[dof2])

        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o')
        ax.set_xlabel('Parameter {} of linkage {}'.format(kinematic_parameter1 + 1, linkage1.name))
        ax.set_ylabel('Parameter {} of linkage {}'.format(kinematic_parameter2 + 1, linkage2.name))
        ax.grid()
        return (fig, ax)

    def trajectory(self, point, part, reference_part):
        if (
         point, part, reference_part) in self.trajectories:
            return self.trajectories[(point, part, reference_part)]
        trajectory = []
        for step in self.steps:
            frame1 = self.mechanism.part_global_frame(part, step)
            frame2 = self.mechanism.part_global_frame(reference_part, step)
            frame = frame1 - frame2
            trajectory.append(frame.OldCoordinates(point))

        self.trajectories[(point, part, reference_part)] = trajectory
        return trajectory

    def plot2D_trajectory(self, point, part, reference_part, x=vm.X3D, y=vm.Y3D, equal_aspect=True):
        xt = []
        yt = []
        for traj_point in self.trajectory(point, part, reference_part):
            xp, yp = traj_point.PlaneProjection2D(x, y)
            xt.append(xp)
            yt.append(yp)

        fig, ax = plt.subplots()
        ax.plot(xt, yt, marker='o')
        ax.grid()
        ax.set_xlabel(str(x))
        ax.set_ylabel(str(y))
        ax.set_title('Trajectory of point {} on part {} relatively to part {}'.format(str(point), part.name, reference_part.name))
        if equal_aspect:
            ax.set_aspect('equal')
        return (fig, ax)

    def plot_trajectory(self, point, part, reference_part, equal_aspect=True):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        xt = []
        yt = []
        zt = []
        for point in self.trajectory(point, part, reference_part):
            xp, yp, zp = point
            xt.append(xp)
            yt.append(yp)
            zt.append(zp)

        ax.plot(xt, yt, zt, marker='o')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Trajectory of point {} on part {} relatively to part {}'.format(str(point), part.name, reference_part.name))
        if equal_aspect:
            ax.set_aspect('equal')
        return (fig, ax)

    def part_local_point_global_speed(self, part, point, istep):
        """

        """
        if istep < 0 or istep > self.number_steps - 1:
            raise ValueError('istep outside of bounds: {}'.format(istep))
        else:
            if istep < 0.5:
                frame1 = self.mechanism.part_global_frame(part, self.steps[0])
                frame2 = self.mechanism.part_global_frame(part, self.steps[1])
                frame3 = self.mechanism.part_global_frame(part, self.steps[2])
                p1 = frame1.OldCoordinates(point)
                p2 = frame2.OldCoordinates(point)
                p3 = frame3.OldCoordinates(point)
                v1 = p2 - p1
                v2 = p3 - p2
                alpha = istep - 0.5
                return (1 - alpha) * v1 + alpha * v2
            if istep > self.number_steps - 1.5:
                i1 = int(istep - 0.5)
                frame1 = self.mechanism.part_global_frame(part, self.steps[(-3)])
                frame2 = self.mechanism.part_global_frame(part, self.steps[(-2)])
                frame3 = self.mechanism.part_global_frame(part, self.steps[(-1)])
                p1 = frame1.OldCoordinates(point)
                p2 = frame2.OldCoordinates(point)
                p3 = frame3.OldCoordinates(point)
                v1 = p2 - p1
                v2 = p3 - p2
                alpha = istep - (self.number_steps - 2.5)
                return (1 - alpha) * v1 + alpha * v2
            int_istep = int(istep)
            if int_istep + 0.5 == istep:
                frame1 = self.mechanism.part_global_frame(part, self.steps[int_istep])
                frame2 = self.mechanism.part_global_frame(part, self.steps[(int_istep + 1)])
                p1 = frame1.OldCoordinates(point)
                p2 = frame2.OldCoordinates(point)
                return p2 - p1
            i1 = int(istep - 0.5)
            frame1 = self.mechanism.part_global_frame(part, self.steps[i1])
            frame2 = self.mechanism.part_global_frame(part, self.steps[(i1 + 1)])
            frame3 = self.mechanism.part_global_frame(part, self.steps[(i1 + 2)])
            p1 = frame1.OldCoordinates(point)
            p2 = frame2.OldCoordinates(point)
            p3 = frame3.OldCoordinates(point)
            v1 = p2 - p1
            v2 = p3 - p2
            alpha = istep - i1 - 0.5
            return (1 - alpha) * v1 + alpha * v2

    def part_global_rotation_vector(self, part, istep):
        step = self.interpolate_step(istep)
        frame = self.mechanism.part_global_frame(part, step)
        point1 = vm.O3D
        point1_speed = self.part_local_point_global_speed(part, point1, istep)
        for point2 in [vm.X3D, vm.Y3D, vm.Z3D]:
            point2_speed = self.part_local_point_global_speed(part, point2, istep)
            delta_speeds = point2_speed - point1_speed
            if not math.isclose((delta_speeds.Norm()), 0, abs_tol=1e-08):
                break

        p21 = frame.OldCoordinates(point2) - frame.OldCoordinates(point1)
        R = delta_speeds.Cross(p21)
        return R

    def part_instant_rotation_global_axis_point(self, part, istep):
        w = self.part_global_rotation_vector(part, istep)
        w2 = w.Dot(w)
        if math.isclose(w2, 0, abs_tol=1e-08):
            return
        step = self.interpolate_step(istep)
        frame = self.mechanism.part_global_frame(part, step)
        for point in [vm.O3D, 0.1 * vm.X3D, 0.1 * vm.Y3D, 0.1 * vm.Z3D]:
            vp = self.part_local_point_global_speed(part, point, istep)
            if not math.isclose((vp.Norm()), 0, abs_tol=1e-06):
                return frame.OldCoordinates(point) - w.Cross(vp) / w2

        raise ValueError

    def plot2D(self, x=vm.X3D, y=vm.Y3D, isteps=None, plot_frames=False, plot_rotation_axis=False):
        fig, ax = plt.subplots()
        np = len(self.mechanism.parts)
        colors = {p:hsv_to_rgb((ip / np, 0.78, 0.87)) for ip, p in enumerate(self.mechanism.parts)}
        colors[self.mechanism.ground] = (0, 0, 0)
        if isteps == None:
            steps = self.steps[:]
        else:
            steps = [self.steps[i] for i in isteps]
        for istep, step in enumerate(steps):
            linkage_positions = {}
            part_frames = {}
            for linkage in self.mechanism.linkages:
                if linkage.positions_require_kinematic_parameters:
                    ql = self.mechanism.extract_linkage_parameters_values(linkage, step)
                else:
                    ql = []
                part1_frame = self.mechanism.part_global_frame(linkage.part1, step)
                part_frames[linkage.part1] = part1_frame
                linkage_position1 = part1_frame.OldCoordinates(linkage.part1_position_function(ql))
                linkage_position1_2D = linkage_position1.PlaneProjection2D(x, y)
                part2_frame = self.mechanism.part_global_frame(linkage.part2, step)
                part_frames[linkage.part2] = part2_frame
                linkage_position2 = part2_frame.OldCoordinates(linkage.part2_position_function(ql))
                linkage_position2_2D = linkage_position1.PlaneProjection2D(x, y)
                if linkage_position1 != linkage_position2:
                    (ax.text)(*linkage_position1_2D, *(linkage.name + ' position1',))
                    (ax.text)(*linkage_position2_2D, *(linkage.name + ' position2',))
                    error = linkage_position2_2D - linkage_position1_2D
                    ax.add_patch(Arrow(*linkage_position1_2D, *error, *(0.05, )))
                else:
                    if istep == 0:
                        (ax.text)(*linkage_position1_2D, *(linkage.name,))
                    linkage_positions[(linkage, linkage.part1)] = linkage_position1
                    linkage_positions[(linkage, linkage.part2)] = linkage_position2

            part_linkages = self.mechanism.part_linkages()
            del part_linkages[self.mechanism.ground]
            for ipart, (part, linkages) in enumerate(part_linkages.items()):
                points = []
                for linkage in linkages:
                    points.append(linkage_positions[(linkage, part)])

                points.extend([part_frames[part].OldCoordinates(p) for p in part.interest_points])
                xm, ym = vm.Point3D.mean_point(points).PlaneProjection2D(x, y).vector
                if istep == 0:
                    ax.text(xm, ym, (part.name + ' step 0'), ha='center',
                      va='center',
                      bbox=dict(boxstyle='square', ec=(colors[part]),
                      fc=(1.0, 1, 1)))
                else:
                    if ipart == 0:
                        ax.text(xm, ym, ('step {}'.format(istep)), ha='center',
                          va='center',
                          bbox=dict(boxstyle='square', ec=(colors[part]),
                          fc=(1.0, 1, 1)))
                    for line in Part.wireframe_lines(points):
                        line.MPLPlot2D(x, y, ax, color=(colors[part]), width=5)

                    part_frame = self.mechanism.part_global_frame(part, step)
                    for point in part.interest_points:
                        x1, y1 = part_frame.OldCoordinates(point).PlaneProjection2D(x, y)
                        ax.plot([x1, xm], [y1, ym], color=(colors[part]))

                    if plot_frames:
                        part_frame = self.mechanism.part_global_frame(part, step)
                        part_frame.plot2d(x=x, y=y, ax=ax)
                if plot_rotation_axis:
                    axis = self.part_global_rotation_vector(part, istep)
                    point = self.part_instant_rotation_global_axis_point(part, istep)
                    if point is not None:
                        axis.Normalize()
                        line = vm.Line3D(point - axis, point + axis)
                        line.PlaneProjection2D(x, y).MPLPlot(ax=ax, color=(colors[part]), dashed=True)

        ax.set_aspect('equal')
        ax.set_xlabel(str(x))
        ax.set_ylabel(str(y))
        ax.margins(0.1)

    def babylonjs(self, page='gm_babylonjs', plot_frames=False, plot_trajectories=True, plot_instant_rotation_axis=False, use_cdn=False):
        page += '.html'
        env = Environment(loader=(PackageLoader('genmechanics', 'templates')), autoescape=(select_autoescape(['html', 'xml'])))
        template = env.get_template('babylon.html')
        np = len(self.mechanism.parts)
        colors = {p:hsv_to_rgb((ip / np, 0.78, 0.87)) for ip, p in enumerate(self.mechanism.parts)}
        part_points = {p:[] for p in self.mechanism.parts}
        part_points[self.mechanism.ground] = []
        for part, linkages in self.mechanism.part_linkages().items():
            for linkage in linkages:
                if linkage.positions_require_kinematic_parameters:
                    ql = self.mechanism.extract_linkage_parameters_values(linkage, self.steps[0])
                else:
                    ql = []
                if part == linkage.part1:
                    linkage_position = linkage.part1_position_function(ql)
                else:
                    linkage_position = linkage.part2_position_function(ql)
                part_points[part].append(linkage_position)

            for point in part.interest_points:
                part_points[part].append(point)

        meshes_string = 'var parts_parent = [];\n'
        for part in self.mechanism.parts:
            meshes_string += 'var part_children = [];\n'
            lines = part.wireframe_lines(part_points[part])
            meshes_string += lines[0].babylon_script(name='part_parent', color=(colors[part]))
            meshes_string += 'parts_parent.push(part_parent);\n'
            for l in lines[1:]:
                meshes_string += l.Babylon(color=(colors[part]), parent='part_parent')

            if plot_frames:
                meshes_string += vm.OXYZ.babylonjs(parent='part_parent', size=0.1)

        if plot_instant_rotation_axis:
            for part in self.mechanism.parts:
                line = vm.LineSegment3D(-0.5 * vm.X3D, 0.5 * vm.X3D)
                meshes_string += line.babylon_script(name='rotation_axis', color=(colors[part]), type_='dashed')
                meshes_string += 'parts_parent.push(rotation_axis);\n'

        linkages_string = ''
        for linkage in self.mechanism.linkages:
            if linkage not in self.mechanism.opened_linkages:
                ql = self.mechanism.extract_linkage_parameters_values(linkage, self.steps[0])
            else:
                ql = []
            if linkage.part1 in self.mechanism.parts:
                part1_parent = 'parts_parent[{}]'.format(self.mechanism.parts.index(linkage.part1))
            else:
                part1_parent = None
            if linkage.part2 in self.mechanism.parts:
                part2_parent = 'parts_parent[{}]'.format(self.mechanism.parts.index(linkage.part2))
            else:
                part2_parent = None
            linkages_string += linkage.babylonjs(ql, part1_parent=part1_parent,
              part2_parent=part2_parent)

        positions = []
        orientations = []
        linkage_positions = []
        for istep, step in enumerate(self.steps):
            step_positions = []
            step_orientations = []
            step_linkage_positions = []
            for part in self.mechanism.parts:
                frame = round(self.mechanism.part_global_frame(part, step))
                step_positions.append(list(frame.origin))
                step_orientations.append([list(frame.u),
                 list(frame.v),
                 list(frame.w)])

            if plot_instant_rotation_axis:
                for part in self.mechanism.parts:
                    axis_point = self.part_instant_rotation_global_axis_point(part, istep)
                    if axis_point is None:
                        u = vm.X3D.copy()
                        v = vm.Y3D.copy()
                        w = vm.Z3D.copy()
                        axis_point = vm.Point3D((100, 100, 100))
                    else:
                        u = self.part_global_rotation_vector(part, istep)
                        u.Normalize()
                        v = u.RandomUnitNormalVector()
                        w = u.Cross(v)
                    step_positions.append(list(axis_point))
                    step_orientations.append([list(u),
                     list(v),
                     list(w)])

            for linkage in self.mechanism.linkages:
                step_linkage_positions.append(list(self.mechanism.linkage_global_position(linkage, step)))

            positions.append(step_positions)
            orientations.append(step_orientations)
            linkage_positions.append(step_linkage_positions)

        trajectories = []
        if plot_trajectories:
            for trajectory in self.trajectories.values():
                trajectories.append([list(p) for p in trajectory])

        script = template.render(center=(0, 0, 0), length=1.0,
          meshes_string=meshes_string,
          linkages_string=linkages_string,
          positions=positions,
          orientations=orientations,
          linkage_positions=linkage_positions,
          trajectories=trajectories,
          use_cdn=use_cdn)
        with open(page, 'w') as (file):
            file.write(script)
        webbrowser.open('file://' + os.path.realpath(page))
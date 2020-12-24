# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\abstractComponent.py
# Compiled at: 2014-12-03 13:11:45
# Size of source mod 2**32: 8914 bytes
from collections import namedtuple
from maverig.data.components.utils.dataObject import Data, ObjectDict

class ElementError(Exception):

    def __init__(self, elem, text):
        self.elem = elem
        self.text = text
        print('Error: %s' % self.text)

    def __str__(self):
        output_text = self.text
        output_text += '\n    parameters of %s:' % self.elem.elem_id
        for param in self.elem.params.values():
            output_text += '\n        %s : %s' % (param.name, str(param.value))

        return output_text


ElemPort = namedtuple('ElemPort', 'elem_id, port')

class Parameter(Data):
    public = True
    name = None
    description = None
    data_type = None
    accepted_values = None
    shared_values = []
    value = None


class Attribute(Data):
    name = None
    description = None
    data_type = 'float'
    unit = None
    unit_description = None
    shared_values = []
    values = []


class Simulator(Data):
    __doc__ = ' simulator description: how to start mosaik simulator '
    name = None
    starter = None
    address = None
    params = dict()

    def as_tuple(self):
        hashable_sim_params = tuple(sorted(self.params.items()))
        return tuple([self.name, self.starter, self.address, hashable_sim_params])

    def __hash__(self):
        """ apply hashing on params and name for simulator collections """
        return hash(self.as_tuple())

    def __eq__(self, other):
        if not isinstance(other, Simulator):
            return False
        return self.as_tuple() == other.as_tuple()

    def prepare_params(self, **global_params):
        """ fill simulator params with global and element params """
        for param_name in self.params:
            if param_name in global_params:
                self.params[param_name] = global_params[param_name]
                continue

    def generate_parent_elems(self, elements, elem):
        """ generate simulator specific parent elements """
        return []


class AcceptedDocking(Data):
    to_component = None
    to_port = 0
    from_attr = None
    to_attr = None

    def can_dock(self, to_elem, to_port):
        return isinstance(to_elem, self.to_component) and to_port == self.to_port


class DockingPort(Data):
    pos = None
    dockings_out = dict()
    dockings_in = dict()
    accepted_dockings_out = []

    def can_dock(self, to_elem, to_port):
        return any([ad.can_dock(to_elem, to_port) for ad in self.accepted_dockings_out])


class Component(Data):
    __doc__ = ' base class for any energy component\n\n    derived classes can be instantiated in order to create elements (component instances)\n    one element is a representation of one real power plant or grid element like a branch, transformer or bus\n    '
    name = None
    description = None
    simulator = None
    drawing_mode = None
    icon = None
    category = None
    params = ObjectDict()
    attrs = ObjectDict()
    elem_id = None
    mosaik_full_id = None
    mosaik_entity = None
    mosaik_simulator = None
    docking_ports = [
     DockingPort()]

    def elem_ports(self):
        return [ElemPort(self.elem_id, port) for port, _ in enumerate(self.docking_ports)]

    def prepare_params(self, **global_params):
        """ fill dependent needed params of element and it's simulator description for mosaik """
        for param_name, value in global_params.items():
            if param_name in self.params:
                self.params[param_name].value = value
                continue

        if self.simulator:
            sim_global_params = {param_name:param.value for param_name, param in self.params.items()}
            sim_global_params.update(global_params)
            self.simulator.prepare_params(**sim_global_params)
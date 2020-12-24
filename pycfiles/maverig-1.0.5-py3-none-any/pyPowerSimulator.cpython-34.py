# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\simulators\pyPowerSimulator.py
# Compiled at: 2014-12-11 18:15:32
# Size of source mod 2**32: 770 bytes
from maverig.data.components.abstractComponent import Simulator, Component, Parameter
from maverig.data.components.utils import pyPowerSerializer
from maverig.data.components.utils.dataObject import ObjectDict

class GridFile(Parameter):
    name = 'gridfile'


class Grid(Component):
    name = 'Grid'
    elem_id = 'Grid_0'
    params = ObjectDict([GridFile])


class PyPower(Simulator):
    name = 'PyPower'
    starter = 'python'
    address = 'mosaik_pypower.mosaik:PyPower'
    params = {'step_size': 900}

    def generate_parent_elems(self, elements, elem):
        grid = Grid()
        py_power_serializer = pyPowerSerializer.PyPowerSerializer()
        grid.params['gridfile'].value = py_power_serializer.serialize_to_file(elements)
        return [grid]
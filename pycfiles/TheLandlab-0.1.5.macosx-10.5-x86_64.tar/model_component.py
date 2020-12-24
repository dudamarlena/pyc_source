# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/core/model_component.py
# Compiled at: 2015-02-11 19:25:27


class Component(object):
    _input_var_names = set()
    _output_var_names = set()
    _var_units = dict()

    def __init__(self, grid, map_vars={}):
        self._grid = grid
        for location, vars in map_vars.items():
            for dest, src in vars.items():
                grid.add_field(location, dest, grid.field_values(location, src))

    @property
    def input_var_names(self):
        return self._input_var_names

    @property
    def output_var_names(self):
        return self._output_var_names

    @property
    def name(self):
        return self._name

    @property
    def units(self):
        return self._var_units

    @property
    def var_units(self):
        return self._var_units

    @property
    def var_definitions(self):
        return self._var_defs

    @property
    def var_mapping(self):
        """var_mapping
        This is 'node', 'cell', 'active_link', etc.
        """
        return self._var_mapping

    @property
    def shape(self):
        return self.grid._shape

    @property
    def grid(self):
        return self._grid

    @property
    def coords(self):
        return (self.grid.node_x, self.grid.node_y)

    def imshow(self, name, **kwds):
        self._grid.imshow(name, **kwds)
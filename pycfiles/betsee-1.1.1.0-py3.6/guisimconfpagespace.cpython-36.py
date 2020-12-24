# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/page/space/guisimconfpagespace.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2718 bytes
"""
**Spatial simulation configuration pager** (i.e., :mod:`PySide2`-based
controller for stack widget pages specific to spatial settings) functionality.
"""
from PySide2.QtWidgets import QMainWindow
from betse.science.parameters import Parameters
from betse.science.enum.enumconf import CellLatticeType
from betse.util.type.types import type_check
from betsee.util.widget.abc.control.guictlpageabc import QBetseePagerABC

class QBetseeSimConfPagerSpace(QBetseePagerABC):
    __doc__ = '\n    **Spatial simulation configuration pager** (i.e., :mod:`PySide2`-based\n    controller connecting all editable widgets of the spatial stack widget page\n    with corresponding settings of the current simulation configuration).\n    '

    @type_check
    def init(self, main_window):
        super().init(main_window)
        sim_conf = main_window.sim_conf
        main_window.sim_conf_space_intra_cell_radius.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.cell_radius))
        main_window.sim_conf_space_intra_lattice_disorder.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.cell_lattice_disorder))
        main_window.sim_conf_space_intra_lattice_type.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.cell_lattice_type),
          enum_member_to_widget_value={CellLatticeType.HEX: main_window.sim_conf_space_intra_lattice_hex, 
         
         CellLatticeType.SQUARE: main_window.sim_conf_space_intra_lattice_square})
        main_window.sim_conf_space_extra_grid_size.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.grid_size))
        main_window.sim_conf_space_extra_is_ecm.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.is_ecm))
        main_window.sim_conf_space_extra_world_len.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.world_len))
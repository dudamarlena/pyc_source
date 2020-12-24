# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/page/export/guisimconfpageexport.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 7385 bytes
"""
**Export simulation configuration pager** (i.e., :mod:`PySide2`-based
controller for stack widget pages specific to export settings) functionality.
"""
from PySide2.QtWidgets import QMainWindow
from betse.science.parameters import Parameters
from betse.science.config.export.visual.confexpvisual import SimConfExportVisual
from betse.lib.matplotlib import mplcolormap
from betse.util.type.types import type_check
from betsee.util.widget.abc.control.guictlpageabc import QBetseePagerABC

class QBetseeSimConfPagerExport(QBetseePagerABC):
    __doc__ = '\n    **Export simulation configuration pager** (i.e., :mod:`PySide2`-based\n    controller connecting all editable widgets of the export stack widget page\n    with corresponding settings of the current simulation configuration).\n    '

    @type_check
    def init(self, main_window):
        super().init(main_window)
        sim_conf_visual = main_window.sim_conf.p.visual
        main_window.sim_conf_exp_is_show_cell_indices.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(SimConfExportVisual.is_show_cell_indices),
          sim_conf_alias_parent=sim_conf_visual)
        main_window.sim_conf_exp_single_cell_index.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(SimConfExportVisual.single_cell_index),
          sim_conf_alias_parent=sim_conf_visual)
        colormap_names = mplcolormap.iter_colormap_names()
        main_window.sim_conf_exp_colormap_diverging.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(Parameters.colormap_diverging_name),
          items_iconless_text=colormap_names)
        main_window.sim_conf_exp_colormap_sequential.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(Parameters.colormap_sequential_name),
          items_iconless_text=colormap_names)
        main_window.sim_conf_exp_colormap_gj.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(Parameters.colormap_gj_name),
          items_iconless_text=colormap_names)
        main_window.sim_conf_exp_colormap_grn.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(Parameters.colormap_grn_name),
          items_iconless_text=colormap_names)
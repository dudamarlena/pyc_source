# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/page/export/guisimconfpageexpplot.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 6430 bytes
"""
**Plot pager** (i.e., :mod:`PySide2`-based controller for stack widget pages
specific to plot exports) functionality.
"""
from betse.science.pipe.export.pipeexpabc import SimPipeExportABC
from betse.science.pipe.export.plot.pipeexpplotcell import SimPipeExportPlotCell
from betse.science.pipe.export.plot.pipeexpplotcells import SimPipeExportPlotCells
from betsee.gui.simconf.stack.page.export.guisimconfpageexpabc import QBetseeSimConfPagerExportABC
from betsee.util.widget.abc.control.guictlpageabc import QBetseePagerABC

class QBetseeSimConfPagerPlot(QBetseePagerABC):
    __doc__ = '\n    **Plot exports simulation configuration pager** (i.e., :mod:`PySide2`-based\n    controller connecting all editable widgets of the stack widget page for\n    *all* plot exports with corresponding settings of the current simulation\n    configuration).\n    '


class QBetseeSimConfPagerPlotCell(QBetseePagerABC):
    __doc__ = '\n    **Single cell plot exports simulation configuration pager** (i.e.,\n    :mod:`PySide2`-based controller connecting all editable widgets of the\n    stack widget page for *all* single cell plot exports with corresponding\n    settings of the current simulation configuration).\n    '


class QBetseeSimConfPagerPlotCellExport(QBetseeSimConfPagerExportABC):
    __doc__ = '\n    **Single cell plot export pager** (i.e., :mod:`PySide2`-based controller\n    connecting all editable widgets of the stack widget page for the currently\n    selected single cell plot export with corresponding settings of a\n    YAML-backed list item of the currently open simulation configuration).\n\n    **This controller implements the well-known flyweight design pattern.**\n    Specifically, this single controller is shared between the zero or more\n    plot exports configured for this simulation and hence *cannot* be\n    implicitly initialized at application startup. Instead, this controller is\n    explicitly reinitialized in an on-the-fly manner immediately before this\n    page is displayed to edit a single such export.\n    '

    @property
    def _pipe_cls(self) -> SimPipeExportABC:
        return SimPipeExportPlotCell

    @property
    def _widget_name_prefix(self) -> str:
        return 'sim_conf_plot_cell_item_'

    @property
    def _yaml_list(self) -> str:
        return self._p.plot.plots_cell_after_sim


class QBetseeSimConfPagerPlotCells(QBetseePagerABC):
    __doc__ = '\n    **Cell cluster plot exports simulation configuration pager** (i.e.,\n    :mod:`PySide2`-based controller connecting all editable widgets of the\n    stack widget page for *all* cell cluster plot exports with corresponding\n    settings of the current simulation configuration).\n    '


class QBetseeSimConfPagerPlotCellsExport(QBetseeSimConfPagerExportABC):
    __doc__ = '\n    **Cell cluster plot export pager** (i.e., :mod:`PySide2`-based controller\n    connecting all editable widgets of the stack widget page for the currently\n    selected cell cluster plot export with corresponding settings of a\n    YAML-backed list item of the currently open simulation configuration).\n\n    **This controller implements the well-known flyweight design pattern.**\n    Specifically, this single controller is shared between the zero or more\n    plot exports configured for this simulation and hence *cannot* be\n    implicitly initialized at application startup. Instead, this controller is\n    explicitly reinitialized in an on-the-fly manner immediately before this\n    page is displayed to edit a single such export.\n    '

    @property
    def _pipe_cls(self) -> SimPipeExportABC:
        return SimPipeExportPlotCells

    @property
    def _widget_name_prefix(self) -> str:
        return 'sim_conf_plot_cells_item_'

    @property
    def _yaml_list(self) -> str:
        return self._p.plot.plots_cells_after_sim
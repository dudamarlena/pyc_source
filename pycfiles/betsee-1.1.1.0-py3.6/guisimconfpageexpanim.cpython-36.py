# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/page/export/guisimconfpageexpanim.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 4065 bytes
"""
**Animation pager** (i.e., :mod:`PySide2`-based controller for stack widget
pages specific to animation exports) functionality.
"""
from betse.science.pipe.export.pipeexpabc import SimPipeExportABC
from betse.science.pipe.export.pipeexpanim import SimPipeExportAnimCells
from betsee.gui.simconf.stack.page.export.guisimconfpageexpabc import QBetseeSimConfPagerExportABC
from betsee.util.widget.abc.control.guictlpageabc import QBetseePagerABC

class QBetseeSimConfPagerAnim(QBetseePagerABC):
    __doc__ = '\n    **Animation exports simulation configuration pager** (i.e.,\n    :mod:`PySide2`-based controller connecting all editable widgets of the\n    stack widget page for *all* animation exports with corresponding settings\n    of the current simulation configuration).\n    '


class QBetseeSimConfPagerAnimCells(QBetseePagerABC):
    __doc__ = '\n    **Cell cluster animation exports simulation configuration pager** (i.e.,\n    :mod:`PySide2`-based controller connecting all editable widgets of the\n    stack widget page for *all* cell cluster animation exports with\n    corresponding settings of the current simulation configuration).\n    '


class QBetseeSimConfPagerAnimCellsExport(QBetseeSimConfPagerExportABC):
    __doc__ = '\n    **Cell cluster animation export pager** (i.e., :mod:`PySide2`-based\n    controller connecting all editable widgets of the stack widget page for the\n    currently selected cell cluster animation export with corresponding\n    settings of a YAML-backed list item of the currently open simulation\n    configuration).\n\n    **This controller implements the well-known flyweight design pattern.**\n    Specifically, this single controller is shared between the zero or more\n    animation exports configured for this simulation and hence *cannot* be\n    implicitly initialized at application startup. Instead, this controller is\n    explicitly reinitialized in an on-the-fly manner immediately before this\n    page is displayed to edit a single such export.\n    '

    @property
    def _pipe_cls(self) -> SimPipeExportABC:
        return SimPipeExportAnimCells

    @property
    def _widget_name_prefix(self) -> str:
        return 'sim_conf_anim_cells_item_'

    @property
    def _yaml_list(self) -> str:
        return self._p.anim.anims_after_sim
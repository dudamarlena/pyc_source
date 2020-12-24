# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/page/export/guisimconfpageexpcsv.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 3081 bytes
"""
**CSV export pager** (i.e., :mod:`PySide2`-based controller for stack widget
pages specific to comma-separated value (CSV) exports) functionality.
"""
from betse.science.pipe.export.pipeexpabc import SimPipeExportABC
from betse.science.pipe.export.pipeexpcsv import SimPipeExportCSVs
from betsee.gui.simconf.stack.page.export.guisimconfpageexpabc import QBetseeSimConfPagerExportABC
from betsee.util.widget.abc.control.guictlpageabc import QBetseePagerABC

class QBetseeSimConfPagerCSV(QBetseePagerABC):
    __doc__ = '\n    **CSV exports simulation configuration pager** (i.e., :mod:`PySide2`-based\n    controller connecting all editable widgets of the stack widget page for\n    *all* comma-separated value (CSV) exports with corresponding settings of\n    the current simulation configuration).\n    '


class QBetseeSimConfPagerCSVExport(QBetseeSimConfPagerExportABC):
    __doc__ = '\n    **CSV export pager** (i.e., :mod:`PySide2`-based controller connecting all\n    editable widgets of the stack widget page for the currently selected\n    comma-separated value (CSV) export with corresponding settings of a\n    YAML-backed list item of the currently open simulation configuration).\n\n    **This controller implements the well-known flyweight design pattern.**\n    Specifically, this single controller is shared between the zero or more CSV\n    exports configured for this simulation and hence *cannot* be implicitly\n    initialized at application startup. Instead, this controller is explicitly\n    reinitialized in an on-the-fly manner immediately before this page is\n    displayed to edit a single such export.\n    '

    @property
    def _pipe_cls(self) -> SimPipeExportABC:
        return SimPipeExportCSVs

    @property
    def _widget_name_prefix(self) -> str:
        return 'sim_conf_csv_item_'

    @property
    def _yaml_list(self) -> str:
        return self._p.csv.csvs_after_sim
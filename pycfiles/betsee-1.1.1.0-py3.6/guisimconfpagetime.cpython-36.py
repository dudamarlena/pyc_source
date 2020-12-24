# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/page/guisimconfpagetime.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2357 bytes
"""
**Temporal simulation configuration pager** (i.e., :mod:`PySide2`-based
controller for stack widget pages specific to temporal settings) functionality.
"""
from PySide2.QtWidgets import QMainWindow
from betse.science.parameters import Parameters
from betse.util.type.types import type_check
from betsee.util.widget.abc.control.guictlpageabc import QBetseePagerABC

class QBetseeSimConfPagerTime(QBetseePagerABC):
    __doc__ = '\n    **Temporal simulation configuration pager** (i.e., :mod:`PySide2`-based\n    controller connecting all editable widgets of the temporal stack widget\n    page with corresponding settings of the current simulation configuration).\n    '

    @type_check
    def init(self, main_window):
        super().init(main_window)
        sim_conf = main_window.sim_conf
        main_window.sim_conf_time_init_total.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.init_time_total))
        main_window.sim_conf_time_init_step.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.init_time_step))
        main_window.sim_conf_time_init_sampling.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.init_time_sampling))
        main_window.sim_conf_time_sim_total.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.sim_time_total))
        main_window.sim_conf_time_sim_step.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.sim_time_step))
        main_window.sim_conf_time_sim_sampling.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.sim_time_sampling))
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/pager/guisimconfpagertime.py
# Compiled at: 2019-01-16 01:51:30
# Size of source mod 2**32: 2267 bytes
"""
:mod:`PySide2`-based stack widget page controllers specific to temporal
settings.
"""
from PySide2.QtWidgets import QMainWindow
from betse.science.parameters import Parameters
from betse.util.type.types import type_check
from betsee.util.widget.abc.guicontrolabc import QBetseeControllerABC

class QBetseeSimConfTimeStackedWidgetPager(QBetseeControllerABC):
    __doc__ = '\n    :mod:`PySide2`-based stack widget page controller, connecting all editable\n    widgets of the temporal page with the corresponding low-level settings of\n    the current simulation configuration.\n    '

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
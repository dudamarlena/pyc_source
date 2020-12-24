# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/pager/guisimconfpagerpath.py
# Compiled at: 2019-01-16 01:51:30
# Size of source mod 2**32: 2859 bytes
"""
:mod:`PySide2`-based stack widget page controllers specific to paths.
"""
from PySide2.QtWidgets import QMainWindow
from betse.science.parameters import Parameters
from betse.util.type.types import type_check
from betsee.util.widget.abc.guicontrolabc import QBetseeControllerABC

class QBetseeSimConfPathStackedWidgetPager(QBetseeControllerABC):
    __doc__ = '\n    :mod:`PySide2`-based stack widget page controller, connecting all editable\n    widgets of the paths page with the corresponding low-level settings of the\n    current simulation configuration.\n    '

    @type_check
    def init(self, main_window):
        super().init(main_window)
        sim_conf = main_window.sim_conf
        main_window.sim_conf_path_seed_pick_file_line.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.seed_pickle_basename))
        main_window.sim_conf_path_init_pick_file_line.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.init_pickle_basename))
        main_window.sim_conf_path_init_pick_dir_line.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.init_pickle_dirname_relative),
          push_btn=(main_window.sim_conf_path_init_pick_dir_btn))
        main_window.sim_conf_path_init_exp_dir_line.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.init_export_dirname_relative),
          push_btn=(main_window.sim_conf_path_init_exp_dir_btn))
        main_window.sim_conf_path_sim_pick_file_line.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.sim_pickle_basename))
        main_window.sim_conf_path_sim_pick_dir_line.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.sim_pickle_dirname_relative),
          push_btn=(main_window.sim_conf_path_sim_pick_dir_btn))
        main_window.sim_conf_path_sim_exp_dir_line.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.sim_export_dirname_relative),
          push_btn=(main_window.sim_conf_path_sim_exp_dir_btn))
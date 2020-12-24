# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/controller/main_controller.py
# Compiled at: 2019-11-04 08:36:45
# Size of source mod 2**32: 4846 bytes
"""
This module implement the main controller class, which is the entry point
of the execution.
The entry class is `MainController` and the entrypoint method is 
`MainController.mainrun`

TODO:
    0. write the out directory structure component properly 
        (This is shared between the 3 modes: RUN, REVERT and NAVIGATE)

    Pipeline:
    1. load the default configuration.
    2. parse the command lines, then load the users config, then update the
        default configs.
    3. setup the ERROR_HANDLER module (pass the repodir).
    4. setup the log facility.
    5. based on the loaded config and command mode, call the relevant 
        mode executor with its configs. (RUN, REVERT, NAVIGATE)

    a) RUN will implement checkpoint and run tasks....
"""
from __future__ import print_function
import os, sys, glob, copy, importlib, logging, muteria.common.mix as common_mix, muteria.common.fs as common_fs, muteria.common.matrices as common_matrices, muteria.configmanager.configurations as configurations
from muteria.configmanager.helper import ConfigurationHelper
from muteria.repositoryandcode.repository_manager import RepositoryManager
import muteria.controller.logging_setup as logging_setup, muteria.controller.explorer as explorer, muteria.controller.executor as executor
ERROR_HANDLER = common_mix.ErrorHandler

class MainController(object):
    __doc__ = '\n    This class implements the main controlle which will organize the execution\n    and reporting.\n\n    :param execution_config: Configuration data for execution setting (such as:\n                            execution order, what to execute, ...)\n    :param reporting_config: Configuration for reporting (coverage, \n                            mutation score, ...)\n    :param tools_config: Configurations of the tools involved (test tool, \n                            mutation tool, code coverage tools)\n    :param project_config: Configurations of the project to analyze\n    :param output_pathdir: Path to the directory where the execution take place\n                            and the resulting data are stored.\n    '

    def __init__(self):
        logging_setup.console_tmp_log_setup()

    def internal_infos(self, config):
        ERROR_HANDLER.error_exit('FIXME: TODO: Implement the internal')

    def view(self, top_timeline_explorer, config):
        """
        Method used to navigate in the output dir and make simple queries
        """
        ERROR_HANDLER.error_exit('FIXME: TODO: Implement the View')

    def raw_config_main(self, raw_config):
        """
        TODO: Deal with config change at different runs
                Notify the user that the config changed and show the diff
        TODO: add option to load the config from prev if not specified()
        """
        final_conf = ConfigurationHelper.get_finalconf_from_rawconf(raw_conf=raw_config)
        self.main(final_config=final_conf)

    def main(self, final_config):
        """
        Entry point function using the final configuration object
        """
        top_timeline_explorer = explorer.TopExplorer(final_config.OUTPUT_ROOT_DIR.get_val())
        mode = final_config.RUN_MODE.get_val()
        if mode == configurations.SessionMode.EXECUTE_MODE:
            exec_obj = executor.Executor(final_config, top_timeline_explorer)
            exec_obj.main()
        else:
            if mode == configurations.SessionMode.RESTORE_REPOS_MODE:
                as_initial = final_config.restore.AS_INITIAL.get_val()
                repo_mgr = executor.Executor.create_repo_manager(final_config)
                repo_mgr.revert_repository(as_initial=as_initial)
            else:
                if mode == configurations.SessionMode.VIEW_MODE:
                    self.view(top_timeline_explorer, final_config)
                elif mode == configurations.SessionMode.INTERNAL_MODE:
                    self.internal_infos(final_config)
        logging.info('All Done!')
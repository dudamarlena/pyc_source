# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/optimizers/testexecution/tools/default.py
# Compiled at: 2019-09-26 13:00:18
# Size of source mod 2**32: 1417 bytes
""" Default test execution optimizer class
"""
from __future__ import print_function
import os, sys, copy, logging, muteria.common.mix as common_mix
from muteria.drivers.optimizers.testexecution.base_test_execution_optimizer import BaseTestExecutionOptimizer
ERROR_HANDLER = common_mix.ErrorHandler

class TestExecutionOptimizer(BaseTestExecutionOptimizer):

    @classmethod
    def installed(cls, custom_binary_dir=None):
        """ Check that the tool is installed
            :return: bool reprenting whether the tool is installed or not 
                    (executable accessible on the path)
                    - True: the tool is installed and works
                    - False: the tool is not installed or do not work
        """
        pass

    def reset(self, toolalias, test_list, disable_reset=False, **kwargs):
        """ Reset the optimizer
        """
        ERROR_HANDLER.assert_true(not self.reset_disabled, 'reset is disabled')
        self.test_ordered_list = copy.deepcopy(test_list)
        self.pointer = 0
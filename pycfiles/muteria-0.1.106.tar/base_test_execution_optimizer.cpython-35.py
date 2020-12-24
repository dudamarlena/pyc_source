# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/optimizers/testexecution/base_test_execution_optimizer.py
# Compiled at: 2019-09-26 13:00:01
# Size of source mod 2**32: 3347 bytes
""" Base and Default test execution optimizer classes

    Each file that implement a optimizer must have the class 
    `TestExecutionOptimizer` that implements the base class bellow
"""
from __future__ import print_function
import os, sys, logging, abc, muteria.common.mix as common_mix
ERROR_HANDLER = common_mix.ErrorHandler

class BaseTestExecutionOptimizer(abc.ABC):
    __doc__ = '\n    '

    def __init__(self, config, explorer, **kwargs):
        self.config = config
        self.explorer = explorer
        self.test_ordered_list = None
        self.pointer = 0
        self.reset_disabled = False

    def has_next_test(self):
        return self.pointer < len(self.test_ordered_list)

    def get_next_test(self):
        ERROR_HANDLER.assert_true(self.test_ordered_list is not None, 'uninitialized test_order_list')
        if self.has_next_test():
            ret = self.test_ordered_list[self.pointer]
            self.pointer += 1
        else:
            ret = None
        return ret

    def select_tests(self, proportion_number, is_proportion=True):
        """ Apply test Selection
        """
        ERROR_HANDLER.assert_true(self.test_ordered_list is not None, 'uninitialized test_order_list')
        ERROR_HANDLER.assert_true(proportion_number > 0, 'proportion_number must be positive')
        if is_proportion:
            ERROR_HANDLER.assert_true(proportion_number <= 100, 'proportion must be <= 100')
            proportion_number = round(len(self.test_ordered_list) * proportion_number / 100.0)
            proportion_number = max(1, int(proportion_number))
        return self.test_ordered_list[:proportion_number]

    def feedback(self, test_case, verdict, **kwargs):
        """ Possibly get feedback from past executions
            Override this if needed
        """
        pass

    @classmethod
    @abc.abstractclassmethod
    def installed(cls, custom_binary_dir=None):
        """ Check that the tool is installed
            :return: bool reprenting whether the tool is installed or not 
                    (executable accessible on the path)
                    - True: the tool is installed and works
                    - False: the tool is not installed or do not work
        """
        print('!!! Must be implemented in child class !!!')

    @abc.abstractmethod
    def reset(self, toolalias, test_list, disable_reset=False, **kwargs):
        """ Reset the optimizer
            :param disable_reset: disable reset after this call to reset
        """
        print('!!! Must be implemented in child class !!!')
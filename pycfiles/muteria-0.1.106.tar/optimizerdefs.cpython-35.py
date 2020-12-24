# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/optimizers/criteriatestexecution/optimizerdefs.py
# Compiled at: 2019-09-26 08:53:09
# Size of source mod 2**32: 1771 bytes
from __future__ import print_function
import importlib, muteria.common.mix as common_mix
from muteria.drivers.criteria import TestCriteria
import muteria.drivers.optimizers.criteriatestexecution.tools as crit_opt

class CriteriaOptimizers(common_mix.EnumAutoName):
    NO_OPTIMIZATION = importlib.import_module('.default', package=crit_opt.__name__).CriteriaTestExecutionOptimizer
    SM_OPTIMIZED_BY_WM = importlib.import_module('.strongmutation_by_weakmutation', package=crit_opt.__name__).CriteriaTestExecutionOptimizer
    SM_OPTIMIZED_BY_MCOV = importlib.import_module('.strongmutation_by_mutantcoverage', package=crit_opt.__name__).CriteriaTestExecutionOptimizer

    def get_optimizer(self):
        return self.get_field_value()


def check_is_right_optimizer(criterion, optimizer):
    """ Check that the optimizer is fit for the criterion
        :return: True if fit, False otherwise
    """
    dat = {TestCriteria.STRONG_MUTATION: {
                                    CriteriaOptimizers.SM_OPTIMIZED_BY_MCOV,
                                    CriteriaOptimizers.SM_OPTIMIZED_BY_WM}}
    if criterion in dat and optimizer in dat[criterion]:
        return True
    return False
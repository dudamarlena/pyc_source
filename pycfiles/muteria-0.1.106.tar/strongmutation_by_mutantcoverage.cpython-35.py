# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/optimizers/criteriatestexecution/tools/strongmutation_by_mutantcoverage.py
# Compiled at: 2019-09-26 12:30:15
# Size of source mod 2**32: 1183 bytes
""" Default criteria test execution optimizer class
"""
from __future__ import print_function
import os, sys, copy, logging, muteria.common.mix as common_mix, muteria.common.matrices as common_matrices, muteria.controller.explorer as explorer
from muteria.drivers.criteria import TestCriteria
import muteria.drivers.optimizers.criteriatestexecution.tools.strongmutation_by_weakmutation as sm_wm
from muteria.drivers.optimizers.testexecution.tools.default import TestExecutionOptimizer
ERROR_HANDLER = common_mix.ErrorHandler

class CriteriaTestExecutionOptimizer(sm_wm.CriteriaTestExecutionOptimizer):

    def _get_optimizing_criterion(self):
        return TestCriteria.MUTANT_COVERAGE
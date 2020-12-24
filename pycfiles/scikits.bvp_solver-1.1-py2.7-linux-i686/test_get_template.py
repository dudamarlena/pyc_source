# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tests/test_get_template.py
# Compiled at: 2011-07-22 15:26:35
"""
Created on Mar 27, 2009

@author: johnsalvatier
"""
from scikits.bvp_solver import get_template
import numpy
from numpy import array
import codeop

def test_templateExample():
    source1 = get_template(num_ODE=3, num_parameters=1, num_left_boundary_conditions=1, function_derivative=True, boundary_conditions_derivative=True, singular_term=True)
    codeop.compile_command(source1)
    source2 = get_template(num_ODE=3, num_parameters=0, num_left_boundary_conditions=1, function_derivative=False, boundary_conditions_derivative=False, singular_term=False)
    codeop.compile_command(source2)
    source3 = get_template(num_ODE=1, num_parameters=3, num_left_boundary_conditions=0, function_derivative=False, boundary_conditions_derivative=False, singular_term=False)
    codeop.compile_command(source3)
    source4 = get_template(num_ODE=1, num_parameters=3, num_left_boundary_conditions=4, function_derivative=True, boundary_conditions_derivative=True, singular_term=True)
    codeop.compile_command(source4)
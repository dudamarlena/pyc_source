# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/Desktop_Tests/MPathic/mpathic/tests/functional_tests_mpathic.py
# Compiled at: 2018-05-14 16:38:01
from __future__ import print_function
import mpathic as mpa, numpy as np
global_success_counter = 0
global_fail_counter = 0
bool_fail_list = [
 0, -1, 'True', 'x', 1]
bool_success_list = [False, True]

def test_for_mistake(func, *args, **kw):
    """
    Run a function with the specified parameters and register whether
    success or failure was a mistake

    parameters
    ----------

    func: (function or class constructor)
        An executable function to which *args and **kwargs are passed.

    return
    ------

    None.
    """
    global global_fail_counter
    global global_success_counter
    test_num = global_fail_counter + global_success_counter
    print('Test # %d: ' % test_num, end='')
    obj = func(*args, **kw)
    if obj.mistake:
        global_fail_counter += 1
    else:
        global_success_counter += 1


def test_parameter_values(func, var_name=None, fail_list=[], success_list=[], **kwargs):
    """
    Tests predictable success & failure of different values for a
    specified parameter when passed to a specified function

    parameters
    ----------

    func: (function)
        Executable to test. Can be function or class constructor.

    var_name: (str)
        Name of variable to test. If not specified, function is
        tested for success in the absence of any passed parameters.

    fail_list: (list)
        List of values for specified variable that should fail

    success_list: (list)
        List of values for specified variable that should succeed

    **kwargs:
        Other keyword variables to pass onto func.

    return
    ------

    None.

    """
    if var_name is not None:
        print('Testing %s() parameter %s ...' % (func.__name__, var_name))
        for x in fail_list:
            kwargs[var_name] = x
            test_for_mistake(func=func, should_fail=True, **kwargs)

        for x in success_list:
            kwargs[var_name] = x
            test_for_mistake(func=func, should_fail=False, **kwargs)

        print('Tests passed: %d. Tests failed: %d.\n' % (
         global_success_counter, global_fail_counter))
    else:
        print('Testing %s() without parameters.' % func.__name__)
        test_for_mistake(func=func, should_fail=False, **kwargs)
    return


def test_simulate_library():
    test_parameter_values(func=mpa.simulate_library_class)
    test_parameter_values(func=mpa.simulate_library_class, var_name='wtseq', fail_list=[3, 1.0, 'XxX', False, ''], success_list=[
     'ATTCCGAGTA', 'ATGTGTAGTCGTAG'])
    test_parameter_values(func=mpa.simulate_library_class, var_name='mutrate', fail_list=[1.1, 2, -1, 0], success_list=[0.5, 0.1])
    test_parameter_values(func=mpa.simulate_library_class, var_name='numseq', fail_list=['x', -1, 0, 0.5], success_list=[1, 2, 3, 100])
    test_parameter_values(func=mpa.simulate_library_class, var_name='dicttype', fail_list=[
     'x', 1, True], success_list=['dna', 'rna', 'protein'])
    test_parameter_values(func=mpa.simulate_library_class, var_name='probarr', fail_list=[1, 1.0, 'x', [1, 2, 3]], success_list=[None])
    test_parameter_values(func=mpa.simulate_library_class, var_name='tags', fail_list=[None, -1, 3.9], success_list=[True, False])
    test_parameter_values(func=mpa.simulate_library_class, var_name='tag_length', fail_list=[None, -1, 3.9], success_list=[
     3, 200])
    return


test_simulate_library()
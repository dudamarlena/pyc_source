# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thierry/vmWareLinux/proj/simulatortofmu/SimulatorToFMU/simulatortofmu/parser/simulator_wrapper.py
# Compiled at: 2017-07-07 15:19:36
# Size of source mod 2**32: 1885 bytes
import numpy

def exchange(configuration_file, time, input_names, input_values, output_names, write_results):
    """
    Return  a list of output values from the Python-based Simulator.
    The order of the output values must match the order of the output names.    

    :param configuration_file (String): Path to the Simulator model or configuration file
    :param time (Float): Simulation time
    :param input_names (Strings): Input names 
    :param input_values (Floats): Input values (same length as input_names) 
    :param output_names (Strings): Output names
    :param write_results (Float): Store results to file (1 to store, 0 else)
        
    Example:
        >>> configuration_file = 'config.json'
        >>> time = 0
        >>> input_names = ['v']
        >>> input_values = [220.0]
        >>> output_names = ['i']
        >>> write_results = 0
        >>> output_values = simulator(configuration_file, time, input_names,
                        input_values, output_names, write_results)
    """
    if len(output_names) > 1:
        output_values = [
         1.0] * len(output_names)
    else:
        output_values = 100.0
    return output_values
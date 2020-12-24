# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/arguments/validation.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 1431 bytes
import eddington.consts as ct
__all__ = ['validate_arguments']
from eddington.arguments.general_functionalities import argument_string

def validate_arguments(args):
    args_dict = vars(args)
    validate_output_dir(args_dict.get(ct.OUTPUT_DIR, None))
    violating_plot_arguments = dependent_arguments(args_dict, [ct.TITLE, ct.RESIDUALS_TITLE, ct.XLABEL, ct.YLABEL], ct.PLOT)
    if len(violating_plot_arguments) != 0:
        raise ValueError(f"The arguments {', '.join(violating_plot_arguments)} cannot be set when {ct.NO_PLOT} is set.")


def validate_output_dir(output_dir):
    if output_dir is None:
        return
    else:
        if not output_dir.exists():
            output_dir.mkdir()
            return
        assert output_dir.is_dir(), f"{output_dir} is not a directory!"
    if len(list(output_dir.glob('*'))) != 0:
        raise ValueError(f"{output_dir} must be empty!")


def dependent_arguments(args_dict, arguments_list, dependent_argument):
    if get_boolean_argument(args_dict, dependent_argument):
        return []
    return [argument_string(arg) for arg in arguments_list if argument_exists(args_dict, arg)]


def get_boolean_argument(args_dict, argument):
    return args_dict.get(argument, False)


def argument_exists(args_dict, argument):
    return args_dict.get(argument.replace('-', '_'), None) is not None
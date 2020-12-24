# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\frontend\_registry.py
# Compiled at: 2020-01-06 14:08:19
# Size of source mod 2**32: 2831 bytes
__doc__ = 'Functionality to register functions that are used to transform between different data types in the frontend.\n'
__author__ = 'Daniel Rose'
__status__ = 'Development'
REGISTERED_INTERFACES = dict()

def register_interface(func, name=''):
    """Register a transformation function (interface) between two representations of models.

    Parameters
    ----------
    func
        Function to be registered. Needs to start with "from_" or "to_" to signify the direction of transformation
    name
        (Optional) String that defines the name under which the function should be registered. If left empty,
        the name will be formatted in the form {target}_from_{source}, where target and source are representations to
        transform from or to."""
    if name is '':
        module_name = func.__module__.split('.')[(-1)]
        func_name = func.__name__
        if func_name.startswith('from_'):
            target = module_name
            source = func_name[5:]
        else:
            if func_name.startswith('to_'):
                source = module_name
                target = func_name[3:]
            else:
                raise ValueError(f"Function name {func_name} does not adhere to convention to start with either `to_` or `from_`.")
        new_name = f"{target}_from_{source}"
    else:
        new_name = name
    if new_name in REGISTERED_INTERFACES:
        raise ValueError(f"Interface {new_name} already exist. Cannot add {func}.")
    else:
        REGISTERED_INTERFACES[new_name] = func
    return func
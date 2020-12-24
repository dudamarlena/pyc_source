# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/capabilities.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 3175 bytes
import logging
LOG = logging.getLogger(__name__)
runtime_capabilities = {}

def add_capability(entry, name, description, doc=None, serial=False, num_args=None, kwarg_names=None, no_return=False, dependency_callback=None, timeout=1800, task_id_kwargs=False):
    """Add a new capability to the runtime capabilities.

    :param entry: The new capability.
    :param name: Name of the new capability.
    :param description: Description of the new capability.
    :param doc: Function docstring.
    :param serial: Boolean indication if the task is serial.
    :param num_args: Number of expected arguments.
    :param kwarg_names: Named arguments.
    :param no_return: True if the task doesn't return any value.
    :param dependency_callback: Callback to check dependency.
    :param timeout: Timeout for the new capability.
    :param task_id_kwargs: Whether to put task_id in kwargs.
    """
    LOG.info('Adding capability %s' % name)
    runtime_capabilities[name] = {'name':name, 
     'entry':entry, 
     'description':description, 
     'doc':doc, 
     'serial':serial, 
     'num_args':num_args, 
     'kwarg_names':kwarg_names, 
     'no_return':no_return, 
     'dependency_callback':dependency_callback, 
     'timeout':timeout, 
     'task_id_kwargs':task_id_kwargs}


def capability(name, description, serial=False, num_args=None, kwarg_names=None, no_return=False, dependency_callback=None, timeout=1800, task_id_kwargs=False):
    """Decorator to add a new capability.

    :param name: Name of the new capability.
    :param description: Description of the new capability.
    :param serial: Boolean indication if the task is serial.
    :param num_args: Number of expected arguments.
    :param kwarg_names: Named arguments.
    :param no_return: True if the task doesn't return any value.
    :param dependency_callback: Callback to check dependency.
    :param timeout: Timeout for the new capability.
    :param task_id_kwargs: Whether to put task_id in kwargs.
    """

    def wrap(entry):
        add_capability(entry, name, description, doc=(entry.__doc__), serial=serial,
          num_args=num_args,
          kwarg_names=kwarg_names,
          no_return=no_return,
          dependency_callback=dependency_callback,
          timeout=timeout,
          task_id_kwargs=task_id_kwargs)
        return entry

    return wrap
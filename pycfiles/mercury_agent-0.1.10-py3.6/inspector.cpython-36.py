# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/procedures/inspector.py
# Compiled at: 2019-02-11 13:08:11
# Size of source mod 2**32: 1853 bytes
from mercury_agent.capabilities import capability
from mercury_agent.configuration import get_configuration
from mercury_agent.inspector import inspect
from mercury_agent.inspector.inspect import global_device_info
from mercury_agent.inspector.inspectors import health

@capability('inspector', description='Run inspector')
def inspector():
    """
    Manually run inspectors
    :return: results
    """
    return inspect.inspect()


@capability('check_hardware', description='Check hardware for errors')
def check_hardware():
    """
    Checks hardware for inconsistencies and defects. Returns a list of discovered critical errors.
    :return:
    """
    configuration = get_configuration().agent
    errors = []
    _health_data = health.system_health_inspector(global_device_info)
    if _health_data['corrected_hardware_event_count'] >= configuration.hardware.mce_threshold:
        errors.append('MCE count is {} which is above the configured threshold of {}'.format(_health_data['corrected_hardware_event_count'], configuration.hardware.mce_threshold))
    return {'errors':errors, 
     'error_count':len(errors)}
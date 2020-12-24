# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/status/status_lib/environment.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import importlib, json
DEFAULT_MODULE_ATTR = [
 '__doc__', '__file__', '__name__', '__package__', '__path__', '__version__']

def check_module_status(module):
    module['is_fulfilled'] = False if module['fulfilled_with_one'] else True
    for module_name in module['libraries'].keys():
        status = {}
        try:
            try:
                package = importlib.import_module(module_name)
                content = dir(package)
                for attr in DEFAULT_MODULE_ATTR:
                    if attr in content:
                        status[attr.replace('__', '')] = getattr(package, attr) or ''
                    else:
                        status[attr.replace('__', '')] = 'unknown'

                status['installed'] = True
                if module['fulfilled_with_one']:
                    module['is_fulfilled'] = True
                status['content'] = content
            except Exception as exp:
                status = {'installed': False, 'error': str(exp)}
                if not module['fulfilled_with_one']:
                    module['is_fulfilled'] = False

        finally:
            module['libraries'][module_name]['status'] = status

    return module


def load_module_status(module_name):
    module = importlib.import_module('doorpi.status.requirements_lib.' + module_name).REQUIREMENT
    return check_module_status(module)


REQUIREMENTS_DOORPI = {'config': load_module_status('req_config'), 
   'sipphone': load_module_status('req_sipphone'), 
   'event_handler': load_module_status('req_event_handler'), 
   'webserver': load_module_status('req_webserver'), 
   'keyboard': load_module_status('req_keyboard'), 
   'system': load_module_status('req_system')}

def get(*args, **kwargs):
    try:
        if len(kwargs['name']) == 0:
            kwargs['name'] = ['']
        if len(kwargs['value']) == 0:
            kwargs['value'] = ['']
        status = {}
        for name_requested in kwargs['name']:
            for possible_name in REQUIREMENTS_DOORPI.keys():
                if name_requested in possible_name:
                    status[possible_name] = REQUIREMENTS_DOORPI[possible_name]

        return status
    except Exception as exp:
        logger.exception(exp)
        return {'Error': 'could not create ' + str(__name__) + ' object - ' + str(exp)}


def is_active(doorpi_object):
    return True
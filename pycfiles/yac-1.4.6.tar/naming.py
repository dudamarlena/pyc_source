# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: yac/lib/naming.py
# Compiled at: 2017-11-16 20:28:41
import os, imp, urlparse
from yac.lib.paths import get_config_path, get_lib_path
from yac.lib.registry import set_remote_string_w_challenge, get_remote_value, get_registry_keys
from yac.lib.registry import set_local_value, get_local_value, delete_local_value
from yac.lib.variables import get_variable
from yac.lib.file import get_file_contents, create_customization_file, file_in_registry, get_file_reg_key

def get_stack_name(params):
    return get_namer_module().get_stack_name(params)


def get_resource_name(params, resource):
    return get_namer_module().get_resource_name(params, resource)


def get_namer_module():
    return imp.load_source('yac.lib.naming', get_namer())


def get_namer():
    yac_namer = get_local_value('yac_namer')
    if not yac_namer:
        yac_namer = os.path.join(get_lib_path(), 'naming_default.py')
    return yac_namer


def set_namer(service_descriptor, servicefile_path, vpc_prefs):
    if get_variable(service_descriptor, 'resource-namer', ''):
        service_namer_path = get_variable(service_descriptor, 'resource-namer', '')
        if not file_in_registry(service_namer_path):
            service_namer_abs_path = os.path.join(servicefile_path, service_namer_path)
            if os.path.exists(service_namer_abs_path):
                namer_code = get_file_contents(service_namer_abs_path)
                file_namespace = get_variable(service_descriptor, 'service-name', '')
                yac_file_key = get_file_reg_key(service_namer_path, file_namespace)
                service_namer_path = create_customization_file(yac_file_key, namer_code)
        elif file_in_registry(service_namer_path):
            service_namer_path = create_customization_file(service_namer_path)
    elif get_variable(vpc_prefs, 'resource-namer', ''):
        service_namer_path = get_variable(vpc_prefs, 'resource-namer', '')
    else:
        service_namer_path = os.path.join(get_lib_path(), 'naming_default.py')
    set_local_value('yac_namer', service_namer_path)


def validate_namer_script(namer_script, prefs_path):
    val_errors = {}
    script_path = os.path.join(prefs_path, namer_script)
    if os.path.exists(script_path):
        naming_module = imp.load_source('yac.lib', script_path)
        if 'get_stack_name' not in dir(naming_module):
            val_errors.update({'stack-namer': 'namer script %s lacks the get_stack_name fxn' % namer_script})
        if 'get_resource_name' not in dir(naming_module):
            val_errors.update({'resource-namer': 'namer script %s lacks the get_resource_name fxn' % namer_script})
    else:
        val_errors = {'namer-script': "namer script %s doesn't exist" % namer_script}
    return val_errors
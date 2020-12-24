# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/intrinsic.py
# Compiled at: 2018-01-05 13:50:32
import os, imp, urlparse
from sets import Set
from yac.lib.file import get_file_contents, file_in_registry, file_in_yac_sources
from yac.lib.file import create_customization_file, get_localized_script_path
from yac.lib.paths import get_yac_path, get_lib_path
from yac.lib.variables import get_variable, set_variable, get_map_variable
from yac.lib.naming import get_resource_name
INSTINSICS = ['yac-ref', 'yac-join', 'yac-fxn', 'yac-name', 'yac-map']
YAC_REF_ERROR = 'ref-error'
YAC_FXN_ERROR = 'fxn-error'
YAC_MAP_ERROR = 'map-error'
INSTRINSIC_ERROR_KEY = 'intrinsic-errors'

def apply_fxn(source_dict, params):
    for key in source_dict.keys():
        if type(source_dict[key]) == dict:
            source_dict[key] = apply_fxn_dict(source_dict[key], params)
        elif type(source_dict[key]) == list:
            source_dict[key] = apply_fxn_list(source_dict[key], params)
        else:
            source_dict[key] = apply_fxn_leaf(key, source_dict, params)

    return source_dict


def apply_fxn_dict(source_dict, params):
    sub_keys = source_dict.keys()
    if len(Set(sub_keys) & Set(INSTINSICS)) == 1:
        source_dict = apply_fxn_leaf(sub_keys[0], source_dict, params)
    else:
        source_dict = apply_fxn(source_dict, params)
    return source_dict


def apply_fxn_list(source_list, params):
    for i, item in enumerate(source_list):
        if type(item) == dict:
            source_list[i] = apply_fxn_dict(item, params)
        elif type(item) == list:
            source_list[i] = apply_fxn_list(item, params)
        else:
            source_list[i] = item

    return source_list


def apply_fxn_leaf(key, source_dict, params):
    if key == 'yac-ref':
        setpoint = get_variable(params, source_dict[key], 'M.I.A.')
        if setpoint == 'M.I.A.':
            setpoint = '%s: %s' % (YAC_REF_ERROR, source_dict[key])
            error_list = get_variable(params, INSTRINSIC_ERROR_KEY, [])
            set_variable(params, INSTRINSIC_ERROR_KEY, error_list + [setpoint])
        return setpoint
    if key == 'yac-map':
        setpoint = ''
        map_tuple = source_dict[key]
        setpoint = map_tuple or '%s: %s missing args' % (YAC_MAP_ERROR, source_dict[key])
        error_list = get_variable(params, INSTRINSIC_ERROR_KEY, [])
        set_variable(params, INSTRINSIC_ERROR_KEY, error_list + [setpoint])
    else:
        if len(map_tuple) == 1:
            setpoint = '%s: %s missing lookup arg' % (YAC_MAP_ERROR, source_dict[key])
            error_list = get_variable(params, INSTRINSIC_ERROR_KEY, [])
            set_variable(params, INSTRINSIC_ERROR_KEY, error_list + [setpoint])
        else:
            map_name = map_tuple[0]
            param_key = map_tuple[1]
            if map_name in params:
                setpoint = get_map_variable(params, map_name, param_key, 'M.I.A')
                if setpoint == 'M.I.A':
                    setpoint = '%s: %s map lookup miss' % (YAC_MAP_ERROR, source_dict[key])
                    error_list = get_variable(params, INSTRINSIC_ERROR_KEY, [])
                    set_variable(params, INSTRINSIC_ERROR_KEY, error_list + [setpoint])
            else:
                setpoint = '%s: %s map missing' % (YAC_MAP_ERROR, source_dict[key])
                error_list = get_variable(params, INSTRINSIC_ERROR_KEY, [])
                set_variable(params, INSTRINSIC_ERROR_KEY, error_list + [setpoint])
        return setpoint
    if key == 'yac-join':
        delimiters = source_dict[key][0]
        name_parts = source_dict[key][1]
        filled_parts = apply_fxn_list(name_parts, params)
        filled_parts = filter(None, filled_parts)
        return delimiters.join(filled_parts)
    else:
        if key == 'yac-fxn':
            fxn_script = source_dict[key]
            return apply_custom_fxn(fxn_script, params)
        else:
            if key == 'yac-name':
                resource = source_dict[key]
                return get_resource_name(params, resource)
            return source_dict[key]

        return


def apply_custom_fxn(script_path_arg, params):
    script_path = get_localized_script_path(script_path_arg, params)
    return_val = ''
    if script_path and os.path.exists(script_path):
        module_name = 'yac.lib.customizations'
        script_module = imp.load_source(module_name, script_path)
        return_val = script_module.get_value(params)
    else:
        setpoint = '%s: %s' % (YAC_FXN_ERROR, script_path)
        error_list = get_variable(params, INSTRINSIC_ERROR_KEY, [])
        set_variable(params, INSTRINSIC_ERROR_KEY, error_list + [setpoint])
    return return_val
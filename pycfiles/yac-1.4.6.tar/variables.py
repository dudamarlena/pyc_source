# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/variables.py
# Compiled at: 2018-01-04 15:04:07


def get_variable(params, variable_name, default_value='', value_key='value'):
    if variable_name in params and value_key in params[variable_name]:
        return params[variable_name][value_key]
    else:
        return default_value


def get_variable_comment(params, variable_name):
    if variable_name in params and 'comment' in params[variable_name]:
        return params[variable_name]['comment']
    else:
        return ''


def set_variable(params, variable_name, value, comment='', value_key='value'):
    params[variable_name] = {value_key: value, 'comment': comment}


def get_map_variable(params, map_name, param_key, default_value='', value_key='value'):
    param_val = get_variable(params, param_key, '')
    if param_val and map_name in params and value_key in params[map_name] and param_val in params[map_name][value_key]:
        return params[map_name][value_key][param_val]
    else:
        return default_value


def set_map_variable(params, map_name, map_key, value, value_key='value'):
    if map_name in params and value_key in params[map_name] and map_key in params[map_name][value_key]:
        params[map_name][value_key][map_key] = value
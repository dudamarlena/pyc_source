# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea-example-app/opentea_example_app/gui/calculator/ot2jsonschema_params.py
# Compiled at: 2019-01-10 11:20:22
# Size of source mod 2**32: 5884 bytes
"""Jsonshema specifics to the params type of opentea."""

def add_bnd(ot_type, bnd_type, ot_data_type):
    """Return the JSON SCHEMA translation of an optentea bnd.

    Parameter :
    -----------
    ot_type : the openTea full type (str: list_double_gt1)
    bnd_type : the boundary kind (str: _lt)
    ot_data_type : the openTea data type (str: double, integer)
    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    for bit in ot_type.split('_'):
        if bit.startswith(bnd_type[1:]):
            if 'double' == ot_data_type:
                bnd_val = float(bit[2:])
                if bnd_type == '_le':
                    out['maximum'] = bnd_val
                if bnd_type == '_lt':
                    out['maximum'] = bnd_val
                    out['exclusiveMaximum'] = True
                if bnd_type == '_ge':
                    out['minimum'] = bnd_val
                if bnd_type == '_gt':
                    out['minimum'] = bnd_val
                    out['exclusiveMinimum'] = True
            elif 'integer' == ot_data_type:
                bnd_val = int(bit[2:])
                if bnd_type == '_le':
                    out['maximum'] = bnd_val
                if bnd_type == '_lt':
                    out['maximum'] = bnd_val
                    out['exclusiveMaximum'] = True
                if bnd_type == '_ge':
                    out['minimum'] = bnd_val
                if bnd_type == '_gt':
                    out['minimum'] = bnd_val
                    out['exclusiveMinimum'] = True

    return out


def param_double_node(dict_):
    """Import a param node.

    Parameter :
    -----------
    dict_ : the openTea specification param double

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    if 'default' in dict_:
        out['default'] = float(dict_['default'])
    for bnd in ('_lt', '_le', '_gt', '_ge'):
        if bnd in dict_['type']:
            out.update(add_bnd(dict_['type'], bnd, 'double'))

    out['type'] = 'number'
    return out


def param_integer_node(dict_):
    """Import a param node.

    Parameter :
    -----------
    dict_ : the openTea specification param double

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    if 'default' in dict_:
        out['default'] = int(dict_['default'])
    out['type'] = 'integer'
    for bnd in ('_lt', '_le', '_gt', '_ge'):
        if bnd in dict_['type']:
            out.update(add_bnd(dict_['type'], bnd, 'integer'))

    return out


def param_string_node(dict_):
    """Import a string node

    Parameter :
    -----------
    dict_ : the openTea specification param string

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    if 'default' in dict_:
        out['default'] = dict_['default']
    out['type'] = 'string'
    out['ot_type'] = 'string'
    return out


def param_file_node(dict_):
    """Import a string node

    Parameter :
    -----------
    dict_ : the openTea specification param string

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    if 'default' in dict_:
        out['default'] = dict_['default']
    out['type'] = 'string'
    out['ot_type'] = 'file'
    if 'filter' in dict_:
        out['ot_filter'] = dict_['filter'].split(';')
    return out


def param_folder_node(dict_):
    """Import a folder node

    Parameter :
    -----------
    dict_ : the openTea specification folder string

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    if 'default' in dict_:
        out['default'] = dict_['default']
    out['type'] = 'string'
    out['ot_type'] = 'folder'
    return out


def param_onoff_node(dict_):
    """Import a onoff node

    Parameter :
    -----------
    dict_ : the openTea specification param  onoff

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    out['type'] = 'boolean'
    if 'default' in dict_:
        if dict_['default'] == '1':
            out['default'] = True
        else:
            if dict_['default'] == '0':
                out['default'] = False
            else:
                raise NotImplementedError('onoff : could not interpret default' + dict_['default'])
    return out


def param_selection_node(dict_):
    """Import a selection node.

    Parameter :
    -----------
    dict_ : the openTea specification param  selection

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    out['type'] = 'string'
    out['ot_type'] = 'selection'
    return out


def param_node(dict_):
    """Import a param node.

    Parameter :
    -----------
    dict_ : the openTea specification dictionnary tab

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    out['name'] = dict_['name']
    if 'title' in dict_:
        out['title'] = dict_['title']
    else:
        out['title'] = dict_['name']
    out['ot_type'] = dict_['type']
    if 'list' in out['ot_type']:
        out['type'] = 'null'
    else:
        if 'double' in out['ot_type']:
            tmp = param_double_node(dict_)
            out.update(tmp)
        else:
            if 'integer' in out['ot_type']:
                tmp = param_integer_node(dict_)
                out.update(tmp)
            else:
                if 'string' in out['ot_type']:
                    out.update(param_string_node(dict_))
                else:
                    if 'file' in out['ot_type']:
                        out.update(param_file_node(dict_))
                    else:
                        if 'folder' in out['ot_type']:
                            out.update(param_file_node(dict_))
                        else:
                            if 'selection' in out['ot_type']:
                                out.update(param_selection_node(dict_))
                            else:
                                if 'onoff' in out['ot_type']:
                                    out.update(param_onoff_node(dict_))
                                else:
                                    raise NotImplementedError('param : could not interpret ot_type ' + out['ot_type'])
    return out
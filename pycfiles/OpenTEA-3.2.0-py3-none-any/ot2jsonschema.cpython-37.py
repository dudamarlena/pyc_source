# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea-example-app/opentea_example_app/gui/calculator/ot2jsonschema.py
# Compiled at: 2019-01-11 10:52:39
# Size of source mod 2**32: 11851 bytes
"""Translates a raw openTea specification into a proper JSON SCHEMA"""
from collections import OrderedDict
from ot2jsonschema_params import param_node

def ot2sjsonschema(dict_):
    """Import the dictionnary.

    Parameter :
    -----------
    dict_ : the openTea specification dictionnary to translate
    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    for key in dict_:
        root = key

    root_dict = dict_[root]
    if 'ot_type' in root_dict:
        if root_dict['ot_type'] == 'solver':
            out = solver_node(root_dict)
        else:
            raise NotImplementedError('No ot_type -solver- in first level of dictionnary')
    else:
        raise NotImplementedError('No ot_type in first level of dictionnary')
    return out


def solver_node(dict_):
    """Import a solver node.

    Parameter :
    -----------
    dict_ : the openTea specification dictionnary for a solver

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    for item in ('name', 'title', 'ot_type'):
        out[item] = dict_[item]

    out['type'] = 'object'
    out['properties'] = {}
    for key in dict_:
        if key in ('name', 'title', 'ot_type', 'folder'):
            continue
        if isinstance(dict_[key], dict):
            if 'ot_type' in dict_[key].keys():
                dict_[key]['ot_type'] == 'tab'
                out['properties'][key] = tab_node(dict_[key])
        else:
            raise NotImplementedError('Solver node : could not translate key -' + key + '-')

    return out


def translate_existif(condition):
    """ Translate the existif conditions"""
    iftest = None
    iflhs = None
    ifrhs = None
    for test in ('==', '>', '>=', '<', '<=', '!='):
        if test in condition:
            iftest = test
            pos1 = condition.find(test)
            pos2 = pos1 + len(test)
            iflhs = condition[:pos1]
            ifrhs = condition[pos2:]

    for char in '#{}':
        iflhs = iflhs.strip(char)
        ifrhs = ifrhs.strip(char)

    if ifrhs == '1':
        ifrhs = True
    if ifrhs == '0':
        ifrhs = False
    ei_dict = {'operator':iftest,  'node':iflhs, 
     'value':ifrhs}
    return ei_dict


def tab_node(dict_):
    """Import a tab node.

    Parameter :
    -----------
    dict_ : the openTea specification dictionnary for a tab

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    for item in ('title', 'ot_type'):
        out[item] = dict_[item]

    for item in ('order', 'script'):
        if item in dict_.keys():
            out[item] = dict_[item]

    if 'existif' in dict_.keys():
        out['existif'] = translate_existif(dict_['existif'])
    out['type'] = 'object'
    out['name'] = dict_['folder']
    out['properties'] = {}
    for key in dict_:
        if key in ('name', 'title', 'ot_type', 'order', 'script', 'folder', 'existif'):
            continue
        if isinstance(dict_[key], dict):
            if 'ot_type' in dict_[key].keys():
                if dict_[key]['ot_type'] == 'model':
                    out['properties'][key] = model_node(dict_[key])
                else:
                    if dict_[key]['ot_type'] == 'modelonoff':
                        out['properties'][key] = modelonoff_node(dict_[key])
                    else:
                        if dict_[key]['ot_type'] == 'status':
                            out['properties'][key] = status_node(dict_[key])
                        else:
                            if dict_[key]['ot_type'] == 'multiple':
                                out['properties'][key] = multiple_node(dict_[key])
                            else:
                                if dict_[key]['ot_type'] == 'xor':
                                    out['properties'][key] = xor_node(dict_[key])
                                else:
                                    if dict_[key]['ot_type'] == 'view3d':
                                        out['properties'][key] = view3d_node(dict_[key])
                                    else:
                                        raise NotImplementedError('Tab node o: could not translate key -' + key + '- ot_type :' + dict_[key]['ot_type'])
        else:
            raise NotImplementedError('Tab node : could not translate key -' + key + '-')

    return out


def model_node(dict_):
    """Import a model node.

    Parameter :
    -----------
    dict_ : the openTea specification dictionnary model

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
    if 'existif' in dict_.keys():
        out['existif'] = translate_existif(dict_['existif'])
    if 'layout' in dict_:
        out['ot_layout'] = dict_['layout']
    out['ot_type'] = 'model'
    out['type'] = 'object'
    out['properties'] = {}
    for key in dict_:
        if key in ('name', 'title', 'ot_type', 'existif', 'layout'):
            continue
        if key in ('docu', 'desc'):
            out['properties'][key] = docudesc_node(key, dict_[key])
        elif isinstance(dict_[key], dict):
            if 'ot_type' in dict_[key].keys():
                if dict_[key]['ot_type'] == 'param':
                    out['properties'][key] = param_node(dict_[key])
                if dict_[key]['ot_type'] == 'status':
                    out['properties'][key] = status_node(dict_[key])
                if dict_[key]['ot_type'] == 'choice':
                    out['properties'][key] = choice_node(dict_[key])
        else:
            raise NotImplementedError('Model node : could not translate key -' + key + '-')

    return out


def modelonoff_node(dict_):
    """Import a modelonoff node.

    Parameter :
    -----------
    dict_ : the openTea specification dictionnary model

    Output :
    --------
    out : the json schema dictionnary
    """
    out = model_node(dict_)
    out['ot_type'] = 'modelonoff'
    out['ot_default'] = False
    return out


def docudesc_node(docu_or_desc, str_docudesc):
    """Import a docu/desc node.

    Parameter :
    -----------
    docu_or_desc : str, ither docu or desc
    dict_ : the openTea specification dictionnary desc_docu

    Output :
    --------
    out : the json schema dictionnary
    """

    def translate_docudesc(str_):
        """Translate a docu/desc of opentea into documentation.

        Parameter :
        -----------
        str_ : the openTea string documentation

        Output :
        --------
        out : the json schema documentation file

        """
        out = str(str_)
        return out

    out = {}
    out['name'] = docu_or_desc
    out['ot_type'] = docu_or_desc
    out['title'] = ''
    out['type'] = 'string'
    out['default'] = translate_docudesc(str_docudesc)
    return out


def choice_node(dict_):
    """Import a choice node.

    Parameter :
    -----------
    dict_ : the openTea specification of a choice

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    for item in ('name', 'title'):
        out[item] = dict_[item]

    out['type'] = 'string'
    out['ot_type'] = 'choice'
    if 'default' in dict_:
        out['default'] = dict_['default']
    out['enum'] = []
    out['enum_titles'] = []
    for key in dict_.keys():
        if isinstance(dict_[key], dict) and 'ot_type' in dict_[key].keys() and dict_[key]['ot_type'] == 'option':
            out['enum'].append(key)
            if 'title' in dict_[key]:
                out['enum_titles'].append(dict_[key]['title'])
            else:
                out['enum_titles'].append(key)

    if not out['enum']:
        out['enum'] = [
         'a', 'b', 'c']
        out['enum_titles'] = ['a', 'b', 'c']
    return out


def xor_node(dict_):
    """Import a choice node.

    Parameter :
    -----------
    dict_ : the openTea specification of a oneOf

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    for item in ('name', 'title', 'default'):
        out[item] = dict_[item]

    out['ot_type'] = 'xor'
    out['oneOf'] = []
    for key in dict_.keys():
        if isinstance(dict_[key], dict) and 'ot_type' in dict_[key].keys() and dict_[key]['ot_type'] == 'model':
            option_dict = OrderedDict()
            option_dict['properties'] = {key: model_node(dict_[key])}
            option_dict['required'] = [key]
            out['oneOf'].append(option_dict)

    return out


def status_node(dict_):
    """Import a status node.

    Parameter :
    -----------
    dict_ : the openTea specification of a status

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    out['name'] = dict_['name']
    out['type'] = 'string'
    out['ot_type'] = 'status'
    out['enum'] = ['-1', '0', '1']
    out['enum_titles'] = [dict_['msgerr'],
     dict_['msgunknown'],
     dict_['msgtrue']]
    return out


def multiple_node(dict_):
    """Import a status node.

    Parameter :
    -----------
    dict_ : the openTea specification of a status

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    out['name'] = dict_['name']
    out['type'] = 'array'
    out['ot_type'] = 'multiple'
    for item in ('require', ):
        if item in dict_.keys():
            out[item] = dict_[item]

    out['items'] = {}
    out['items']['title'] = dict_['title']
    out['items']['properties'] = {}
    for key in dict_:
        if key in ('name', 'title', 'require', 'subcolumns', 'ot_type'):
            continue
        if isinstance(dict_[key], dict):
            if 'ot_type' in dict_[key].keys():
                if dict_[key]['ot_type'] == 'model':
                    out['items']['properties'][key] = model_node(dict_[key])
                else:
                    if dict_[key]['ot_type'] == 'xor':
                        out['items']['properties'][key] = xor_node(dict_[key])
                    else:
                        if dict_[key]['ot_type'] == 'status':
                            out['items']['properties'][key] = status_node(dict_[key])
                        else:
                            if dict_[key]['ot_type'] == 'param':
                                out['items']['properties'][key] = param_node(dict_[key])
                            else:
                                raise NotImplementedError('Mutiple node : could not translate key -' + key + '- ot_type :' + dict_[key]['ot_type'])
        else:
            raise NotImplementedError('Mutiple node : could not translate key -' + key + '-')

    return out


def view3d_node(dict_):
    """Import a view3d node.

    Parameter :
    -----------
    dict_ : the openTea specification of a view3d

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    out['name'] = dict_['name']
    out['type'] = 'string'
    out['ot_type'] = 'view3d'
    out['default'] = 'Not Implemented!'
    return out


def include_node(dict_):
    """Import a view3d node.

    Parameter :
    -----------
    dict_ : the openTea specification of an include node

    Output :
    --------
    out : the json schema dictionnary
    """
    out = {}
    out['name'] = 'include'
    out['ot_address'] = dict_['address']
    return out
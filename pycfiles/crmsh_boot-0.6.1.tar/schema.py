# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/schema.py
# Compiled at: 2016-05-04 07:56:27
from . import config
import re
from .pacemaker import CrmSchema, PacemakerError
from .msg import common_err

def is_supported(name):
    """
    Check if the given name is a supported schema name
    A short form is also accepted where the prefix
    pacemaker- is implied.

    Revision: The pacemaker schema version now
    changes too often for a strict check to make sense.
    Lets just check look for schemas we know we don't
    support.
    """
    name = re.match('pacemaker-(\\d+\\.\\d+)$', name)
    if name:
        return float(name.group(1)) > 0.9
    return True


def get_attrs(schema, name):
    return {'a': schema.get_elem_attrs(name, 'a'), 
       'r': schema.get_elem_attrs(name, 'r'), 
       'o': schema.get_elem_attrs(name, 'o')}


def get_subs(schema, name):
    return {'a': schema.get_sub_elems(name, 'a'), 
       'r': schema.get_sub_elems(name, 'r'), 
       'o': schema.get_sub_elems(name, 'o')}


def get_attr_details_d(schema, name):
    d = {}
    for attr_obj in schema.get_elem_attr_objs(name):
        attr_name = schema.get_obj_name(attr_obj)
        d[attr_name] = {'t': schema.get_attr_type(attr_obj), 
           'v': schema.get_attr_values(attr_obj), 
           'd': schema.get_attr_default(attr_obj)}

    return d


def get_attr_details_l(schema, name):
    l = []
    for attr_obj in schema.get_elem_attr_objs(name):
        l.append({'n': schema.get_obj_name(attr_obj), 
           't': schema.get_attr_type(attr_obj), 
           'v': schema.get_attr_values(attr_obj), 
           'd': schema.get_attr_default(attr_obj)})

    return l


_cache_funcs = {'attr': get_attrs, 
   'sub': get_subs, 
   'attr_det': get_attr_details_d, 
   'attr_det_l': get_attr_details_l}
_crm_schema = None
_store = {}

def reset():
    global _store
    _store = {}


def _load_schema(cib):
    return CrmSchema(cib, config.path.crm_dtd_dir)


def init_schema(cib):
    global _crm_schema
    try:
        _crm_schema = _load_schema(cib)
    except PacemakerError as msg:
        common_err(msg)

    reset()


def test_schema(cib):
    try:
        crm_schema = _load_schema(cib)
    except PacemakerError as msg:
        common_err(msg)
        return

    return crm_schema.validate_name


def validate_name():
    if _crm_schema is None:
        return 'pacemaker-2.0'
    else:
        return _crm_schema.validate_name


def get(t, name, subset=None):
    if _crm_schema is None:
        return []
    else:
        if t not in _store:
            _store[t] = {}
        if name not in _store[t]:
            _store[t][name] = _cache_funcs[t](_crm_schema, name)
        if subset:
            return _store[t][name][subset]
        return _store[t][name]
        return


def rng_attr_values(el_name, attr_name):
    """"""
    try:
        return get('attr_det', el_name)[attr_name]['v']
    except:
        return []


def rng_attr_values_l(el_name, attr_name):
    """"""
    l = get('attr_det_l', el_name)
    l2 = []
    for el in l:
        if el['n'] == attr_name:
            l2 += el['v']

    return l2


def rng_xpath(xpath, namespaces=None):
    if _crm_schema is None:
        return []
    else:
        return _crm_schema.rng_xpath(xpath, namespaces=namespaces)
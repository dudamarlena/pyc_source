# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/configuration/sources/from_dict.py
# Compiled at: 2020-04-25 10:46:39
# Size of source mod 2**32: 2250 bytes
import copy, importlib
from satella.coding.recast_exceptions import rethrow_as
from satella.coding.decorators import for_argument
from satella.configuration import sources
from satella.configuration.sources.base import BaseSource
from satella.exceptions import ConfigurationError
__all__ = [
 'load_source_from_dict',
 'load_source_from_list']

def handle_import(dct: dict):

    def convert(v):
        if 'cast_before' in dct:
            v = EXTRA_TYPES[dct['cast_before']['type']](dct['cast_before'])(v)
        return getattr(importlib.import_module(dct['module']), dct['attribute'])(v)

    return convert


EXTRA_TYPES = {'binary':lambda dct: dct['value'].encode(dct.get('encoding', 'ascii')), 
 'lambda':lambda dct: eval('lambda x: ' + dct['operation'], globals(), locals()), 
 'import':handle_import}

@rethrow_as(Exception, ConfigurationError)
@for_argument(copy.copy)
def load_source_from_dict(dct: dict) -> BaseSource:
    """
    dct has a form of

    {
        "type": "BaseSource",
        "args": []  # optional
        ... kwargs
    }

    :raises ConfigurationError: upon failure to instantiate
    """
    type_ = dct.pop('type')
    args = dct.pop('args', [])
    optional = dct.pop('optional', False)

    def to_arg(arg):
        if isinstance(arg, dict):
            if 'type' in arg:
                a_type = arg['type']
                if a_type in EXTRA_TYPES:
                    return EXTRA_TYPES[a_type](arg)
                if a_type in sources.__dict__:
                    return load_source_from_dict(arg)
                raise ValueError('unrecognized argument type %s' % (arg['type'],))
        else:
            return arg

    args = map(to_arg, args)
    kwargs = {k:to_arg(v) for k, v in dct.items()}
    s = (sources.__dict__[type_])(*args, **kwargs)
    if optional:
        s = sources.OptionalSource(s)
    return s


def load_source_from_list(obj: list) -> 'sources.MergingSource':
    """
    Builds a MergingSource from dict-ed objects
    """
    return (sources.MergingSource)(*map(load_source_from_dict, obj))
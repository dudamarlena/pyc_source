# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jan/repos/warlock/warlock/core.py
# Compiled at: 2019-05-18 13:29:13
"""Core Warlock functionality"""
import copy
from . import model

def model_factory(schema, resolver=None, base_class=model.Model, name=None):
    """Generate a model class based on the provided JSON Schema

    :param schema: dict representing valid JSON schema
    :param name: A name to give the class, if `name` is not in `schema`
    """
    schema = copy.deepcopy(schema)
    resolver = resolver

    class Model(base_class):

        def __init__(self, *args, **kwargs):
            self.__dict__['schema'] = schema
            self.__dict__['resolver'] = resolver
            base_class.__init__(self, *args, **kwargs)

    if resolver is not None:
        Model.resolver = resolver
    if name is not None:
        Model.__name__ = name
    elif 'name' in schema:
        Model.__name__ = str(schema['name'])
    return Model
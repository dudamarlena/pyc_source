# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camsaxs/loader.py
# Compiled at: 2018-11-19 17:42:50
# Size of source mod 2**32: 1582 bytes
import os, yaml
from collections import OrderedDict
_fixed = {'name':'Fixed', 
 'value':True,  'type':'bool'}
_bounds = [{'name':'Lower',  'value':'-∞'}, {'name':'Upper',  'value':'∞'}]
_bounded = {'name':'Bounded',  'value':False,  'type':'bool',  'children':_bounds, 
 'visible':False,  'enabled':False}

class XicamParameter(yaml.YAMLObject):
    yaml_tag = '!YMLParameter'

    def __init__(self, name, description, value, units, **kwags):
        self.name = name
        self.description = description
        self.value = value
        self.units = units
        self.fixed = True
        self.bounds = [None, None]

    def __repr__(self):
        return '%s (%r, value=%r, units=%r)' % (
         self.__class__.__name__, self.name, self.value, self.units)

    @classmethod
    def from_yaml(cls, loader, node):
        opts = loader.construct_mapping(node)
        return cls(**opts)


def load_models():
    path, _ = os.path.split(os.path.realpath(__file__))
    config = os.path.join(path, 'config.yml')
    if not os.path.isfile(config):
        raise ImportWarning('Unable to load config file')
        return
    with open(config) as (fp):
        yml = yaml.load(fp)
    model_tree = OrderedDict()
    for key, val in yml.items():
        models = OrderedDict()
        for name, params in val.items():
            _params = [p['param'] for p in params]
            models[name] = {'params': _params}

        model_tree[key] = models

    return model_tree
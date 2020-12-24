# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/utils.py
# Compiled at: 2018-08-17 07:02:31
import six, yaml, uuid, re
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    from yaml import CLoader as YamlLoader, CDumper as YamlDumper
except ImportError:
    from yaml import Loader as YamlLoader, Dumper as YamlDumper

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
dict_representer = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
dict_constructor = lambda loader, node: OrderedDict(loader.construct_pairs(node))
YamlDumper.add_representer(OrderedDict, dict_representer)
YamlLoader.add_constructor(_mapping_tag, dict_constructor)
__all__ = [
 'setdefaultdict',
 'memoized_property',
 'memoized',
 'yamp_load',
 'yamp_dump',
 'yaml',
 'OrderedDict']

def yamp_dump(data):
    return yaml.dump(data, Dumper=YamlDumper, default_flow_style=False, indent=4)


def yamp_load(content):
    return yaml.load(content, Loader=YamlLoader)


def setdefaultdict(_dict, name=None, default={}, ordered=False):
    if name:
        value = _dict.setdefault(name, default)
    else:
        value = _dict
    if not isinstance(value, dict):
        if name:
            value = _dict[name] = default
        else:
            value = default
    if ordered:
        value = OrderedDict(value)
    return value


class memoized_property(object):

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.__get = fget
        self.__set = fset
        self.__del = fdel
        self.__doc__ = doc
        self.___uuid = str(uuid.uuid1())

    def __get__(self, inst, cls=None):
        if not hasattr(inst, self.___uuid):
            setattr(inst, self.___uuid, self.__get(inst))
        return getattr(inst, self.___uuid)


class memoized(object):

    def __init__(self, fct):
        self.___fct = fct
        self.___uuid = str(uuid.uuid1())

    def __get__(self, inst, cls=None):
        self.___inst = inst
        return self

    def __call__(self, inst, *args, **kwargs):
        if not hasattr(inst, self.___uuid):
            setattr(inst, self.___uuid, self.___fct(inst, *args, **kwargs))
        return getattr(inst, self.___uuid)


def combine(elm1, elm2, *args):
    if elm1 is None and elm2 is None:
        return
    else:
        if elm1 is None and isinstance(elm2, six.string_types):
            elm1 = elm2
        else:
            if elm1 is None and isinstance(elm2, dict):
                elm1 = elm2
                combine(elm1, elm2)
            elif elm1 is None and isinstance(elm2, list):
                elm1 = elm2
                combine(elm1, elm2)
            elif isinstance(elm1, dict) and isinstance(elm2, dict):
                for key2, val2 in elm2.items():
                    val1 = elm1.get(key2, val2)
                    elm1[key2] = combine(val1, val2)

            elif isinstance(elm1, list) and isinstance(elm2, list):
                elm1 = list(set(elm2 + elm1))
            elif isinstance(elm1, list) and elm2 is None:
                for ind1, val1 in enumerate(elm1):
                    elm1[ind1] = combine(ind1, None)

            if args:
                return combine(elm1, **args)
        return elm1
        return
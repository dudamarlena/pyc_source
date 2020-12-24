# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/saltcontainermap/extmods/lazy_yaml.py
# Compiled at: 2017-11-28 12:39:26
from __future__ import unicode_literals, absolute_import
from dockermap.map.yaml import yaml
from msgpack import ExtType
from salt.utils.yamlloader import SaltYamlSafeLoader
_ext_types = {}

def render(yaml_data, saltenv=b'base', sls=b'', **kws):
    config_get = __salt__[b'config.get']
    _ext_types[b'pillar'] = config_get(b'lazy_yaml.ext_code_pillar', 10)
    _ext_types[b'grain'] = config_get(b'lazy_yaml.ext_code_grain', 11)
    if config_get(b'lazy_yaml.skip_render', False):
        return yaml_data
    if not isinstance(yaml_data, basestring):
        yaml_data = yaml_data.read()
    data = yaml.load(yaml_data, Loader=SaltYamlSafeLoader)
    if data:
        return data
    return {}


def expand_pillar_lazy(loader, node):
    """
    Substitutes a variable read from a YAML node with a MsgPack ExtType value referring to data stored in a pillar.

    :param loader: YAML loader.
    :type loader: yaml.loader.SafeLoader
    :param node: Document node.
    :type node: ScalarNode
    :return: Corresponding value stored in the pillar.
    :rtype: msgpack.ExtType
    """
    val = loader.construct_scalar(node)
    return ExtType(_ext_types[b'pillar'], val.encode(b'utf-8'))


def expand_grain_lazy(loader, node):
    """
    Substitutes a variable read from a YAML node with a MsgPack ExtType value referring to data stored in a grain.

    :param loader: YAML loader.
    :type loader: yaml.loader.SafeLoader
    :param node: Document node.
    :type node: ScalarNode
    :return: Corresponding value stored in the grain.
    :rtype: msgpack.ExtType
    """
    val = loader.construct_scalar(node)
    return ExtType(_ext_types[b'grain'], val.encode(b'utf-8'))


yaml.add_constructor(b'!pillar', expand_pillar_lazy, SaltYamlSafeLoader)
yaml.add_constructor(b'!grain', expand_grain_lazy, SaltYamlSafeLoader)
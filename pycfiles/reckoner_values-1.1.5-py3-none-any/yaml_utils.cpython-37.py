# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jim/workspace/python_module_helm_values/reckoner_values/yaml_utils.py
# Compiled at: 2019-07-22 08:47:19
# Size of source mod 2**32: 1093 bytes
from collections import OrderedDict
import oyaml as yaml, json
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):

    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return yaml.load(stream, OrderedLoader)


def olddata_to_yaml(data):
    return yaml.dump(data, Dumper=Dumper)


def data_to_yaml(data, **options):
    opts = dict(indent=4, default_flow_style=False)
    opts.update(options)
    if 'Dumper' not in opts:
        return (yaml.safe_dump)(data, **opts)
    return (yaml.dump)(data, **opts)
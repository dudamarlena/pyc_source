# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/yamlhelper.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3241 bytes
"""
YAML helper, sourced from the AWS CLI

https://github.com/aws/aws-cli/blob/develop/awscli/customizations/cloudformation/yamlhelper.py
"""
import json
from botocore.compat import OrderedDict
import yaml
from yaml.resolver import ScalarNode, SequenceNode

def intrinsics_multi_constructor(loader, tag_prefix, node):
    """
    YAML constructor to parse CloudFormation intrinsics.
    This will return a dictionary with key being the instrinsic name
    """
    tag = node.tag[1:]
    prefix = 'Fn::'
    if tag in ('Ref', 'Condition'):
        prefix = ''
    cfntag = prefix + tag
    if tag == 'GetAtt' and isinstance(node.value, str):
        value = node.value.split('.', 1)
    else:
        if isinstance(node, ScalarNode):
            value = loader.construct_scalar(node)
        else:
            if isinstance(node, SequenceNode):
                value = loader.construct_sequence(node)
            else:
                value = loader.construct_mapping(node)
    return {cfntag: value}


def _dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


def yaml_dump(dict_to_dump):
    """
    Dumps the dictionary as a YAML document
    :param dict_to_dump:
    :return:
    """
    FlattenAliasDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(dict_to_dump, default_flow_style=False, Dumper=FlattenAliasDumper)


def _dict_constructor(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


def yaml_parse(yamlstr):
    """Parse a yaml string"""
    try:
        return json.loads(yamlstr, object_pairs_hook=OrderedDict)
    except ValueError:
        yaml.SafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _dict_constructor)
        yaml.SafeLoader.add_multi_constructor('!', intrinsics_multi_constructor)
        return yaml.safe_load(yamlstr)


class FlattenAliasDumper(yaml.SafeDumper):

    def ignore_aliases(self, data):
        return True
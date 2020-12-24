# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ycfg/yaml.py
# Compiled at: 2018-04-16 00:21:31
# Size of source mod 2**32: 2368 bytes
import collections, yaml, yaml.constructor

class ordered_dict_loader(yaml.Loader):
    __doc__ = '\n        A YAML loader that loads mappings into ordered dictionaries.\n\n        See also: https://gist.github.com/enaeseth/844388\n    '

    def __init__(self, *args, **kwargs):
        (yaml.Loader.__init__)(self, *args, **kwargs)
        self.add_constructor('tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor('tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = collections.OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None, 'expected a mapping node, but found {}'.format(node.id), node.start_mark)
        mapping = collections.OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as ex:
                raise yaml.constructor.ConstructorError('while constructing a mapping', node.start_mark, 'found unacceptable key `{}`'.format(ex), key_node.start_mark)

            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping
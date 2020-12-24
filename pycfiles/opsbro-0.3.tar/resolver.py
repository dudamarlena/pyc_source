# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ruamel/yaml/resolver.py
# Compiled at: 2017-07-27 07:36:53
from __future__ import absolute_import
import re
try:
    from .error import *
    from .nodes import *
    from .compat import string_types
except (ImportError, ValueError):
    from ruamel.yaml.error import *
    from ruamel.yaml.nodes import *
    from ruamel.yaml.compat import string_types

__all__ = ['BaseResolver', 'Resolver', 'VersionedResolver']
_DEFAULT_VERSION = (1, 2)

class ResolverError(YAMLError):
    pass


class BaseResolver(object):
    DEFAULT_SCALAR_TAG = 'tag:yaml.org,2002:str'
    DEFAULT_SEQUENCE_TAG = 'tag:yaml.org,2002:seq'
    DEFAULT_MAPPING_TAG = 'tag:yaml.org,2002:map'
    yaml_implicit_resolvers = {}
    yaml_path_resolvers = {}

    def __init__(self):
        self._loader_version = None
        self.resolver_exact_paths = []
        self.resolver_prefix_paths = []
        return

    @classmethod
    def add_implicit_resolver(cls, tag, regexp, first):
        if 'yaml_implicit_resolvers' not in cls.__dict__:
            cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()
        if first is None:
            first = [
             None]
        for ch in first:
            cls.yaml_implicit_resolvers.setdefault(ch, []).append((
             tag, regexp))

        return

    @classmethod
    def add_path_resolver(cls, tag, path, kind=None):
        if 'yaml_path_resolvers' not in cls.__dict__:
            cls.yaml_path_resolvers = cls.yaml_path_resolvers.copy()
        new_path = []
        for element in path:
            if isinstance(element, (list, tuple)):
                if len(element) == 2:
                    node_check, index_check = element
                elif len(element) == 1:
                    node_check = element[0]
                    index_check = True
                else:
                    raise ResolverError('Invalid path element: %s' % element)
            else:
                node_check = None
                index_check = element
            if node_check is str:
                node_check = ScalarNode
            elif node_check is list:
                node_check = SequenceNode
            elif node_check is dict:
                node_check = MappingNode
            elif node_check not in [ScalarNode, SequenceNode, MappingNode] and not isinstance(node_check, string_types) and node_check is not None:
                raise ResolverError('Invalid node checker: %s' % node_check)
            if not isinstance(index_check, (string_types, int)) and index_check is not None:
                raise ResolverError('Invalid index checker: %s' % index_check)
            new_path.append((node_check, index_check))

        if kind is str:
            kind = ScalarNode
        elif kind is list:
            kind = SequenceNode
        elif kind is dict:
            kind = MappingNode
        elif kind not in [ScalarNode, SequenceNode, MappingNode] and kind is not None:
            raise ResolverError('Invalid node kind: %s' % kind)
        cls.yaml_path_resolvers[(tuple(new_path), kind)] = tag
        return

    def descend_resolver(self, current_node, current_index):
        if not self.yaml_path_resolvers:
            return
        exact_paths = {}
        prefix_paths = []
        if current_node:
            depth = len(self.resolver_prefix_paths)
            for path, kind in self.resolver_prefix_paths[(-1)]:
                if self.check_resolver_prefix(depth, path, kind, current_node, current_index):
                    if len(path) > depth:
                        prefix_paths.append((path, kind))
                    else:
                        exact_paths[kind] = self.yaml_path_resolvers[(path,
                         kind)]

        else:
            for path, kind in self.yaml_path_resolvers:
                if not path:
                    exact_paths[kind] = self.yaml_path_resolvers[(path, kind)]
                else:
                    prefix_paths.append((path, kind))

        self.resolver_exact_paths.append(exact_paths)
        self.resolver_prefix_paths.append(prefix_paths)

    def ascend_resolver(self):
        if not self.yaml_path_resolvers:
            return
        self.resolver_exact_paths.pop()
        self.resolver_prefix_paths.pop()

    def check_resolver_prefix(self, depth, path, kind, current_node, current_index):
        node_check, index_check = path[(depth - 1)]
        if isinstance(node_check, string_types):
            if current_node.tag != node_check:
                return
        elif node_check is not None:
            if not isinstance(current_node, node_check):
                return
        if index_check is True and current_index is not None:
            return
        else:
            if (index_check is False or index_check is None) and current_index is None:
                return
            if isinstance(index_check, string_types):
                if not (isinstance(current_index, ScalarNode) and index_check == current_index.value):
                    return
            elif isinstance(index_check, int) and not isinstance(index_check, bool):
                if index_check != current_index:
                    return
            return True

    def resolve(self, kind, value, implicit):
        if kind is ScalarNode and implicit[0]:
            if value == '':
                resolvers = self.yaml_implicit_resolvers.get('', [])
            else:
                resolvers = self.yaml_implicit_resolvers.get(value[0], [])
            resolvers += self.yaml_implicit_resolvers.get(None, [])
            for tag, regexp in resolvers:
                if regexp.match(value):
                    return tag

            implicit = implicit[1]
        if self.yaml_path_resolvers:
            exact_paths = self.resolver_exact_paths[(-1)]
            if kind in exact_paths:
                return exact_paths[kind]
            if None in exact_paths:
                return exact_paths[None]
        if kind is ScalarNode:
            return self.DEFAULT_SCALAR_TAG
        else:
            if kind is SequenceNode:
                return self.DEFAULT_SEQUENCE_TAG
            if kind is MappingNode:
                return self.DEFAULT_MAPPING_TAG
            return

    @property
    def processing_version(self):
        return


class Resolver(BaseResolver):
    pass


Resolver.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile('^(?:yes|Yes|YES|no|No|NO\n    |true|True|TRUE|false|False|FALSE\n    |on|On|ON|off|Off|OFF)$', re.X), list('yYnNtTfFoO'))
Resolver.add_implicit_resolver('tag:yaml.org,2002:float', re.compile('^(?:\n     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?\n    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)\n    |\\.[0-9_]+(?:[eE][-+][0-9]+)?\n    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*\n    |[-+]?\\.(?:inf|Inf|INF)\n    |\\.(?:nan|NaN|NAN))$', re.X), list('-+0123456789.'))
Resolver.add_implicit_resolver('tag:yaml.org,2002:int', re.compile('^(?:[-+]?0b[0-1_]+\n    |[-+]?0o?[0-7_]+\n    |[-+]?(?:0|[1-9][0-9_]*)\n    |[-+]?0x[0-9a-fA-F_]+\n    |[-+]?[1-9][0-9_]*(?::[0-5]?[0-9])+)$', re.X), list('-+0123456789'))
Resolver.add_implicit_resolver('tag:yaml.org,2002:merge', re.compile('^(?:<<)$'), [
 '<'])
Resolver.add_implicit_resolver('tag:yaml.org,2002:null', re.compile('^(?: ~\n    |null|Null|NULL\n    | )$', re.X), [
 '~', 'n', 'N', ''])
Resolver.add_implicit_resolver('tag:yaml.org,2002:timestamp', re.compile('^(?:[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\n    |[0-9][0-9][0-9][0-9] -[0-9][0-9]? -[0-9][0-9]?\n    (?:[Tt]|[ \\t]+)[0-9][0-9]?\n    :[0-9][0-9] :[0-9][0-9] (?:\\.[0-9]*)?\n    (?:[ \\t]*(?:Z|[-+][0-9][0-9]?(?::[0-9][0-9])?))?)$', re.X), list('0123456789'))
Resolver.add_implicit_resolver('tag:yaml.org,2002:value', re.compile('^(?:=)$'), [
 '='])
Resolver.add_implicit_resolver('tag:yaml.org,2002:yaml', re.compile('^(?:!|&|\\*)$'), list('!&*'))
implicit_resolvers = [
 ([(1, 2)],
  'tag:yaml.org,2002:bool',
  re.compile('^(?:true|True|TRUE|false|False|FALSE)$', re.X),
  list('tTfF')),
 (
  [
   (1, 1)],
  'tag:yaml.org,2002:bool',
  re.compile('^(?:yes|Yes|YES|no|No|NO\n        |true|True|TRUE|false|False|FALSE\n        |on|On|ON|off|Off|OFF)$', re.X),
  list('yYnNtTfFoO')),
 (
  [
   (1, 2), (1, 1)],
  'tag:yaml.org,2002:float',
  re.compile('^(?:\n         [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?\n        |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)\n        |\\.[0-9_]+(?:[eE][-+][0-9]+)?\n        |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*\n        |[-+]?\\.(?:inf|Inf|INF)\n        |\\.(?:nan|NaN|NAN))$', re.X),
  list('-+0123456789.')),
 (
  [
   (1, 2)],
  'tag:yaml.org,2002:int',
  re.compile('^(?:[-+]?0b[0-1_]+\n        |[-+]?0o?[0-7_]+\n        |[-+]?(?:0|[1-9][0-9_]*)\n        |[-+]?0x[0-9a-fA-F_]+)$', re.X),
  list('-+0123456789')),
 (
  [
   (1, 1)],
  'tag:yaml.org,2002:int',
  re.compile('^(?:[-+]?0b[0-1_]+\n        |[-+]?0o?[0-7_]+\n        |[-+]?(?:0|[1-9][0-9_]*)\n        |[-+]?0x[0-9a-fA-F_]+\n        |[-+]?[1-9][0-9_]*(?::[0-5]?[0-9])+)$', re.X),
  list('-+0123456789')),
 (
  [
   (1, 2), (1, 1)],
  'tag:yaml.org,2002:merge',
  re.compile('^(?:<<)$'),
  [
   '<']),
 (
  [
   (1, 2), (1, 1)],
  'tag:yaml.org,2002:null',
  re.compile('^(?: ~\n        |null|Null|NULL\n        | )$', re.X),
  [
   '~', 'n', 'N', '']),
 (
  [
   (1, 2), (1, 1)],
  'tag:yaml.org,2002:timestamp',
  re.compile('^(?:[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\n        |[0-9][0-9][0-9][0-9] -[0-9][0-9]? -[0-9][0-9]?\n        (?:[Tt]|[ \\t]+)[0-9][0-9]?\n        :[0-9][0-9] :[0-9][0-9] (?:\\.[0-9]*)?\n        (?:[ \\t]*(?:Z|[-+][0-9][0-9]?(?::[0-9][0-9])?))?)$', re.X),
  list('0123456789')),
 (
  [
   (1, 2), (1, 1)],
  'tag:yaml.org,2002:value',
  re.compile('^(?:=)$'),
  [
   '=']),
 (
  [
   (1, 2), (1, 1)],
  'tag:yaml.org,2002:yaml',
  re.compile('^(?:!|&|\\*)$'),
  list('!&*'))]

class VersionedResolver(BaseResolver):
    """
    contrary to the "normal" resolver, the smart resolver delays loading
    the pattern matching rules. That way it can decide to load 1.1 rules
    or the (default) 1.2 that no longer support octal without 0o, sexagesimals
    and Yes/No/On/Off booleans.
    """

    def __init__(self, version=None):
        BaseResolver.__init__(self)
        self._loader_version = self.get_loader_version(version)
        self._version_implicit_resolver = {}

    def add_version_implicit_resolver(self, version, tag, regexp, first):
        if first is None:
            first = [
             None]
        impl_resolver = self._version_implicit_resolver.setdefault(version, {})
        for ch in first:
            impl_resolver.setdefault(ch, []).append((tag, regexp))

        return

    def get_loader_version(self, version):
        if version is None or isinstance(version, tuple):
            return version
        if isinstance(version, list):
            return tuple(version)
        else:
            return tuple(map(int, version.split('.')))

    @property
    def resolver(self):
        """
        select the resolver based on the version we are parsing
        """
        version = self.processing_version
        if version not in self._version_implicit_resolver:
            for x in implicit_resolvers:
                if version in x[0]:
                    self.add_version_implicit_resolver(version, x[1], x[2], x[3])

        return self._version_implicit_resolver[version]

    def resolve(self, kind, value, implicit):
        if kind is ScalarNode and implicit[0]:
            if value == '':
                resolvers = self.resolver.get('', [])
            else:
                resolvers = self.resolver.get(value[0], [])
            resolvers += self.resolver.get(None, [])
            for tag, regexp in resolvers:
                if regexp.match(value):
                    return tag

            implicit = implicit[1]
        if self.yaml_path_resolvers:
            exact_paths = self.resolver_exact_paths[(-1)]
            if kind in exact_paths:
                return exact_paths[kind]
            if None in exact_paths:
                return exact_paths[None]
        if kind is ScalarNode:
            return self.DEFAULT_SCALAR_TAG
        else:
            if kind is SequenceNode:
                return self.DEFAULT_SEQUENCE_TAG
            if kind is MappingNode:
                return self.DEFAULT_MAPPING_TAG
            return

    @property
    def processing_version(self):
        try:
            version = self.yaml_version
        except AttributeError:
            version = self.use_version

        if version is None:
            version = self._loader_version
            if version is None:
                version = _DEFAULT_VERSION
        return version
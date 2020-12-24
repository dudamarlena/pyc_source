# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/config/yaml.py
# Compiled at: 2020-05-02 23:35:41
# Size of source mod 2**32: 5401 bytes
"""Application configuration classes parsed from YAML files.

"""
__author__ = 'Paul Landes'
import logging, sys
from pprint import pprint
import copy, yaml
from zensols.config import Configurable
logger = logging.getLogger(__name__)

class YamlConfig(Configurable):
    __doc__ = 'Just like zensols.actioncli.Config but parse configuration from YAML files.\n    Variable substitution works just like ini files, but you can set what\n    delimiter to use and keys are the paths of the data in the hierarchy\n    separated by dots.\n\n    See the test cases for example.\n\n    '
    CLASS_VER = 0

    def __init__(self, config_file=None, default_vars=None, delimiter='$', default_expect=False):
        super().__init__(config_file, default_expect)
        self.default_vars = default_vars if default_vars else {}
        self.delimiter = delimiter

    @classmethod
    def _is_primitive(cls, obj):
        return isinstance(obj, str) or isinstance(obj, list) or isinstance(obj, bool)

    def _parse(self):
        with open(self.config_file) as (f):
            content = f.read()
        struct = yaml.load(content, yaml.FullLoader)
        context = {}
        context.update(self.default_vars)

        def flatten(path, n):
            logger.debug('path: {}, n: <{}>'.format(path, n))
            logger.debug('context: <{}>'.format(context))
            if self._is_primitive(n):
                context[path] = n
            else:
                if isinstance(n, dict):
                    for k, v in n.items():
                        k = path + '.' + k if len(path) else k
                        flatten(k, v)

                else:
                    raise ValueError('unknown yaml type {}: {}'.format(type(n), n))

        flatten('', struct)
        self._all_keys = copy.copy(list(context.keys()))
        return (content, struct, context)

    def _make_class(self):
        class_name = 'YamlTemplate{}'.format(self.CLASS_VER)
        self.CLASS_VER += 1
        code = 'from string import Template\nclass ' + class_name + "(Template):\n     idpattern = r'[a-z][_a-z0-9.]*'\n     delimiter = '" + self.delimiter + "'"
        exec(code)
        cls = eval(class_name)
        return cls

    def _compile(self):
        content, struct, context = self._parse()
        prev = None
        cls = self._make_class()
        while prev != content:
            prev = content
            content = cls(content).substitute(context)

        return yaml.load(content, yaml.FullLoader)

    @property
    def config(self):
        if not hasattr(self, '_config'):
            self._config = self._compile()
        return self._config

    def write(self, writer=sys.stdout):
        pprint(self.config, writer)

    def _option(self, name):

        def find(n, path, name):
            logger.debug('search: n={}, path={}, name={}'.format(n, path, name))
            if path == name:
                logger.debug('found: <{}>'.format(n))
                return n
            if isinstance(n, dict):
                for k, v in n.items():
                    k = path + '.' + k if len(path) else k
                    v = find(v, k, name)
                    if v is not None:
                        logger.debug('found {} -> {}'.format(name, v))
                        return v

                logger.debug('not found: {}'.format(name))

        return find(self.config, '', name)

    def _get_option(self, name, expect=None):
        node = self._option(name)
        if self._is_primitive(node):
            return node
        if self.default_vars is not None:
            if name in self.default_vars:
                return self.default_vars[name]
        if self._narrow_expect(expect):
            raise ValueError('no such option: {}'.format(name))

    @property
    def options(self):
        if not hasattr(self, '_options'):
            self.config
            self._options = {}
            for k in self._all_keys:
                self._options[k] = self._get_option(k, expect=True)

        return self._options

    def get_option(self, name, expect=None):
        if self.default_vars:
            if name in self.default_vars:
                return self.default_vars[name]
        ops = self.options
        if name in ops:
            return ops[name]
        if self._narrow_expect(expect):
            raise ValueError('no such option: {}'.format(name))

    def get_options(self, name, expect=None):
        if self.default_vars:
            if name in self.default_vars:
                return self.default_vars[name]
        node = self._option(name)
        if not isinstance(node, str) or isinstance(node, list):
            return node
        if name in self.default_vars:
            return self.default_vars[name]
        if self._narrow_expect(expect):
            raise ValueError('no such option: {}'.format(name))
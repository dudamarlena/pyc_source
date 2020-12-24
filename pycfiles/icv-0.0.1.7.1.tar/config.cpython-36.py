# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/config.py
# Compiled at: 2019-04-21 04:19:39
# Size of source mod 2**32: 5112 bytes
import os.path as osp, sys
from argparse import ArgumentParser
from collections import Iterable
from importlib import import_module
from addict import Dict
from .misc import check_file_exist

class ConfigDict(Dict):

    def __missing__(self, name):
        raise KeyError(name)

    def __getattr__(self, name):
        try:
            value = super(ConfigDict, self).__getattr__(name)
        except KeyError:
            ex = AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))
        except Exception as e:
            ex = e
        else:
            return value
        raise ex


def add_args(parser, cfg, prefix=''):
    for k, v in cfg.items():
        if isinstance(v, str):
            parser.add_argument('--' + prefix + k)
        elif isinstance(v, int):
            parser.add_argument(('--' + prefix + k), type=int)
        elif isinstance(v, float):
            parser.add_argument(('--' + prefix + k), type=float)
        elif isinstance(v, bool):
            parser.add_argument(('--' + prefix + k), action='store_true')
        else:
            if isinstance(v, dict):
                add_args(parser, v, k + '.')
            else:
                if isinstance(v, Iterable):
                    parser.add_argument(('--' + prefix + k), type=(type(v[0])), nargs='+')
                else:
                    print('connot parse key {} of type {}'.format(prefix + k, type(v)))

    return parser


class Config(object):
    __doc__ = 'A facility for config and config files.\n\n    It supports common file formats as configs: python/json/yaml. The interface\n    is the same as a dict object and also allows access config values as\n    attributes.\n\n    Example:\n        >>> cfg = Config(dict(a=1, b=dict(b1=[0, 1])))\n        >>> cfg.a\n        1\n        >>> cfg.b\n        {\'b1\': [0, 1]}\n        >>> cfg.b.b1\n        [0, 1]\n        >>> cfg = Config.fromfile(\'tests/data/config/a.py\')\n        >>> cfg.filename\n        "/home/kchen/projects/mmcv/tests/data/config/a.py"\n        >>> cfg.item4\n        \'test\'\n        >>> cfg\n        "Config [path: /home/kchen/projects/mmcv/tests/data/config/a.py]: "\n        "{\'item1\': [1, 2], \'item2\': {\'a\': 0}, \'item3\': True, \'item4\': \'test\'}"\n\n    '

    @staticmethod
    def fromfile(filename):
        filename = osp.abspath(osp.expanduser(filename))
        check_file_exist(filename)
        if filename.endswith('.py'):
            sys.path.append(osp.dirname(filename))
            module_name = osp.basename(filename)[:-3]
            if '.' in module_name:
                raise ValueError('Dots are not allowed in config file path.')
            mod = import_module(module_name)
            cfg_dict = {name:value for name, value in mod.__dict__.items() if not name.startswith('__') if not name.startswith('__')}
        else:
            if filename.endswith(('.yaml', '.json')):
                import mmcv
                cfg_dict = mmcv.load(filename)
            else:
                raise IOError('Only py/yaml/json type are supported now!')
        return Config(cfg_dict, filename=filename)

    @staticmethod
    def auto_argparser(description=None):
        """Generate argparser from config file automatically (experimental)
        """
        partial_parser = ArgumentParser(description=description)
        partial_parser.add_argument('config', help='config file path')
        cfg_file = partial_parser.parse_known_args()[0].config
        cfg = Config.from_file(cfg_file)
        parser = ArgumentParser(description=description)
        parser.add_argument('config', help='config file path')
        add_args(parser, cfg)
        return (parser, cfg)

    def __init__(self, cfg_dict=None, filename=None):
        if cfg_dict is None:
            cfg_dict = dict()
        else:
            if not isinstance(cfg_dict, dict):
                raise TypeError('cfg_dict must be a dict, but got {}'.format(type(cfg_dict)))
            super(Config, self).__setattr__('_cfg_dict', ConfigDict(cfg_dict))
            super(Config, self).__setattr__('_filename', filename)
            if filename:
                with open(filename, 'r') as (f):
                    super(Config, self).__setattr__('_text', f.read())
            else:
                super(Config, self).__setattr__('_text', '')

    @property
    def filename(self):
        return self._filename

    @property
    def text(self):
        return self._text

    def __repr__(self):
        return 'Config (path: {}): {}'.format(self.filename, self._cfg_dict.__repr__())

    def __len__(self):
        return len(self._cfg_dict)

    def __getattr__(self, name):
        return getattr(self._cfg_dict, name)

    def __getitem__(self, name):
        return self._cfg_dict.__getitem__(name)

    def __setattr__(self, name, value):
        if isinstance(value, dict):
            value = ConfigDict(value)
        self._cfg_dict.__setattr__(name, value)

    def __setitem__(self, name, value):
        if isinstance(value, dict):
            value = ConfigDict(value)
        self._cfg_dict.__setitem__(name, value)

    def __iter__(self):
        return iter(self._cfg_dict)
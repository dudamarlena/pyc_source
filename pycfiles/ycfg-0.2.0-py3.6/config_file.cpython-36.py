# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ycfg/config_file.py
# Compiled at: 2018-04-16 00:19:42
# Size of source mod 2**32: 1844 bytes
from .yaml import ordered_dict_loader
import collections, pathlib, yaml

class items_as_attributes(collections.UserDict):

    def __init__(self, data={}):
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            item = self.data[name]
            if isinstance(item, type(self.data)):
                return items_as_attributes(item)
            else:
                return item
        raise AttributeError('Key {} not found'.format(name))


class config(collections.UserDict):

    def __init__(self, filename: pathlib.Path):
        with filename.open('r') as (f):
            data = yaml.load(f, ordered_dict_loader)
        if data is None:
            self.data = {}
        else:
            if not isinstance(data, collections.OrderedDict):
                raise ValueError('Config file expected to be a YAML dictionary, but it does not: `{}`'.format(filename))
            else:
                self.data = data
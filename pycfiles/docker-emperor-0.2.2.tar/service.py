# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/nodes/service.py
# Compiled at: 2018-08-29 07:25:58
import os, copy, six
from docker_emperor.nodes.environment import Environment
from docker_emperor.utils import setdefaultdict, yaml
__all__ = [
 'Services', 'Service']

class Services(dict):

    def __new__(cls, data, *args, **kwargs):
        return dict.__new__(cls, data, *args, **kwargs)

    def __init__(self, data, *args):
        super(Services, self).__init__(setdefaultdict(data, ordered=True))
        for key, val in self.items():
            self[key] = Service(key, val)

        for arg in args:
            self < arg

    def __gt__(self, inst):
        if not isinstance(inst, self.__class__):
            return self
        return inst < self

    def __lt__(self, inst):
        if not isinstance(inst, self.__class__):
            return self
        for key, val in inst.items():
            if key not in self:
                self[key] = val.copy()
            else:
                self[key] < val

        return self

    def __iter__(self):
        for name, service in self.items():
            yield service

    def __repr__(self):
        return ('<{}: {}>').format(self.__class__.__name__, super(dict, self).__repr__())


yaml.add_representer(Services, lambda dumper, data: dumper.represent_dict(data))

class Service(dict):

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, name, data, *args):
        self.name = name
        super(self.__class__, self).__init__(setdefaultdict(data))
        for default_name, default_class in [
         (
          'environment', Environment)]:
            self[default_name] = default_class(self[default_name])

        for arg in args:
            self < arg

    def __getitem__(self, key):
        return self.get(key)

    def __gt__(self, inst):
        if not isinstance(inst, self.__class__):
            return self
        return inst < self

    def __lt__(self, inst):
        if not isinstance(inst, self.__class__):
            return self
        for key, val in inst.items():
            if key == 'environment':
                self[key] < val
            elif key not in self:
                self[key] = copy.deepcopy(val)
            elif isinstance(self[key], dict) and isinstance(val, dict):
                self[key].update(val)
            elif isinstance(self[key], list) and isinstance(val, list):
                self[key] = list(set(self[key] + copy.deepcopy(val)))
            elif isinstance(val, six.string_types):
                self[key] = val

        return self

    def __repr__(self):
        return ('<{}: {}>').format(self.__class__.__name__, self.name)

    def copy(self):
        return self.__class__(self.name, dict(self))


yaml.add_representer(Service, lambda dumper, data: dumper.represent_dict(data))
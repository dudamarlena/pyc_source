# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/nodes/environment.py
# Compiled at: 2018-10-15 09:45:57
from docker_emperor.utils import yaml
__all__ = [
 'Environment']

class Environment(list):

    def __new__(cls, *args, **kwargs):
        return list.__new__(cls, *args, **kwargs)

    def __init__(self, value, *args, **kwargs):
        if not isinstance(value, list):
            if isinstance(value, dict):
                value = [ ('{}={}').format(key, val) for key, val in value.items() ]
            else:
                value = []
        self.dict = dict()
        for var in value:
            if isinstance(var, tuple):
                key, val = var
            else:
                key, val = var.split('=', 1)
            self.dict[key.strip()] = val.strip()

        super(self.__class__, self).__init__(value)

    def __repr__(self):
        return '<%s: %s\r\n>' % (
         self.__class__.__name__,
         ('').join([ '\r\n\t%s: %s' % (key, val) for key, val in self ]))

    def __gt__(self, inst):
        if not isinstance(inst, self.__class__):
            return self
        return inst < self

    def __lt__(self, inst):
        if not isinstance(inst, self.__class__):
            return self
        del self[:]
        self.dict.update(inst.dict)
        self.__init__(self.dict)
        return self

    def items(self):
        return self.dict.items()

    @property
    def list(self):
        return [ '%s=%s' % (k, v.strip().replace('\\ ', '').replace(' ', '\\ ')) for k, v in self
               ]

    def __dict__(self, key):
        return self.dict

    def get(self, key, default):
        return self[key] or default

    def __getitem__(self, key):
        return self.dict.get(key)

    def __setitem__(self, key, value):
        self.dict[key] = value
        self.__init__(self.dict)

    def __iter__(self):
        for key, val in self.items():
            yield (key, val)

    def __set__(self, value):
        del self[:]
        self[:] = value

    def copy(self):
        return self.__class__(self.dict)


yaml.add_representer(Environment, lambda dumper, data: dumper.represent_list([ ('{}={}').format(key, val) for key, val in data.items() ]))
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/config.py
# Compiled at: 2018-11-28 17:23:39
# Size of source mod 2**32: 3260 bytes
import os, json

class Config:
    __doc__ = '\n    User Config state\n    '

    def __init__(self, config_file=None, **kwargs):
        self._cfg = {}
        if config_file:
            self._config_file = config_file
        else:
            if os.path.isfile('.hscfg'):
                self._config_file = '.hscfg'
            else:
                self._config_file = os.path.expanduser('~/.hscfg')
        if os.path.isfile(self._config_file):
            line_number = 0
            with open(self._config_file) as (f):
                for line in f:
                    line_number += 1
                    s = line.strip()
                    if not s:
                        continue
                    if s[0] == '#':
                        continue
                    fields = s.split('=')
                    if len(fields) < 2:
                        print('config file: {} line: {} is not valid'.format(self._config_file, line_number))
                        continue
                    k = fields[0].strip()
                    v = fields[1].strip()
                    self._cfg[k] = v

        for k in self._cfg.keys():
            if k.upper() in os.environ:
                self._cfg[k] = os.environ[k.upper()]

        for k in kwargs.keys():
            self._cfg[k] = kwargs[k]

    def __getitem__(self, name):
        """ Get a config item  """
        if name not in self._cfg:
            if name.upper() in os.environ:
                self._cfg[name] = os.environ[name.upper()]
            else:
                return
        return self._cfg[name]

    def __setitem__(self, name, obj):
        """ set config item """
        self._cfg[name] = obj

    def __delitem__(self, name):
        """ Delete option. """
        del self._cfg[name]

    def __len__(self):
        return len(self._cfg)

    def __iter__(self):
        """ Iterate over config names """
        keys = self._cfg.keys()
        for key in keys:
            yield key

    def __contains__(self, name):
        return name in self._cfg

    def __repr__(self):
        return json.dumps(self._cfg)

    def keys(self):
        return self._cfg.keys()
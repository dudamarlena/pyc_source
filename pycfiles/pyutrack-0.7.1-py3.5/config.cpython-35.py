# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyutrack/config.py
# Compiled at: 2017-10-28 23:30:53
# Size of source mod 2**32: 1246 bytes
import os, anyconfig
from pyutrack import Credentials

class Config(object):
    DEFAULT_PATH = os.path.expanduser('~/.pyutrack')

    def __init__(self, path=DEFAULT_PATH):
        self._Config__config = {}
        self._Config__path = path
        self._Config__load()

    def __load(self):
        if not os.path.isfile(self._Config__path):
            return
        self._Config__config = anyconfig.load(self._Config__path, ac_parser=not os.path.splitext(self._Config__path)[1] and 'ini').get('pyutrack', {})

    def reload(self):
        self._Config__load()
        return self

    def persist(self):
        anyconfig.dump({'pyutrack': self._Config__config}, self._Config__path, 'ini')

    @property
    def persisted(self):
        return os.path.isfile(self._Config__path)

    @property
    def credentials(self):
        return Credentials(self._Config__config.get('username'), self._Config__config.get('password'))

    @credentials.setter
    def credentials(self, value):
        self._Config__config['username'] = value.username
        self._Config__config['password'] = value.password

    @property
    def base_url(self):
        return self._Config__config.get('base_url')

    @base_url.setter
    def base_url(self, value):
        self._Config__config['base_url'] = value
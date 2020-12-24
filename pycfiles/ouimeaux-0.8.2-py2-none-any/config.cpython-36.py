# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ian/src/github.com/iancmcc/ouimeaux/ouimeaux/config.py
# Compiled at: 2018-08-26 09:51:15
# Size of source mod 2**32: 1646 bytes
import os, yaml

def in_home(*path):
    try:
        from win32com.shell import shellcon, shell
    except ImportError:
        home = os.path.expanduser('~')
    else:
        home = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
    return (os.path.join)(home, *path)


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


class WemoConfiguration(object):

    def __init__(self, filename=None):
        if filename is None:
            ensure_directory(in_home('.wemo'))
            filename = in_home('.wemo', 'config.yml')
        if not os.path.isfile(filename):
            with open(filename, 'w') as (f):
                f.write('\naliases:\n# Shortcuts to longer device names. Uncommenting the following\n# line will allow you to execute \'wemo switch lr on\' instead of\n# \'wemo switch "Living Room Lights" on\'\n#\n#    lr: Living Room Lights\n\n# ip:port to bind to when receiving responses from discovery.\n# The default is first DNS resolution of local host, port 54321\n#\n# bind: 10.1.2.3:9090\n\n# Web app bind address\n#\n# listen: 0.0.0.0:5000\n\n# Require basic authentication (username:password) for the web app\n#\n# auth: admin:password\n')
        with open(filename, 'r') as (cfg):
            self._parsed = yaml.load(cfg)

    @property
    def aliases(self):
        return self._parsed.get('aliases') or {}

    @property
    def bind(self):
        return self._parsed.get('bind', None)

    @property
    def listen(self):
        return self._parsed.get('listen', None)

    @property
    def auth(self):
        return self._parsed.get('auth', None)
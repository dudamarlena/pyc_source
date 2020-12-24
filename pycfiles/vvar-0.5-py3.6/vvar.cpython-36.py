# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vvar\vvar.py
# Compiled at: 2019-10-24 02:49:37
# Size of source mod 2**32: 1454 bytes
from pathlib import Path
import platform, os, pickle

def _get_path():
    location = str(Path.home())
    if platform.system() == 'Linux':
        location += '/.vvar/'
    else:
        location += '\\.vvar\\'
    try:
        os.makedirs(location)
    except:
        pass

    return location


class VVarEnvironment:

    def __getattribute__(self, name):
        content = ''
        try:
            with open(_get_path() + name, 'r') as (f):
                content = f.read()
        except:
            raise AttributeError(name)

        return content

    def __setattr__(self, name, value):
        with open(_get_path() + name, 'w') as (f):
            f.write(value)

    def __delattr__(self, name):
        try:
            os.remove(_get_path() + name)
        except:
            raise AttributeError(name)


class OVarEnvironment:

    def __getattribute__(self, name):
        content = ''
        try:
            with open(_get_path() + name + '.o', 'rb') as (f):
                content = pickle.load(f)
        except:
            raise AttributeError(name)

        return content

    def __setattr__(self, name, value):
        with open(_get_path() + name + '.o', 'wb') as (f):
            pickle.dump(value, f)

    def __delattr__(self, name):
        try:
            os.remove(_get_path() + name + '.o')
        except:
            raise AttributeError(name)


env = VVarEnvironment()
oenv = OVarEnvironment()
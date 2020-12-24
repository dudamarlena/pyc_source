# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: puke/Require.py
# Compiled at: 2012-10-18 11:09:43
__doc__ = 'REquire parser\n\nThis class simply provide an accessor on a dict\n'
import os, re, yaml, json
from puke.Env import *
from puke.Console import *
from puke.Yak import *
from puke.Utils import *

def custom_str_constructor(loader, node):
    return loader.construct_scalar(node).encode('utf-8')


yaml.add_constructor('tag:yaml.org,2002:str', custom_str_constructor)

class Load(object):

    def __init__(self, filename):
        self.content = None
        try:
            stream = None
            stream = file(filename, 'r')
            payload = stream.read()
            stream.close()
            size = payload.strip()
            ext = os.path.splitext(stream.name)[1]
            if size == 0:
                self.content = {}
                return
            if ext in ('.json', '.js'):
                self.content = json.loads(payload)
            elif ext in ('.yaml', '.yml'):
                self.content = yaml.load(payload)
        except Exception as error:
            raise RequireError('Require load error : %s' % error)
            self.content = None

        return

    def __str__(self):
        return '%s' % self.content

    def __repr__(self):
        return '%s' % self.content


class Require(object):
    __sharedState = {}
    __globalPattern = re.compile('\\$\\{([^}]+)\\}([|])?(.*)')

    def __init__(self, filename):
        self.__dict__ = self.__sharedState
        if not self.__sharedState:
            self.__files = [
             filename]
            self.__cfg = Load(filename).content
            self.__makeenvs(self.__cfg)

    def merge(self, filename):
        self.__files.append(filename)
        self.__cfg = deepmerge(self.__cfg, Load(filename).content)
        self.__makeenvs(self.__cfg)

    def yak(self, selector):
        if not self.get(selector):
            return False
        else:
            for node, value in self.get(selector).items():
                existing = Yak.get(node)
                if existing != None and not isinstance(existing, str):
                    value = deepmerge(Yak.get(node), value)
                Yak.set(node, value)

            return

    def get(self, key):
        if self.__cfg.has_key(key):
            return self.__cfg[key]

    def set(self, key, value):
        self.__cfg[key] = value

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.__cfg

    def __repr__(self):
        return 'Config: %s' % self.__cfg

    def __makeenvs(self, data):
        if data == None:
            return False
        else:
            if isinstance(data, list):
                dataIter = enumerate(data)
            else:
                if isinstance(data, dict):
                    dataIter = data.items()
                else:
                    return
                for node, value in dataIter:
                    if not isinstance(value, (str, int)):
                        self.__makeenvs(value)
                    elif value.startswith('${'):
                        m = self.__globalPattern.match(value)
                        if not m:
                            continue
                        name, isDefault, extValue = m.groups()
                        if isDefault:
                            default = extValue
                        else:
                            default = ''
                        value = Env.get(name, default)
                        if not isDefault:
                            value += extValue
                        data[node] = value

            return

    def reload(self):
        files = self.__files
        self.__files = []
        self.__cfg = {}
        for filename in files:
            self.include(filename)


class RequireError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/submodfix/submodfix.py
# Compiled at: 2013-10-24 11:30:07
from re import match, search
from os import system

class Submodule:
    name = None
    path = None
    url = None

    def is_valid(self):
        if self.name and self.path and self.url:
            return True
        return False

    def add(self):
        system('git submodule add --name %s %s %s' % (self.name, self.url, self.path))

    def __init__(self, name, path=None, url=None):
        self.name = name
        self.path = path
        self.url = url

    def __unicode__(self):
        return self.name


def main():
    with open('.gitmodules', 'r') as (f):
        submodule = None
        submodules = []
        for line in f.readlines():
            m = match('^\\[submodule \\"(?P<name>[^\\0^\\"]+)\\"\\]$', line)
            if m:
                if submodule and submodule.is_valid():
                    submodules.append(submodule)
                submodule = Submodule(m.group('name'))
            else:
                m = match('^\\s*(?P<key>\\w+)\\s*=\\s(?P<value>[^\\0^\\"]+)$', line)
                if m and submodule:
                    key = m.group('key')
                    value = m.group('value')
                    if key == 'path':
                        submodule.path = value.strip()
                    elif key == 'url':
                        submodule.url = value.strip()

        if submodule.is_valid():
            submodules.append(submodule)
    for submodule in submodules:
        submodule.add()

    return


if __name__ == '__main__':
    main()
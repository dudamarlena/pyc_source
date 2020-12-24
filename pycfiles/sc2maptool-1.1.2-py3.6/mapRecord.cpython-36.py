# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2maptool\mapRecord.py
# Compiled at: 2018-08-13 20:50:48
# Size of source mod 2**32: 2597 bytes
import os, re
from sc2maptool import constants as c

def standardizeMapName(mapName):
    """pretty-fy the name for pysc2 map lookup"""
    newName = os.path.basename(mapName)
    newName = newName.split('.')[0]
    newName = newName.split('(')[0]
    newName = re.sub('[LT]E+$', '', newName)
    newName = re.sub('-', '', newName)
    newName = re.sub(' ', '', newName, flags=(re.UNICODE))
    foreignName = newName
    if foreignName in c.mapNameTranslations:
        return c.mapNameTranslations[foreignName]
    else:
        return newName


class MapRecord(object):
    EXCLUDED_ATTRS = [
     'name']

    def __init__(self, name, path, attrs):
        self.name = standardizeMapName(name)
        self.path = path
        for a in attrs:
            a = a.lower()
            val = re.search('^([a-z]+)([\\d_]\\w*)$', a)
            if val:
                a, val = val.groups()
                try:
                    val = int(val)
                except:
                    val = val.lstrip('_')

            else:
                val = True
            setattr(self, a, val)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.name)

    @property
    def attrs(self):
        try:
            return self._attrs
        except AttributeError:
            pass

        self._attrs = [a for a in self.__dict__ if a not in MapRecord.EXCLUDED_ATTRS]
        return self._attrs

    @property
    def rawData(self):
        """the raw, binary contents of the Starcraft2 map file"""
        with open(self.path, 'rb') as (f):
            return f.read()

    def display(self):
        print(self)
        for a in self.attrs:
            print('    %8s : %s' % (a, self.__dict__[a]))
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/findtable.py
# Compiled at: 2006-06-01 13:56:34
"""Class to provide "findTable" convenience callable"""
from basicproperty import common, propertied, basic

class FindTable(propertied.Propertied):
    """Provides callable object that retrieves a given table schema table by name"""
    nameCache = common.DictionaryProperty('nameCache', 'Cache of the names retrieved')
    schema = basic.BasicProperty('schema', 'Table schema in which we look up names')

    def __call__(self, name):
        current = self.nameCache.get(name)
        if current is not None:
            return current
        current = self.schema.lookupName(name)
        if current is None:
            raise NameError('Unrecognised table name: %r' % (name,))
        self.nameCache[name] = current
        return current
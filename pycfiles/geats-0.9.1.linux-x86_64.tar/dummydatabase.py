# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/databases/dummydatabase.py
# Compiled at: 2013-12-22 08:50:56


class DummyDatabase:

    def __init__(self, config):
        self.datastore = {}

    def create(self, name, definition, **extras):
        self.datastore[name] = extras
        extras['definition'] = definition

    def update(self, name, definition=None, **extras):
        d = self.datastore[name]
        if definition:
            d['definition'] = d
        d.update(extras)

    def delete(self, name):
        if name in self.datastore:
            del self.datastore[name]

    def list(self):
        return self.datastore.keys()

    def get_definition(self, name):
        d = self.datastore.get(name, None)
        if d:
            return d['definition']
        else:
            return
            return

    def get(self, name, key=None):
        if name not in self.datastore:
            return
        else:
            if key is None:
                return self.datastore[name]
            else:
                return self.datastore[name].get(key, {})

            return
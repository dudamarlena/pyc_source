# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/ycollections/tagmaps.py
# Compiled at: 2016-03-30 08:43:32


class TagMaps(dict):
    DefaultKey = ''

    def __missing__(self, key):
        if isinstance(key, int):
            return self.keys()[key]
        if self.DefaultKey in self:
            return self.get(self.DefaultKey)
        raise KeyError(key)

    def register(self, key, force=False):
        """
        Register obj as a decorator

        :param key: obj key
        :param force: force update
        """
        key = str(key)
        if not force and key in self:
            raise KeyError('%s was existed' % key)

        def update(obj):
            self.update(key, obj)
            return obj

        return update

    def update(self, key_or_dict, obj=NotImplemented):
        if obj is not NotImplemented:
            key_or_dict = {str(key_or_dict): obj}
        return super(TagMaps, self).update(key_or_dict)
# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sdb/db/key.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2036 bytes


class Key(object):

    @classmethod
    def from_path(cls, *args, **kwds):
        raise NotImplementedError('Paths are not currently supported')

    def __init__(self, encoded=None, obj=None):
        self.name = None
        if obj:
            self.id = obj.id
            self.kind = obj.kind()
        else:
            self.id = None
            self.kind = None

    def app(self):
        raise NotImplementedError('Applications are not currently supported')

    def kind(self):
        return self.kind

    def id(self):
        return self.id

    def name(self):
        raise NotImplementedError('Key Names are not currently supported')

    def id_or_name(self):
        return self.id

    def has_id_or_name(self):
        return self.id is not None

    def parent(self):
        raise NotImplementedError('Key parents are not currently supported')

    def __str__(self):
        return self.id_or_name()
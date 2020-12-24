# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/borg.py
# Compiled at: 2017-04-23 10:30:41


def borg(cls):
    cls._state = {}
    orig_init = cls.__init__

    def new_init(self, *args, **kwargs):
        self.__dict__ = cls._state
        orig_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls
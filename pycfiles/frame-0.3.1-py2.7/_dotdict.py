# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/_dotdict.py
# Compiled at: 2013-02-02 17:31:38


class DotDict(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            self[key] = DotDict(value)
        else:
            self[key] = value
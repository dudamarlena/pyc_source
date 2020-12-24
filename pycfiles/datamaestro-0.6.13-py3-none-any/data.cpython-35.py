# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bpiwowar/development/datasets/datasets/data.py
# Compiled at: 2016-11-18 05:09:13
# Size of source mod 2**32: 467 bytes


class Context(object):
    __doc__ = 'Context of a configuration file'

    def __init__(self, prefix):
        self.prefix = prefix

    def id(self, _id):
        return '%s.%s' % (self.prefix, _id)


class Data:

    def __init__(self, context, config):
        self.id = config.id
        if type(config.id) == list:
            self.aliases = self.id
            self.id = self.id[0]


class Documents:

    def __init__(self, context, config):
        pass
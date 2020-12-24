# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/mongua/errors.py
# Compiled at: 2017-06-19 05:49:36
# Size of source mod 2**32: 894 bytes


class MonguaLocked(Exception):

    def __init__(self, obj):
        self.data = obj
        self.msg = '[MongoMixin]: locked instance is not savable.'


class MonguaNotFound(Exception):

    def __init__(self, collection):
        self.msg = '[MongoMixin]: not found collection({})'.format(collection)


class MonguaKeyFrozen(Exception):

    def __init__(self, collection, field_key):
        self.msg = '[MongoMixin]: {}._frozen_key({}) is immutable.'.format(collection, field_key)


class MonguaKeyUndefined(Exception):

    def __init__(self, collection, field_key):
        self.msg = '[MongoMixin]: The Key({}) is undefined in {}.__fields__'.format(field_key, collection)


class MonguaFieldUnmovable(Exception):

    def __init__(self, collection, field_key):
        self.msg = '[MongoMixin]: The Field({}) is still in {}.__fields__ '.format(field_key, collection)
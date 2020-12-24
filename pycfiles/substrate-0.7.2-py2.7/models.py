# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/lib/substrate/restler/models.py
# Compiled at: 2012-09-08 20:09:57


class TransientModel(object):

    @classmethod
    def kind(cls):
        return cls.__name__

    @classmethod
    def required_fields(cls):
        return tuple()

    @classmethod
    def optional_fields(cls):
        return tuple()

    @classmethod
    def fields(cls):
        return cls.required_fields() + cls.optional_fields()

    def __init__(self, **kwargs):
        for prop in self.fields():
            setattr(self, prop, kwargs.get(prop))
            if prop in self.required_fields() and getattr(self, prop) is None:
                raise AttributeError('The property: %s is required.' % prop)

        return

    def properties(self):
        return dict([ (prop, getattr(self, prop)) for prop in self.fields() ])
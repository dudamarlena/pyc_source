# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: distributions/mixins.py
# Compiled at: 2017-10-28 18:53:45
import warnings, functools

def deprecated(message='function will be removed in the future'):

    def decorator(fun):

        @functools.wraps(fun)
        def deprecated_fun(*args, **kwargs):
            warnings.warn(('DEPRECATED {}: {}').format(fun.__name__, message))
            return fun(*args, **kwargs)

        return deprecated_fun

    return decorator


class ComponentModel(object):
    pass


class SharedMixin(object):

    def add_value(self, value):
        pass

    def remove_value(self, value):
        pass

    def realize(self):
        pass


class ProtobufSerializable(object):

    @classmethod
    def to_protobuf(cls, raw, message):
        model = cls()
        model.load(raw)
        model.protobuf_dump(message)

    @classmethod
    def from_protobuf(cls, message):
        model = cls()
        model.protobuf_load(message)
        return model.dump()

    @deprecated('use protobuf_dump(message) instead')
    def dump_protobuf(self, message):
        self.protobuf_dump(message)

    @deprecated('use protobuf_load(message) instead')
    def load_protobuf(self, message):
        self.protobuf_load(message)


class GroupIoMixin(ProtobufSerializable):

    @classmethod
    def from_values(cls, model, values=[]):
        group = cls()
        group.init(model)
        for value in values:
            group.add_value(model, value)

        return group

    @classmethod
    def from_dict(cls, raw):
        group = cls()
        group.load(raw)
        return group


class SharedIoMixin(ProtobufSerializable):

    @classmethod
    def from_dict(cls, raw):
        model = cls()
        model.load(raw)
        return model
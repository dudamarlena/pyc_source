# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/base.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 8763 bytes
from __future__ import unicode_literals
from inspect import isclass
from weakref import proxy
from ....package.loader import traverse, load
from ....schema import Attribute
from ....schema.transform import BaseTransform
from ....schema.validate import Validator
from ....schema.compat import str, unicode, py3
from ...query import Q
from ...util import adjust_attribute_sequence, SENTINEL

class FieldTransform(BaseTransform):

    def foreign(self, value, context):
        field, document = context
        if hasattr(field, 'to_foreign'):
            return field.to_foreign(document, field.__name__, value)
        else:
            return value

    def native(self, value, context):
        field, document = context
        if hasattr(field, 'to_native'):
            return field.to_native(document, field.__name__, value)
        else:
            return value


@adjust_attribute_sequence(1000, 'transformer', 'validator', 'positional', 'assign', 'repr', 'project', 'read', 'write', 'sort')
class Field(Attribute):
    __allowed_operators__ = set()
    __disallowed_operators__ = set()
    __document__ = None
    __foreign__ = {}
    __acl__ = []
    choices = Attribute(default=None)
    required = Attribute(default=False)
    nullable = Attribute(default=False)
    exclusive = Attribute(default=None)
    transformer = Attribute(default=(FieldTransform()))
    validator = Attribute(default=(Validator()))
    positional = Attribute(default=True)
    assign = Attribute(default=False)
    repr = Attribute(default=True)
    project = Attribute(default=None)
    read = Attribute(default=True)
    write = Attribute(default=True)
    sort = Attribute(default=True)

    def adapt(self, **kw):
        instance = self.__class__()
        instance.__data__ = self.__data__.copy()
        for k, v in kw.items():
            setattr(instance, k, v)

        return instance

    def __repr__(self):
        fields = []
        for field in self.__attributes__.values():
            name = field.__name__
            if name in ('__name__', ):
                pass
            elif name not in self.__data__:
                continue
            default = getattr(field, 'default', SENTINEL)
            value = self.__data__[name]
            if value != default:
                fields.append((field.__name__, value))

        if fields:
            fields = ', '.join('{}={!r}'.format(field, value) for field, value in fields)
            fields = ', ' + fields
        else:
            fields = ''
        name = getattr(self, '__name__', '<anonymous>')
        return "{self.__class__.__name__}('{name}'{fields})".format(self=self,
          name=name,
          fields=fields)

    def is_readable(self, context=None):
        if callable(self.read):
            if context:
                return self.read(context, self)
            return self.read(self)
        else:
            return bool(self.read)

    def is_writeable(self, context=None):
        if callable(self.write):
            if context:
                return self.write(context, self)
            return self.write(self)
        else:
            return bool(self.write)

    def __init__(self, *args, **kw):
        (super(Field, self).__init__)(*args, **kw)
        if self.nullable:
            try:
                self.default
            except AttributeError:
                self.default = None

    def __fixup__(self, document):
        """Called after an instance of our Field class is assigned to a Document."""
        self.__document__ = proxy(document)

    def __get__(self, obj, cls=None):
        """Executed when retrieving a Field instance attribute."""
        if obj is None:
            return Q(cls, self)
        else:
            result = super(Field, self).__get__(obj, cls)
            if result is None:
                return
            return self.transformer.native(result, (self, obj))

    def __set__(self, obj, value):
        if self.exclusive:
            for other in self.exclusive:
                try:
                    ovalue = traverse(obj, other, None)
                except LookupError:
                    pass

                if ovalue is not None:
                    raise AttributeError('Can not assign to ' + self.__name__ + ' if ' + other + ' has a value.')

        if value is not None:
            value = self.transformer.foreign(value, (self, obj))
        super(Field, self).__set__(obj, value)

    def __delete__(self, obj):
        """Executed via the `del` statement with a DataAttribute instance attribute as the argument."""
        del obj.__data__[self.__name__]

    def __unicode__(self):
        return self.__name__

    if py3:
        __str__ = __unicode__
        del __unicode__


class _HasKind(Field):
    __doc__ = 'A mix-in to provide an easily definable singular or plural set of document types.'
    kind = Attribute(default=None)

    def __init__(self, *args, **kw):
        if args:
            kw['kind'], args = args[0], args[1:]
        (super(_HasKind, self).__init__)(*args, **kw)

    def __fixup__(self, document):
        super(_HasKind, self).__fixup__(document)
        kind = self.kind
        if not kind:
            return
        if isinstance(kind, Field):
            kind.__name__ = self.__name__
            kind.__document__ = proxy(document)
            kind.__fixup__(document)

    def _kind(self, document=None):
        kind = self.kind
        if isinstance(kind, (str, unicode)):
            if kind.startswith('.'):
                kind = traverse(document or self.__document__, kind[1:])
                if not isinstance(kind, (str, unicode)):
                    return kind
            else:
                kind = load(kind, 'marrow.mongo.document')
        return kind


class _CastingKind(Field):

    def to_native(self, obj, name, value):
        """Transform the MongoDB value into a Marrow Mongo value."""
        from marrow.mongo import Document
        from marrow.mongo.trait import Derived
        kind = self._kind(obj.__class__)
        if isinstance(value, Document):
            if __debug__:
                if kind:
                    if issubclass(kind, Document):
                        if not isinstance(value, kind):
                            raise ValueError('Not an instance of ' + kind.__name__ + ' or a sub-class: ' + repr(value))
            return value
        else:
            if isinstance(kind, Field):
                return kind.transformer.native(value, (kind, obj))
            return (kind or Derived).from_mongo(value)

    def to_foreign(self, obj, name, value):
        """Transform to a MongoDB-safe value."""
        from marrow.mongo import Document
        kind = self._kind(obj if isclass(obj) else obj.__class__)
        if isinstance(value, Document):
            if __debug__:
                if kind:
                    if issubclass(kind, Document):
                        if not isinstance(value, kind):
                            raise ValueError('Not an instance of ' + kind.__name__ + ' or a sub-class: ' + repr(value))
            return value
        if isinstance(kind, Field):
            return kind.transformer.foreign(value, (kind, obj))
        else:
            if kind:
                value = kind(**value)
            return value
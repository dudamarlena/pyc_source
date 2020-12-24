# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/fieldspec.py
# Compiled at: 2007-03-21 14:34:41
"""Fieldspec-related code.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevo.constant import UNASSIGNED
from schevo.label import label_from_name
from schevo.lib.odict import odict

class FieldMap(odict):
    """Field Mapping based on Ordered Dictionary."""
    __module__ = __name__
    __slots__ = [
     '_keys']

    def update_values(self, other):
        """Update field values based on field values in other FieldMap."""
        for (name, field) in other.iteritems():
            if name in self:
                f = self[name]
                if f.fget is None and not f.readonly:
                    f.set(field.get())

        return

    def value_map(self):
        d = odict()
        for (name, field) in self.items():
            value = field._value
            d[name] = value

        return d


class FieldSpecMap(odict):
    """Field spec mapping based on Ordered Dictionary."""
    __module__ = __name__
    __slots__ = [
     '_keys']

    def __call__(self, *filters):
        """Return FieldSpecMap instance based on self, filtered by optional
        callable objects specified in `filters`."""
        new_fields = self.iteritems()
        for filt in filters:
            new_fields = [ (key, field) for (key, field) in new_fields if filt(field) ]

        return FieldSpecMap(new_fields)

    def field_map(self, instance=None, values={}):
        """Return a FieldMap based on field specifications."""
        pairs = [ (name, FieldClass(instance=instance, value=values.get(name, UNASSIGNED))) for (name, FieldClass) in self.iteritems() ]
        return FieldMap(pairs)


def field_spec_from_class(cls, class_dict, slots=False):
    field_spec = FieldSpecMap()
    if cls._field_spec:
        for (name, BaseFieldClass) in cls._field_spec.iteritems():
            field_spec[name] = new_field_class(BaseFieldClass, slots)

    specs = []
    for (name, field_def) in class_dict.items():
        if isinstance(field_def, FieldDefinition):
            field_def.name = name
            BaseFieldClass = field_def.FieldClass
            NewClass = new_field_class(BaseFieldClass, slots)
            NewClass._name = name
            if not NewClass.label:
                NewClass.label = label_from_name(name)
            specs.append((field_def.counter, name, NewClass))
            if isinstance(getattr(cls, name, None), FieldDefinition):
                delattr(cls, name)

    specs.sort()
    specs = [ s[1:] for s in specs ]
    field_spec.update(FieldSpecMap(specs))
    return field_spec


def new_field_class(BaseFieldClass, slots):
    """Return a new field class subclassed from BaseFieldClass."""
    if slots:

        class NewClass(BaseFieldClass):
            __module__ = __name__

    else:

        class NoSlotsField(BaseFieldClass):
            __module__ = __name__

        NewClass = NoSlotsField
    NewClass.readonly = BaseFieldClass.readonly
    NewClass.__name__ = BaseFieldClass.__name__
    return NewClass


class FieldDefinition(object):
    """A definition of a field attached to something.

    The order of FieldDefinition instance creation is kept for the
    purposes of creating ordered dictionaries of fields, etc.
    """
    __module__ = __name__
    __do_not_optimize__ = True
    BaseFieldClass = None
    _counter = 0

    def __init__(self, *args, **kw):
        self.name = None
        BaseFieldClass = self.BaseFieldClass

        class _Field(BaseFieldClass):
            __module__ = __name__

        _Field.BaseFieldClass = BaseFieldClass
        _Field._init_kw(kw)
        _Field._init_args(args)
        _Field._init_final()
        _Field.__name__ = BaseFieldClass.__name__
        self.FieldClass = _Field
        self.counter = FieldDefinition._counter
        FieldDefinition._counter += 1
        return

    def __call__(self, fn):
        """For use as a decorator."""
        self.FieldClass.fget = (
         fn,)
        return self

    def field(self, name, instance=None, value=None):

        class NoSlotsField(self.FieldClass):
            __module__ = __name__

        NoSlotsField.__name__ = self.FieldClass.__name__
        NewClass = NoSlotsField
        NewClass._name = name
        if not NewClass.label:
            NewClass.label = label_from_name(name)
        f = NewClass(instance, value)
        return f


optimize.bind_all(sys.modules[__name__])
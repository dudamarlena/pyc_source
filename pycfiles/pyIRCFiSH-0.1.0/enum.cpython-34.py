# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/util/enum.py
# Compiled at: 2015-10-08 05:15:50
# Size of source mod 2**32: 22931 bytes
import sys
from collections import OrderedDict
from types import MappingProxyType

class DynamicClassAttribute:
    """DynamicClassAttribute"""

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or fget.__doc__
        self.overwrite_doc = doc is None
        self.__isabstractmethod__ = bool(getattr(fget, '__isabstractmethod__', False))

    def __get__(self, instance, ownerclass=None):
        if instance is None:
            if self.__isabstractmethod__:
                return self
            raise AttributeError()
        elif self.fget is None:
            raise AttributeError('unreadable attribute')
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def getter(self, fget):
        fdoc = fget.__doc__ if self.overwrite_doc else None
        result = type(self)(fget, self.fset, self.fdel, fdoc or self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result

    def setter(self, fset):
        result = type(self)(self.fget, fset, self.fdel, self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result

    def deleter(self, fdel):
        result = type(self)(self.fget, self.fset, fdel, self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result


__all__ = [
 'Enum', 'IntEnum', 'unique']

def _is_descriptor(obj):
    """Returns True if obj is a descriptor, False otherwise."""
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')


def _is_dunder(name):
    """Returns True if a __dunder__ name, False otherwise."""
    return name[:2] == name[-2:] == '__' and name[2:3] != '_' and name[-3:-2] != '_' and len(name) > 4


def _is_sunder(name):
    """Returns True if a _sunder_ name, False otherwise."""
    return name[0] == name[(-1)] == '_' and name[1:2] != '_' and name[-2:-1] != '_' and len(name) > 2


def _make_class_unpicklable(cls):
    """Make the given class un-picklable."""

    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)

    cls.__reduce_ex__ = _break_on_call_reduce
    cls.__module__ = '<unknown>'


class _EnumDict(dict):
    """_EnumDict"""

    def __init__(self):
        super().__init__()
        self._member_names = []

    def __setitem__(self, key, value):
        """Changes anything not dundered or not a descriptor.

        If an enum member name is used twice, an error is raised; duplicate
        values are not checked for.

        Single underscore (sunder) names are reserved.

        """
        if _is_sunder(key):
            raise ValueError('_names_ are reserved for future Enum use')
        else:
            if _is_dunder(key):
                pass
            else:
                if key in self._member_names:
                    raise TypeError('Attempted to reuse key: %r' % key)
                elif not _is_descriptor(value):
                    if key in self:
                        raise TypeError('Key already defined as: %r' % self[key])
                    self._member_names.append(key)
        super().__setitem__(key, value)


Enum = None

class EnumMeta(type):
    """EnumMeta"""

    @classmethod
    def __prepare__(metacls, cls, bases):
        return _EnumDict()

    def __new__(metacls, cls, bases, classdict):
        member_type, first_enum = metacls._get_mixins_(bases)
        __new__, save_new, use_args = metacls._find_new_(classdict, member_type, first_enum)
        members = {k:classdict[k] for k in classdict._member_names}
        for name in classdict._member_names:
            del classdict[name]

        invalid_names = set(members) & {'mro'}
        if invalid_names:
            raise ValueError('Invalid enum member name: {0}'.format(','.join(invalid_names)))
        enum_class = super().__new__(metacls, cls, bases, classdict)
        enum_class._member_names_ = []
        enum_class._member_map_ = OrderedDict()
        enum_class._member_type_ = member_type
        enum_class._value2member_map_ = {}
        if '__reduce_ex__' not in classdict:
            if member_type is not object:
                methods = ('__getnewargs_ex__', '__getnewargs__', '__reduce_ex__',
                           '__reduce__')
                if not any(m in member_type.__dict__ for m in methods):
                    _make_class_unpicklable(enum_class)
        for member_name in classdict._member_names:
            value = members[member_name]
            if not isinstance(value, tuple):
                args = (
                 value,)
            else:
                args = value
            if member_type is tuple:
                args = (
                 args,)
            if not use_args:
                enum_member = __new__(enum_class)
                if not hasattr(enum_member, '_value_'):
                    enum_member._value_ = value
            else:
                enum_member = __new__(enum_class, *args)
                if not hasattr(enum_member, '_value_'):
                    enum_member._value_ = member_type(*args)
            value = enum_member._value_
            enum_member._name_ = member_name
            enum_member.__objclass__ = enum_class
            enum_member.__init__(*args)
            for name, canonical_member in enum_class._member_map_.items():
                if canonical_member._value_ == enum_member._value_:
                    enum_member = canonical_member
                    break
            else:
                enum_class._member_names_.append(member_name)

            enum_class._member_map_[member_name] = enum_member
            try:
                enum_class._value2member_map_[value] = enum_member
            except TypeError:
                pass

        for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            class_method = getattr(enum_class, name)
            obj_method = getattr(member_type, name, None)
            enum_method = getattr(first_enum, name, None)
            if obj_method is not None and obj_method is class_method:
                setattr(enum_class, name, enum_method)
                continue

        if Enum is not None:
            if save_new:
                enum_class.__new_member__ = __new__
            enum_class.__new__ = Enum.__new__
        return enum_class

    def __call__(cls, value, names=None, *, module=None, qualname=None, type=None):
        """Either returns an existing member, or creates a new enum class.

        This method is used both when an enum class is given a value to match
        to an enumeration member (i.e. Color(3)) and for the functional API
        (i.e. Color = Enum('Color', names='red green blue')).

        When used for the functional API:

        `value` will be the name of the new class.

        `names` should be either a string of white-space/comma delimited names
        (values will start at 1), or an iterator/mapping of name, value pairs.

        `module` should be set to the module this class is being created in;
        if it is not set, an attempt to find that module will be made, but if
        it fails the class will not be picklable.

        `qualname` should be set to the actual location this class can be found
        at in its module; by default it is set to the global scope.  If this is
        not correct, unpickling will fail in some circumstances.

        `type`, if set, will be mixed in as the first base class.

        """
        if names is None:
            return cls.__new__(cls, value)
        return cls._create_(value, names, module=module, qualname=qualname, type=type)

    def __contains__(cls, member):
        return isinstance(member, cls) and member._name_ in cls._member_map_

    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError('%s: cannot delete Enum member.' % cls.__name__)
        super().__delattr__(attr)

    def __dir__(self):
        return [
         '__class__', '__doc__', '__members__', '__module__'] + self._member_names_

    def __getattr__(cls, name):
        """Return the enum member matching `name`

        We use __getattr__ instead of descriptors or inserting into the
        enum class' __dict__ in order to support `name` and `value`
        being both properties for enum members (which live in the class'
        __dict__) and enum members themselves.

        """
        if _is_dunder(name):
            raise AttributeError(name)
        try:
            return cls._member_map_[name]
        except KeyError:
            raise AttributeError(name) from None

    def __getitem__(cls, name):
        return cls._member_map_[name]

    def __iter__(cls):
        return (cls._member_map_[name] for name in cls._member_names_)

    def __len__(cls):
        return len(cls._member_names_)

    @property
    def __members__(cls):
        """Returns a mapping of member name->value.

        This mapping lists all enum members, including aliases. Note that this
        is a read-only view of the internal mapping.

        """
        return MappingProxyType(cls._member_map_)

    def __repr__(cls):
        return '<enum %r>' % cls.__name__

    def __reversed__(cls):
        return (cls._member_map_[name] for name in reversed(cls._member_names_))

    def __setattr__(cls, name, value):
        """Block attempts to reassign Enum members.

        A simple assignment to the class namespace only changes one of
        the several possible ways to get an Enum member from the Enum
        class, resulting in an inconsistent Enumeration.

        """
        member_map = cls.__dict__.get('_member_map_', {})
        if name in member_map:
            raise AttributeError('Cannot reassign members.')
        super().__setattr__(name, value)

    def _create_(cls, class_name, names=None, *, module=None, qualname=None, type=None):
        """Convenience method to create a new Enum class.

        `names` can be:

        * A string containing member names, separated either with spaces or
          commas.  Values are auto-numbered from 1.
        * An iterable of member names.  Values are auto-numbered from 1.
        * An iterable of (member name, value) pairs.
        * A mapping of member name -> value.

        """
        metacls = cls.__class__
        bases = (cls,) if type is None else (type, cls)
        classdict = metacls.__prepare__(class_name, bases)
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
        if isinstance(names, (tuple, list)) and isinstance(names[0], str):
            names = [(e, i) for i, e in enumerate(names, 1)]
        for item in names:
            if isinstance(item, str):
                member_name, member_value = item, names[item]
            else:
                member_name, member_value = item
            classdict[member_name] = member_value

        enum_class = metacls.__new__(metacls, class_name, bases, classdict)
        if module is None:
            try:
                module = sys._getframe(2).f_globals['__name__']
            except (AttributeError, ValueError):
                pass

        if module is None:
            _make_class_unpicklable(enum_class)
        else:
            enum_class.__module__ = module
        if qualname is not None:
            enum_class.__qualname__ = qualname
        return enum_class

    @staticmethod
    def _get_mixins_(bases):
        """Returns the type for creating enum members, and the first inherited
        enum class.

        bases: the tuple of bases that was given to __new__

        """
        if not bases:
            return (object, Enum)
        member_type = first_enum = None
        for base in bases:
            if base is not Enum and issubclass(base, Enum) and base._member_names_:
                raise TypeError('Cannot extend enumerations')
                continue

        if not issubclass(base, Enum):
            raise TypeError('new enumerations must be created as `ClassName([mixin_type,] enum_type)`')
        if not issubclass(bases[0], Enum):
            member_type = bases[0]
            first_enum = bases[(-1)]
        else:
            for base in bases[0].__mro__:
                if issubclass(base, Enum):
                    if first_enum is None:
                        first_enum = base
                elif member_type is None:
                    member_type = base
                    continue

        return (
         member_type, first_enum)

    @staticmethod
    def _find_new_(classdict, member_type, first_enum):
        """Returns the __new__ to be used for creating the enum members.

        classdict: the class dictionary given to __new__
        member_type: the data type whose __new__ will be used by default
        first_enum: enumeration to check for an overriding __new__

        """
        __new__ = classdict.get('__new__', None)
        save_new = __new__ is not None
        if __new__ is None:
            for method in ('__new_member__', '__new__'):
                for possible in (member_type, first_enum):
                    target = getattr(possible, method, None)
                    if target not in {
                     None,
                     (None).__new__,
                     object.__new__,
                     Enum.__new__}:
                        __new__ = target
                        break

                if __new__ is not None:
                    break
            else:
                __new__ = object.__new__

        if __new__ is object.__new__:
            use_args = False
        else:
            use_args = True
        return (
         __new__, save_new, use_args)


class Enum(metaclass=EnumMeta):
    """Enum"""

    def __new__(cls, value):
        if isinstance(value, cls):
            return value
        try:
            if value in cls._value2member_map_:
                return cls._value2member_map_[value]
        except TypeError:
            for member in cls._member_map_.values():
                if member._value_ == value:
                    return member

        raise ValueError('%r is not a valid %s' % (value, cls.__name__))

    def __repr__(self):
        return '<%s.%s: %r>' % (
         self.__class__.__name__, self._name_, self._value_)

    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)

    def __dir__(self):
        added_behavior = [m for cls in self.__class__.mro() for m in cls.__dict__ if m[0] != '_']
        return [
         '__class__', '__doc__', '__module__', 'name', 'value'] + added_behavior

    def __format__(self, format_spec):
        if self._member_type_ is object:
            cls = str
            val = str(self)
        else:
            cls = self._member_type_
            val = self._value_
        return cls.__format__(val, format_spec)

    def __hash__(self):
        return hash(self._name_)

    def __reduce_ex__(self, proto):
        return (
         self.__class__, (self._value_,))

    @DynamicClassAttribute
    def name(self):
        """The name of the Enum member."""
        return self._name_

    @DynamicClassAttribute
    def value(self):
        """The value of the Enum member."""
        return self._value_


class IntEnum(int, Enum):
    """IntEnum"""
    pass


def unique(enumeration):
    """Class decorator for enumerations ensuring unique member values."""
    duplicates = []
    for name, member in enumeration.__members__.items():
        if name != member.name:
            duplicates.append((name, member.name))
            continue

    if duplicates:
        alias_details = ', '.join(['%s -> %s' % (alias, name) for alias, name in duplicates])
        raise ValueError('duplicate values found in %r: %s' % (
         enumeration, alias_details))
    return enumeration
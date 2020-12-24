# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/smriprep/wrapper/build/lib/python3.7/enum.py
# Compiled at: 2019-09-12 11:41:56
# Size of source mod 2**32: 34778 bytes
import sys
from types import MappingProxyType, DynamicClassAttribute
try:
    from _collections import OrderedDict
except ImportError:
    from collections import OrderedDict

__all__ = ['EnumMeta',
 'Enum', 'IntEnum', 'Flag', 'IntFlag',
 'auto', 'unique']

def _is_descriptor(obj):
    """Returns True if obj is a descriptor, False otherwise."""
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')


def _is_dunder(name):
    """Returns True if a __dunder__ name, False otherwise."""
    return len(name) > 4 and name[:2] == name[-2:] == '__' and name[2] != '_' and name[(-3)] != '_'


def _is_sunder(name):
    """Returns True if a _sunder_ name, False otherwise."""
    return len(name) > 2 and name[0] == name[(-1)] == '_' and name[1:2] != '_' and name[-2:-1] != '_'


def _make_class_unpicklable(cls):
    """Make the given class un-picklable."""

    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)

    cls.__reduce_ex__ = _break_on_call_reduce
    cls.__module__ = '<unknown>'


_auto_null = object()

class auto:
    __doc__ = '\n    Instances are replaced with an appropriate value in Enum class suites.\n    '
    value = _auto_null


class _EnumDict(dict):
    __doc__ = 'Track enum member order and ensure member names are not reused.\n\n    EnumMeta will use the names found in self._member_names as the\n    enumeration member names.\n\n    '

    def __init__(self):
        super().__init__()
        self._member_names = []
        self._last_values = []
        self._ignore = []

    def __setitem__(self, key, value):
        if _is_sunder(key):
            if key not in ('_order_', '_create_pseudo_member_', '_generate_next_value_',
                           '_missing_', '_ignore_'):
                raise ValueError('_names_ are reserved for future Enum use')
            if key == '_generate_next_value_':
                setattr(self, '_generate_next_value', value)
            else:
                if key == '_ignore_':
                    if isinstance(value, str):
                        value = value.replace(',', ' ').split()
                    else:
                        value = list(value)
                    self._ignore = value
                    already = set(value) & set(self._member_names)
                    if already:
                        raise ValueError('_ignore_ cannot specify already set names: %r' % (already,))
        else:
            if _is_dunder(key):
                if key == '__order__':
                    key = '_order_'
            else:
                if key in self._member_names:
                    raise TypeError('Attempted to reuse key: %r' % key)
                else:
                    if key in self._ignore:
                        pass
                    else:
                        if not _is_descriptor(value):
                            if key in self:
                                raise TypeError('%r already defined as: %r' % (key, self[key]))
                            if isinstance(value, auto):
                                if value.value == _auto_null:
                                    value.value = self._generate_next_value(key, 1, len(self._member_names), self._last_values[:])
                                value = value.value
                            self._member_names.append(key)
                            self._last_values.append(value)
                        super().__setitem__(key, value)


Enum = None

class EnumMeta(type):
    __doc__ = 'Metaclass for Enum'

    @classmethod
    def __prepare__(metacls, cls, bases):
        enum_dict = _EnumDict()
        member_type, first_enum = metacls._get_mixins_(bases)
        if first_enum is not None:
            enum_dict['_generate_next_value_'] = getattr(first_enum, '_generate_next_value_', None)
        return enum_dict

    def __new__(metacls, cls, bases, classdict):
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        for key in ignore:
            classdict.pop(key, None)

        member_type, first_enum = metacls._get_mixins_(bases)
        __new__, save_new, use_args = metacls._find_new_(classdict, member_type, first_enum)
        enum_members = {k:classdict[k] for k in classdict._member_names}
        for name in classdict._member_names:
            del classdict[name]

        _order_ = classdict.pop('_order_', None)
        invalid_names = set(enum_members) & {'mro', ''}
        if invalid_names:
            raise ValueError('Invalid enum member name: {0}'.format(','.join(invalid_names)))
        if '__doc__' not in classdict:
            classdict['__doc__'] = 'An enumeration.'
        enum_class = super().__new__(metacls, cls, bases, classdict)
        enum_class._member_names_ = []
        enum_class._member_map_ = OrderedDict()
        enum_class._member_type_ = member_type
        dynamic_attributes = {k for c in enum_class.mro() for k, v in c.__dict__.items() if isinstance(v, DynamicClassAttribute)}
        enum_class._value2member_map_ = {}
        if '__reduce_ex__' not in classdict:
            if member_type is not object:
                methods = ('__getnewargs_ex__', '__getnewargs__', '__reduce_ex__',
                           '__reduce__')
                if not any((m in member_type.__dict__ for m in methods)):
                    _make_class_unpicklable(enum_class)
        for member_name in classdict._member_names:
            value = enum_members[member_name]
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
                        if member_type is object:
                            enum_member._value_ = value
                        else:
                            enum_member._value_ = member_type(*args)
                    value = enum_member._value_
                    enum_member._name_ = member_name
                    enum_member.__objclass__ = enum_class
                    (enum_member.__init__)(*args)
                    for name, canonical_member in enum_class._member_map_.items():
                        if canonical_member._value_ == enum_member._value_:
                            enum_member = canonical_member
                            break
                    else:
                        enum_class._member_names_.append(member_name)

                    if member_name not in dynamic_attributes:
                        setattr(enum_class, member_name, enum_member)
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

        if Enum is not None:
            if save_new:
                enum_class.__new_member__ = __new__
            enum_class.__new__ = Enum.__new__
        if _order_ is not None:
            if isinstance(_order_, str):
                _order_ = _order_.replace(',', ' ').split()
            if _order_ != enum_class._member_names_:
                raise TypeError('member order does not match _order_')
        return enum_class

    def __bool__(self):
        """
        classes/types should always be True.
        """
        return True

    def __call__(cls, value, names=None, *, module=None, qualname=None, type=None, start=1):
        """Either returns an existing member, or creates a new enum class.

        This method is used both when an enum class is given a value to match
        to an enumeration member (i.e. Color(3)) and for the functional API
        (i.e. Color = Enum('Color', names='RED GREEN BLUE')).

        When used for the functional API:

        `value` will be the name of the new class.

        `names` should be either a string of white-space/comma delimited names
        (values will start at `start`), or an iterator/mapping of name, value pairs.

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
        return cls._create_(value, names, module=module, qualname=qualname, type=type, start=start)

    def __contains__(cls, member):
        if not isinstance(member, Enum):
            import warnings
            warnings.warn('using non-Enums in containment checks will raise TypeError in Python 3.8', DeprecationWarning, 2)
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

        We use __getattr__ instead of descriptors or inserting into the enum
        class' __dict__ in order to support `name` and `value` being both
        properties for enum members (which live in the class' __dict__) and
        enum members themselves.

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
        member_map = cls.__dict__.get('_member_map_', {})
        if name in member_map:
            raise AttributeError('Cannot reassign members.')
        super().__setattr__(name, value)

    def _create_(cls, class_name, names, *, module=None, qualname=None, type=None, start=1):
        """Convenience method to create a new Enum class.

        `names` can be:

        * A string containing member names, separated either with spaces or
          commas.  Values are incremented by 1 from `start`.
        * An iterable of member names.  Values are incremented by 1 from `start`.
        * An iterable of (member name, value) pairs.
        * A mapping of member name -> value pairs.

        """
        metacls = cls.__class__
        bases = (cls,) if type is None else (type, cls)
        _, first_enum = cls._get_mixins_(bases)
        classdict = metacls.__prepare__(class_name, bases)
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
        elif isinstance(names, (tuple, list)):
            if names:
                if isinstance(names[0], str):
                    original_names, names = names, []
                    last_values = []
                    for count, name in enumerate(original_names):
                        value = first_enum._generate_next_value_(name, start, count, last_values[:])
                        last_values.append(value)
                        names.append((name, value))

            else:
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
                    except (AttributeError, ValueError, KeyError) as exc:
                        try:
                            pass
                        finally:
                            exc = None
                            del exc

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
            return (
             object, Enum)

        def _find_data_type(bases):
            for chain in bases:
                for base in chain.__mro__:
                    if base is object:
                        continue

        first_enum = bases[(-1)]
        if not issubclass(first_enum, Enum):
            raise TypeError('new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`')
        member_type = _find_data_type(bases) or object
        if first_enum._member_names_:
            raise TypeError('Cannot extend enumerations')
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

        elif __new__ is object.__new__:
            use_args = False
        else:
            use_args = True
        return (
         __new__, save_new, use_args)


class Enum(metaclass=EnumMeta):
    __doc__ = 'Generic enumeration.\n\n    Derive from this class to define new enumerations.\n\n    '

    def __new__(cls, value):
        if type(value) is cls:
            return value
            try:
                return cls._value2member_map_[value]
            except KeyError:
                pass
            except TypeError:
                for member in cls._member_map_.values():
                    if member._value_ == value:
                        return member

            try:
                exc = None
                result = cls._missing_(value)
            except Exception as e:
                try:
                    exc = e
                    result = None
                finally:
                    e = None
                    del e

            if isinstance(result, cls):
                return result
            ve_exc = ValueError('%r is not a valid %s' % (value, cls.__name__))
            if result is None and exc is None:
                raise ve_exc
        elif exc is None:
            exc = TypeError('error in %s._missing_: returned %r instead of None or a valid member' % (
             cls.__name__, result))
        exc.__context__ = ve_exc
        raise exc

    def _generate_next_value_(name, start, count, last_values):
        for last_value in reversed(last_values):
            try:
                return last_value + 1
            except TypeError:
                pass

        else:
            return start

    @classmethod
    def _missing_(cls, value):
        raise ValueError('%r is not a valid %s' % (value, cls.__name__))

    def __repr__(self):
        return '<%s.%s: %r>' % (
         self.__class__.__name__, self._name_, self._value_)

    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)

    def __dir__(self):
        added_behavior = [m for cls in self.__class__.mro() if m[0] != '_' if m not in self._member_map_ for m in cls if m not in self._member_map_]
        return [
         '__class__', '__doc__', '__module__'] + added_behavior

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

    @classmethod
    def _convert(cls, name, module, filter, source=None):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        module_globals = vars(sys.modules[module])
        if source:
            source = vars(source)
        else:
            source = module_globals
        members = [(name, source[name]) for name in source.keys() if filter(name)]
        try:
            members.sort(key=(lambda t: (t[1], t[0])))
        except TypeError:
            members.sort(key=(lambda t: t[0]))

        cls = cls(name, members, module=module)
        cls.__reduce_ex__ = _reduce_ex_by_name
        module_globals.update(cls.__members__)
        module_globals[name] = cls
        return cls


class IntEnum(int, Enum):
    __doc__ = 'Enum where members are also (and must be) ints'


def _reduce_ex_by_name(self, proto):
    return self.name


class Flag(Enum):
    __doc__ = 'Support for flags'

    def _generate_next_value_(name, start, count, last_values):
        """
        Generate the next value when not given.

        name: the name of the member
        start: the initital start value or None
        count: the number of existing members
        last_value: the last value assigned or None
        """
        if not count:
            if start is not None:
                return start
            return 1
        for last_value in reversed(last_values):
            try:
                high_bit = _high_bit(last_value)
                break
            except Exception:
                raise TypeError('Invalid Flag value: %r' % last_value) from None

        return 2 ** (high_bit + 1)

    @classmethod
    def _missing_(cls, value):
        original_value = value
        if value < 0:
            value = ~value
        possible_member = cls._create_pseudo_member_(value)
        if original_value < 0:
            possible_member = ~possible_member
        return possible_member

    @classmethod
    def _create_pseudo_member_(cls, value):
        """
        Create a composite member iff value contains only members.
        """
        pseudo_member = cls._value2member_map_.get(value, None)
        if pseudo_member is None:
            _, extra_flags = _decompose(cls, value)
            if extra_flags:
                raise ValueError('%r is not a valid %s' % (value, cls.__name__))
            pseudo_member = object.__new__(cls)
            pseudo_member._name_ = None
            pseudo_member._value_ = value
            pseudo_member = cls._value2member_map_.setdefault(value, pseudo_member)
        return pseudo_member

    def __contains__(self, other):
        if not isinstance(other, self.__class__):
            import warnings
            warnings.warn('using non-Flags in containment checks will raise TypeError in Python 3.8', DeprecationWarning, 2)
            return False
        return other._value_ & self._value_ == other._value_

    def __repr__(self):
        cls = self.__class__
        if self._name_ is not None:
            return '<%s.%s: %r>' % (cls.__name__, self._name_, self._value_)
        members, uncovered = _decompose(cls, self._value_)
        return '<%s.%s: %r>' % (
         cls.__name__,
         '|'.join([str(m._name_ or m._value_) for m in members]),
         self._value_)

    def __str__(self):
        cls = self.__class__
        if self._name_ is not None:
            return '%s.%s' % (cls.__name__, self._name_)
        members, uncovered = _decompose(cls, self._value_)
        if len(members) == 1:
            if members[0]._name_ is None:
                return '%s.%r' % (cls.__name__, members[0]._value_)
        return '%s.%s' % (
         cls.__name__,
         '|'.join([str(m._name_ or m._value_) for m in members]))

    def __bool__(self):
        return bool(self._value_)

    def __or__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value_ | other._value_)

    def __and__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value_ & other._value_)

    def __xor__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value_ ^ other._value_)

    def __invert__(self):
        members, uncovered = _decompose(self.__class__, self._value_)
        inverted = self.__class__(0)
        for m in self.__class__:
            if m not in members:
                inverted = m._value_ & self._value_ or inverted | m

        return self.__class__(inverted)


class IntFlag(int, Flag):
    __doc__ = 'Support for integer-based Flags'

    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__name__))
        new_member = cls._create_pseudo_member_(value)
        return new_member

    @classmethod
    def _create_pseudo_member_(cls, value):
        pseudo_member = cls._value2member_map_.get(value, None)
        if pseudo_member is None:
            need_to_create = [
             value]
            _, extra_flags = _decompose(cls, value)
            while extra_flags:
                bit = _high_bit(extra_flags)
                flag_value = 2 ** bit
                if flag_value not in cls._value2member_map_:
                    if flag_value not in need_to_create:
                        need_to_create.append(flag_value)
                if extra_flags == -flag_value:
                    extra_flags = 0
                else:
                    extra_flags ^= flag_value

            for value in reversed(need_to_create):
                pseudo_member = int.__new__(cls, value)
                pseudo_member._name_ = None
                pseudo_member._value_ = value
                pseudo_member = cls._value2member_map_.setdefault(value, pseudo_member)

        return pseudo_member

    def __or__(self, other):
        if not isinstance(other, (self.__class__, int)):
            return NotImplemented
        result = self.__class__(self._value_ | self.__class__(other)._value_)
        return result

    def __and__(self, other):
        if not isinstance(other, (self.__class__, int)):
            return NotImplemented
        return self.__class__(self._value_ & self.__class__(other)._value_)

    def __xor__(self, other):
        if not isinstance(other, (self.__class__, int)):
            return NotImplemented
        return self.__class__(self._value_ ^ self.__class__(other)._value_)

    __ror__ = __or__
    __rand__ = __and__
    __rxor__ = __xor__

    def __invert__(self):
        result = self.__class__(~self._value_)
        return result


def _high_bit(value):
    """returns index of highest bit, or -1 if value is zero or negative"""
    return value.bit_length() - 1


def unique(enumeration):
    """Class decorator for enumerations ensuring unique member values."""
    duplicates = []
    for name, member in enumeration.__members__.items():
        if name != member.name:
            duplicates.append((name, member.name))

    if duplicates:
        alias_details = ', '.join(['%s -> %s' % (alias, name) for alias, name in duplicates])
        raise ValueError('duplicate values found in %r: %s' % (
         enumeration, alias_details))
    return enumeration


def _decompose(flag, value):
    """Extract all members from the value."""
    not_covered = value
    negative = value < 0
    if negative:
        flags_to_check = [(m, v) for v, m in list(flag._value2member_map_.items()) if m.name is not None]
    else:
        flags_to_check = [(m, v) for v, m in list(flag._value2member_map_.items()) if not m.name is not None if _power_of_two(v)]
    members = []
    for member, member_value in flags_to_check:
        if member_value and member_value & value == member_value:
            members.append(member)
            not_covered &= ~member_value

    if not members:
        if value in flag._value2member_map_:
            members.append(flag._value2member_map_[value])
    members.sort(key=(lambda m: m._value_), reverse=True)
    if len(members) > 1:
        if members[0].value == value:
            members.pop(0)
    return (
     members, not_covered)


def _power_of_two(value):
    if value < 1:
        return False
    return value == 2 ** _high_bit(value)
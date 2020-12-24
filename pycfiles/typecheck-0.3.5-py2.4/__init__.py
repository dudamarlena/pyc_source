# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/typecheck/__init__.py
# Compiled at: 2006-05-27 18:48:04
__all__ = [
 'accepts', 'returns', 'yields', 'TypeCheckError', 'Length', 'Empty', 'TypeSignatureError', 'And', 'Any', 'Class', 'Exact', 'HasAttr', 'IsAllOf', 'IsCallable', 'IsIterable', 'IsNoneOf', 'IsOneOf', 'IsOnlyOneOf', 'Not', 'Or', 'Self', 'Xor', 'YieldSeq', 'register_type', 'is_registered_type', 'unregister_type', 'Function']
import inspect, types
from types import GeneratorType, FunctionType, MethodType, ClassType, TypeType
enable_checking = True

def check_type(type, func, val):
    type.__typecheck__(func, val)


class _TC_Exception(Exception):
    __module__ = __name__

    def error_message(self):
        raise NotImplementedError('Incomplete _TC_Exception subclass (%s)' % str(self.__class__))

    def format_bad_object(self, bad_object):
        return (
         'for %s, ' % str(bad_object), self)


class _TC_LengthError(_TC_Exception):
    __module__ = __name__

    def __init__(self, wrong, right=None):
        _TC_Exception.__init__(self)
        self.wrong = wrong
        self.right = right

    def error_message(self):
        m = None
        if self.right is not None:
            m = ', expected %d' % self.right
        return 'length was %d%s' % (self.wrong, m or '')


class _TC_TypeError(_TC_Exception):
    __module__ = __name__

    def __init__(self, wrong, right):
        _TC_Exception.__init__(self)
        self.wrong = calculate_type(wrong)
        self.right = right

    def error_message(self):
        return 'expected %s, got %s' % (self.right, self.wrong)


class _TC_NestedError(_TC_Exception):
    __module__ = __name__

    def __init__(self, inner_exception):
        self.inner = inner_exception

    def error_message(self):
        try:
            return ', ' + self.inner.error_message()
        except:
            print "'%s'" % self.inner.message
            raw_input()
            raise


class _TC_IndexError(_TC_NestedError):
    __module__ = __name__

    def __init__(self, index, inner_exception):
        _TC_NestedError.__init__(self, inner_exception)
        self.index = index

    def error_message(self):
        return 'at index %d' % self.index + _TC_NestedError.error_message(self)


class _TC_DictError(_TC_NestedError):
    __module__ = __name__

    def format_bad_object(self, bad_object):
        message = 'for {%s}, ' % (', ').join([ '%s: %s' % (repr(k), repr(bad_object[k])) for k in sorted(bad_object.keys()) ])
        if not isinstance(self.inner, _TC_LengthError):
            return (
             message, self)
        return (
         message, self.inner)

    def error_message(self):
        raise NotImplementedError('Incomplete _TC_DictError subclass: ' + str(self.__class__))


class _TC_KeyError(_TC_DictError):
    __module__ = __name__

    def __init__(self, key, inner_exception):
        _TC_NestedError.__init__(self, inner_exception)
        self.key = key

    def error_message(self):
        return 'for key %s' % repr(self.key) + _TC_NestedError.error_message(self)


class _TC_KeyValError(_TC_KeyError):
    __module__ = __name__

    def __init__(self, key, val, inner_exception):
        _TC_KeyError.__init__(self, key, inner_exception)
        self.val = val

    def error_message(self):
        return 'at key %s, value %s' % (repr(self.key), repr(self.val)) + _TC_NestedError.error_message(self)


class _TC_GeneratorError(_TC_NestedError):
    __module__ = __name__

    def __init__(self, yield_no, inner_exception):
        _TC_NestedError.__init__(self, inner_exception)
        self.yield_no = yield_no

    def error_message(self):
        raise RuntimeError('_TC_GeneratorError.message should never be called')

    def format_bad_object(self, bad_object):
        (bad_obj, start_message) = self.inner.format_bad_object(bad_object)
        message = 'At yield #%d: %s' % (self.yield_no, bad_obj)
        return (message, start_message)


class _TC_AttrException(_TC_Exception):
    __module__ = __name__

    def __init__(self, attr):
        _TC_Exception.__init__(self, attr)
        self.attr = attr


class _TC_AttrError(_TC_AttrException, _TC_NestedError):
    __module__ = __name__

    def __init__(self, attr, inner_exception):
        _TC_AttrException.__init__(self, attr)
        _TC_NestedError.__init__(self, inner_exception)

    def error_message(self):
        return 'as for attribute %s' % self.attr + _TC_NestedError.error_message(self)


class _TC_MissingAttrError(_TC_AttrException):
    __module__ = __name__

    def error_message(self):
        return 'missing attribute %s' % self.attr


class _TC_YieldCountError(_TC_Exception):
    __module__ = __name__

    def __init__(self, expected):
        _TC_Exception.__init__(self, expected)
        self.expected = expected

    def format_bad_object(self, bad_object):
        return (
         '', self)

    def error_message(self):
        plural = 's'
        if self.expected == 1:
            plural = ''
        return 'only expected the generator to yield %d time%s' % (self.expected, plural)


class _TC_XorError(_TC_NestedError):
    __module__ = __name__

    def __init__(self, matched_conds, inner_exception):
        assert matched_conds in (0, 2)
        assert isinstance(inner_exception, _TC_TypeError)
        _TC_Exception.__init__(self, matched_conds, inner_exception)
        _TC_NestedError.__init__(self, inner_exception)
        self.matched_conds = matched_conds

    def error_message(self):
        if self.matched_conds == 0:
            m = 'neither assertion'
        else:
            m = 'both assertions'
        return _TC_NestedError.error_message(self) + ' (matched %s)' % m


class _TC_FunctionError(_TC_Exception):
    __module__ = __name__

    def __init__(self, checking_func, obj):
        self.checking_func = checking_func
        self.rejected_obj = obj

    def error_message(self):
        return ' was rejected by %s' % self.checking_func

    def format_bad_object(self, bad_object):
        return (
         str(bad_object), self)


class _TC_ExactError(_TC_Exception):
    __module__ = __name__

    def __init__(self, wrong, right):
        self.wrong = wrong
        self.right = right

    def error_message(self):
        return 'expected %s, got %s' % (self.right, self.wrong)


class _TS_Exception(Exception):
    __module__ = __name__

    def error_message(self):
        raise NotImplementedError('Incomplete _TS_Exception subclass (%s)' % str(self.__class__))


class _TS_TupleError(_TS_Exception):
    __module__ = __name__

    def __init__(self, parameters, types):
        parameters = _rec_tuple(parameters)
        types = _rec_tuple(types)
        _TS_Exception.__init__(self, parameters, types)
        self.parameters = parameters
        self.types = types

    def error_message(self):
        return 'the signature type %s does not match %s' % (str(self.types), str(self.parameters))


class _TS_ExtraKeywordError(_TS_Exception):
    __module__ = __name__

    def __init__(self, keyword):
        _TS_Exception.__init__(self, keyword)
        self.keyword = keyword

    def error_message(self):
        return "the keyword '%s' in the signature is not in the function" % self.keyword


class _TS_ExtraPositionalError(_TS_Exception):
    __module__ = __name__

    def __init__(self, type):
        _TS_Exception.__init__(self, type)
        self.type = type

    def error_message(self):
        return 'an extra positional type has been supplied'


class _TS_MissingTypeError(_TS_Exception):
    __module__ = __name__

    def __init__(self, parameter):
        _TS_Exception.__init__(self, parameter)
        self.parameter = parameter

    def error_message(self):
        return "parameter '%s' lacks a type" % self.parameter


class _TS_TwiceTypedError(_TS_Exception):
    __module__ = __name__

    def __init__(self, parameter, kw_type, pos_type):
        _TS_Exception.__init__(self, parameter, kw_type, pos_type)
        self.parameter = parameter
        self.kw_type = kw_type
        self.pos_type = pos_type

    def error_message(self):
        return "parameter '%s' is provided two types (%s and %s)" % (self.parameter, str(self.kw_type), str(self.pos_type))


_hooks = ('__typesig__', '__startchecking__', '__stopchecking__', '__switchchecking__')
_registered_types = set()
_registered_hooks = dict([ (_h, set()) for _h in _hooks ])

def _manage_registration(add_remove, reg_type):
    if not isinstance(reg_type, (types.ClassType, types.TypeType)):
        raise ValueError('registered types must be classes or types')
    valid = False
    for hook in _hooks:
        if hasattr(reg_type, hook):
            getattr(_registered_hooks[hook], add_remove)(reg_type)
            valid = True

    if valid:
        getattr(_registered_types, add_remove)(reg_type)
    else:
        raise ValueError('registered types must have at least one of the following methods: ' + (', ').join(_hooks))


def register_type(reg_type):
    _manage_registration('add', reg_type)


def unregister_type(reg_type):
    _manage_registration('remove', reg_type)


def is_registered_type(reg_type):
    return reg_type in _registered_types


def Type(obj):
    for reg_type in _registered_hooks['__typesig__']:
        v = reg_type.__typesig__(obj)
        if v is not None:
            return v

    raise AssertionError("Object is of type '%s'; not a type" % str(type(obj)))
    return


def __checking(start_stop, *args):
    attr = '__%schecking__' % start_stop
    for reg_type in _registered_hooks[attr]:
        getattr(reg_type, attr)(*args)


def start_checking(function):
    __checking('start', function)


def stop_checking(function):
    __checking('stop', function)


def switch_checking(from_func, to_func):
    for reg_type in _registered_types:
        if hasattr(reg_type, '__switchchecking__'):
            getattr(reg_type, '__switchchecking__')(from_func, to_func)
        else:
            if hasattr(reg_type, '__stopchecking__'):
                getattr(reg_type, '__stopchecking__')(from_func)
            if hasattr(reg_type, '__startchecking__'):
                getattr(reg_type, '__startchecking__')(to_func)


def calculate_type(obj):
    if isinstance(obj, types.InstanceType):
        return obj.__class__
    elif isinstance(obj, dict):
        if len(obj) == 0:
            return {}
        key_types = set()
        val_types = set()
        for (k, v) in obj.items():
            key_types.add(calculate_type(k))
            val_types.add(calculate_type(v))

        if len(key_types) == 1:
            key_types = key_types.pop()
        else:
            key_types = Or(*key_types)
        if len(val_types) == 1:
            val_types = val_types.pop()
        else:
            val_types = Or(*val_types)
        return {key_types: val_types}
    elif isinstance(obj, tuple):
        return tuple([ calculate_type(t) for t in obj ])
    elif isinstance(obj, list):
        length = len(obj)
        if length == 0:
            return []
        obj = [ calculate_type(o) for o in obj ]
        partitions = [
         1]
        partitions.extend([ i for i in range(2, int(length / 2) + 1) if length % i == 0 ])
        partitions.append(length)

        def evaluate(items_per):
            parts = length / items_per
            for i in range(0, parts):
                for j in range(0, items_per):
                    if obj[(items_per * i + j)] != obj[j]:
                        raise StopIteration

            return obj[0:items_per]

        for items_per in partitions:
            try:
                return evaluate(items_per)
            except StopIteration:
                continue

    else:
        return type(obj)


class CheckType(object):
    __module__ = __name__

    def __repr__(self):
        return type(self).name + '(' + (', ').join(sorted((repr(t) for t in self._types))) + ')'

    __str__ = __repr__

    def __eq__(self, other):
        return not self != other

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        raise NotImplementedError('Incomplete CheckType subclass: %s' % self.__class__)

    def __typecheck__(self, func, obj):
        raise NotImplementedError('Incomplete CheckType subclass: %s' % self.__class__)

    @classmethod
    def __typesig__(cls, obj):
        if isinstance(obj, CheckType):
            return obj


class Single(CheckType):
    __module__ = __name__
    name = 'Single'

    def __init__(self, type):
        if not isinstance(type, (types.ClassType, types.TypeType)):
            raise TypeError('Cannot type-check a %s' % type(type))
        else:
            self.type = type
        self._types = [self.type]

    def __typecheck__(self, func, to_check):
        if not isinstance(to_check, self.type):
            raise _TC_TypeError(to_check, self.type)

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return False
        return self.type == other.type

    def __hash__(self):
        return hash(str(hash(self.__class__)) + str(hash(self.type)))

    def __repr__(self):
        return repr(self.type)

    @classmethod
    def __typesig__(cls, obj):
        if isinstance(obj, (types.ClassType, types.TypeType)):
            return Single(obj)


class Empty(Single):
    __module__ = __name__
    name = 'Empty'

    def __init__(self, type):
        if not hasattr(type, '__len__'):
            raise TypeError('Can only assert emptyness for types with __len__ methods')
        Single.__init__(self, type)

    def __typecheck__(self, func, to_check):
        Single.__typecheck__(self, func, to_check)
        if len(to_check) > 0:
            err = _TC_LengthError(len(to_check), 0)
            if isinstance(to_check, dict):
                raise _TC_DictError(err)
            raise err


class Dict(CheckType):
    __module__ = __name__
    name = 'Dict'

    def __init__(self, key, val):
        self.__check_key = Type(key)
        self.__check_val = Type(val)
        self.type = {key: val}
        self._types = [
         key, val]

    def __typecheck__(self, func, to_check):
        if not isinstance(to_check, types.DictType):
            raise _TC_TypeError(to_check, self.type)
        for (k, v) in to_check.items():
            try:
                check_type(self.__check_key, func, k)
            except _TC_Exception, inner:
                raise _TC_KeyError(k, inner)

            try:
                check_type(self.__check_val, func, v)
            except _TC_Exception, inner:
                raise _TC_KeyValError(k, v, inner)

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return False
        return self.type == other.type

    def __hash__(self):
        cls = self.__class__
        key = self.__check_key
        val = self.__check_val

        def strhash(obj):
            return str(hash(obj))

        return hash(('').join(map(strhash, [cls, key, val])))

    @classmethod
    def __typesig__(cls, obj):
        if isinstance(obj, dict):
            if len(obj) == 0:
                return Empty(dict)
            return Dict(obj.keys()[0], obj.values()[0])


class List(CheckType):
    __module__ = __name__
    name = 'List'

    def __init__(self, *type):
        self._types = [ Type(t) for t in type ]
        self.type = [ t.type for t in self._types ]

    def __typecheck__(self, func, to_check):
        if not isinstance(to_check, list):
            raise _TC_TypeError(to_check, self.type)
        if len(to_check) % len(self._types):
            raise _TC_LengthError(len(to_check))
        pat_len = len(self._types)
        type_tuples = [ (i, val, self._types[(i % pat_len)]) for (i, val) in enumerate(to_check) ]
        for (i, val, type) in type_tuples:
            try:
                check_type(type, func, val)
            except _TC_Exception, e:
                raise _TC_IndexError(i, e)

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return False
        if len(self._types) != len(other._types):
            return False
        for (s, o) in zip(self._types, other._types):
            if s != o:
                return False

        return True

    def __hash__(self):

        def strhash(obj):
            return str(hash(obj))

        return hash(('').join(map(strhash, [self.__class__] + self._types)))

    @classmethod
    def __typesig__(cls, obj):
        if isinstance(obj, list):
            if len(obj) == 0:
                return Empty(list)
            return List(*obj)


class Tuple(List):
    __module__ = __name__
    name = 'Tuple'

    def __init__(self, *type):
        List.__init__(self, *type)
        self.type = tuple(self.type)

    def __typecheck__(self, func, to_check):
        if not isinstance(to_check, types.TupleType) or len(to_check) != len(self._types):
            raise _TC_TypeError(to_check, self.type)
        for (i, (val, type)) in enumerate(zip(to_check, self._types)):
            try:
                check_type(type, func, val)
            except _TC_Exception, inner:
                raise _TC_IndexError(i, inner)

    @classmethod
    def __typesig__(cls, obj):
        if isinstance(obj, tuple):
            return Tuple(*obj)


class TypeVariables(CheckType):
    __module__ = __name__
    __mapping_stack = []
    __active_mapping = None
    __gen_mappings = {}

    def __init__(self, name):
        self.type = name

    def __str__(self):
        return 'TypeVariable(%s)' % self.type

    __repr__ = __str__

    def __hash__(self):
        return hash(('').join([ str(o) for o in (self.__class__, hash(type(self.type)), hash(self.type)) ]))

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return type(self.type) is type(other.type) and self.type == other.type

    def __typecheck__(self, func, to_check):
        name = self.type
        if isinstance(func, GeneratorType):
            active = self.__class__.__gen_mappings[func]
        else:
            active = self.__class__.__active_mapping
        lookup = (
         name, type(name))
        if lookup in active:
            check_type(active[lookup], func, to_check)
        else:
            active[lookup] = Type(calculate_type(to_check))

    @classmethod
    def __typesig__(cls, obj):
        if isinstance(obj, basestring):
            return cls(obj)

    @classmethod
    def __startchecking__(cls, func):
        if isinstance(func, GeneratorType):
            cls.__gen_mappings.setdefault(func, {})
        elif isinstance(func, FunctionType):
            cls.__mapping_stack.append(cls.__active_mapping)
            cls.__active_mapping = {}
        else:
            raise TypeError(func)

    @classmethod
    def __switchchecking__(cls, from_func, to_func):
        if isinstance(from_func, FunctionType):
            if isinstance(to_func, GeneratorType):
                cls.__gen_mappings[to_func] = cls.__active_mapping
                cls.__stopchecking__(from_func)
            elif isinstance(to_func, FunctionType):
                cls.__stopchecking__(from_func)
                cls.__startchecking__(to_func)
            else:
                raise TypeError(to_func)
        else:
            raise TypeError(from_func)

    @classmethod
    def __stopchecking__(cls, func):
        if isinstance(func, GeneratorType):
            del cls.__gen_mappings[func]
        elif isinstance(func, FunctionType):
            cls.__active_mapping = cls.__mapping_stack.pop()
        else:
            raise TypeError(func)


class Function(CheckType):
    __module__ = __name__

    def __init__(self, func):
        self._func = func
        self.type = self

    @classmethod
    def __typesig__(cls, obj):
        if isinstance(obj, (FunctionType, MethodType)):
            return cls(obj)
        if type(obj) not in (types.ClassType, type) and callable(obj):
            return cls(obj)

    def __typecheck__(self, func, to_check):
        if False == self._func(to_check):
            raise _TC_FunctionError(self._func, to_check)

    def __str__(self):
        return 'Function(%s)' % self._func

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return self._func is other._func

    def __hash__(self):
        return hash(str(self.__class__) + str(hash(self._func)))


for c in (CheckType, List, Tuple, Dict, Single, TypeVariables, Function):
    register_type(c)

class Any(CheckType):
    __module__ = __name__
    name = 'Any'

    def __init__(self):
        self.type = object

    def __typecheck__(self, func, to_check):
        pass

    def __str__(self):
        return 'Any()'

    __repr__ = __str__

    def __eq__(self, other):
        return other.__class__ is self.__class__

    def __hash__(self):
        return hash(self.__class__)


class _Boolean(CheckType):
    __module__ = __name__

    def __init__(self, first_type, second_type, *types):
        self._types = set()
        for t in (first_type, second_type) + types:
            if type(t) is type(self):
                self._types.update(t._types)
            else:
                self._types.add(Type(t))

        if len(self._types) < 2:
            raise TypeError('there must be at least 2 distinct parameters to __init__()')
        self.type = self

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return False
        return self._types == other._types

    def __hash__(self):
        return hash(str(hash(self.__class__)) + str(hash(frozenset(self._types))))


class Or(_Boolean):
    __module__ = __name__
    name = 'Or'

    def __typecheck__(self, func, to_check):
        for type in self._types:
            try:
                check_type(type, func, to_check)
                return
            except _TC_Exception:
                pass

        raise _TC_TypeError(to_check, self)


class And(_Boolean):
    __module__ = __name__
    name = 'And'

    def __typecheck__(self, func, to_check):
        for type in self._types:
            try:
                check_type(type, func, to_check)
            except _TC_Exception, e:
                raise _TC_TypeError(to_check, self)


class Not(Or):
    __module__ = __name__
    name = 'Not'

    def __init__(self, first_type, *types):
        self._types = set([ Type(t) for t in (first_type,) + types ])
        self.type = self

    def __typecheck__(self, func, to_check):
        try:
            Or.__typecheck__(self, func, to_check)
        except _TC_Exception:
            return

        raise _TC_TypeError(to_check, self)


class Xor(_Boolean):
    __module__ = __name__
    name = 'Xor'

    def __typecheck__(self, func, to_check):
        already_met_1_cond = False
        for typ in self._types:
            try:
                check_type(typ, func, to_check)
            except _TC_Exception:
                pass
            else:
                if already_met_1_cond:
                    raise _TC_XorError(2, _TC_TypeError(to_check, self))
                already_met_1_cond = True

        if not already_met_1_cond:
            raise _TC_XorError(0, _TC_TypeError(to_check, self))


class IsCallable(CheckType):
    __module__ = __name__

    def __init__(self):
        self.type = self

    def __str__(self):
        return 'IsCallable()'

    __repr__ = __str__

    def __hash__(self):
        return id(self.__class__)

    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __typecheck__(self, func, to_check):
        if not callable(to_check):
            raise _TC_TypeError(to_check, 'a callable')


class HasAttr(CheckType):
    __module__ = __name__

    def __init__(self, set_1, set_2=None):
        attr_sets = {list: [], dict: {}}
        for (arg_1, arg_2) in ((set_1, set_2), (set_2, set_1)):
            for t in (list, dict):
                if isinstance(arg_1, t):
                    attr_sets[t] = arg_1
                    if isinstance(arg_2, t):
                        raise TypeError('can only have one list and/or one dict')

        self._attr_types = dict.fromkeys(attr_sets[list], Any())
        for (attr, typ) in attr_sets[dict].items():
            self._attr_types[attr] = Type(typ)

    def __typecheck__(self, func, to_check):
        for (attr, typ) in self._attr_types.items():
            if not hasattr(to_check, attr):
                raise _TC_MissingAttrError(attr)
            try:
                check_type(typ, func, getattr(to_check, attr))
            except _TC_Exception, e:
                raise _TC_AttrError(attr, e)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return self._attr_types == other._attr_types

    def __hash__(self):
        return hash(str(hash(self.__class__)) + str(hash(str(self._attr_types))))

    def __str__(self):
        any_type = []
        spec_type = {}
        any = Any()
        for (attr, typ) in self._attr_types.items():
            if typ == any:
                any_type.append(attr)
            else:
                spec_type[attr] = typ

        msg = [ t for t in (any_type, spec_type) if len(t) ]
        return 'HasAttr(' + (', ').join(map(str, msg)) + ')'

    __repr__ = __str__


class IsIterable(CheckType):
    __module__ = __name__

    def __init__(self):
        self.type = self

    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __hash__(self):
        return id(self.__class__)

    def __str__(self):
        return 'IsIterable()'

    __repr__ = __str__

    def __typecheck__(self, func, to_check):
        if not (hasattr(to_check, '__iter__') and callable(to_check.__iter__)):
            raise _TC_TypeError(to_check, 'an iterable')


class YieldSeq(CheckType):
    __module__ = __name__
    _index_map = {}

    def __init__(self, type_1, type_2, *types):
        self.type = self
        self._type = [
         type_1, type_2] + list(types)
        self._types = [ Type(t) for t in self._type ]

    def __hash__(self):
        return id(self)

    def __str__(self):
        return 'YieldSeq(' + (', ').join(map(str, self._type)) + ')'

    __repr__ = __str__

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return self._types == other._types

    def __hash__(self):
        return hash(str(self.__class__) + str([ hash(t) for t in self._types ]))

    @classmethod
    def __startchecking__(cls, gen):
        if isinstance(gen, GeneratorType):
            cls._index_map[gen] = {}

    @classmethod
    def __stopchecking__(cls, gen):
        if gen in cls._index_map:
            del cls._index_map[gen]

    def __typecheck__(self, gen, to_check):
        index_map = self.__class__._index_map
        if self not in index_map[gen]:
            index_map[gen][self] = -1
        index = index_map[gen]
        if index[self] >= len(self._types) - 1:
            raise _TC_YieldCountError(len(self._types))
        index[self] += 1
        check_type(self._types[index[self]], gen, to_check)


register_type(YieldSeq)

class Exact(CheckType):
    __module__ = __name__

    def __init__(self, obj):
        self.type = self
        self._obj = obj

    def __hash__(self):
        try:
            obj_hash = str(hash(self._obj))
        except TypeError:
            obj_hash = str(type(self._obj)) + str(self._obj)

        return hash(str(self.__class__) + obj_hash)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return self._obj == other._obj

    def __typecheck__(self, func, to_check):
        if self._obj != to_check:
            raise _TC_ExactError(to_check, self._obj)


class Length(CheckType):
    __module__ = __name__

    def __init__(self, length):
        self.type = self
        self._length = int(length)

    def __hash__(self):
        return hash(str(self.__class__) + str(self._length))

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return self._length == other._length

    def __typecheck__(self, func, to_check):
        try:
            length = len(to_check)
        except TypeError:
            raise _TC_TypeError(to_check, 'something with a __len__ method')

        if length != self._length:
            raise _TC_LengthError(length, self._length)


import sys

class Class(CheckType):
    __module__ = __name__

    def __init__(self, class_name):
        self.type = self
        self.class_name = class_name
        self.class_obj = None
        self._frame = sys._getframe(1)
        return

    def __hash__(self):
        return hash(str(self.__class__) + self.class_name)

    def __str__(self):
        return "Class('%s')" % self.class_name

    __repr__ = __str__

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return self.class_name == other.class_name

    def __typecheck__(self, func, to_check):
        if self.class_obj is None:
            class_name = self.class_name
            frame = self._frame
            for f_dict in (frame.f_locals, frame.f_globals):
                if class_name in frame.f_locals:
                    if self is not frame.f_locals[class_name]:
                        self.class_obj = frame.f_locals[class_name]
                        self._frame = None
                        break
            else:
                raise NameError("name '%s' is not defined" % class_name)
        if not isinstance(to_check, self.class_obj):
            raise _TC_TypeError(to_check, self.class_obj)
        return


class Typeclass(CheckType):
    __module__ = __name__
    bad_members = dict.fromkeys(['__class__', '__new__', '__init__'], True)

    def __init__(self, *types):
        if len(types) == 0:
            raise TypeError('Must supply at least one type to __init__()')
        self.type = self
        self._cache = set()
        self._interface = set()
        self._instances = set()
        for t in types:
            self.add_instance(t)

        self._calculate_interface()

    def recalculate_interface(self):
        self._cache = self._instances.copy()
        self._calculate_interface()

    def instances(self):
        return list(self._instances)

    def interface(self):
        return list(self._interface)

    def has_instance(self, instance):
        return instance in self._instances

    def add_instance(self, instance):
        if isinstance(instance, self.__class__):
            for inst in instance.instances():
                self._instances.add(inst)
                self._cache.add(inst)

        elif isinstance(instance, (ClassType, TypeType)):
            self._instances.add(instance)
            self._cache.add(instance)
        else:
            raise TypeError('All instances must be classes or types')

    def intersect(self, other):
        if isinstance(other, self.__class__):
            new_instances = other.instances()
        else:
            new_instances = other
        self._instances.update(new_instances)
        self._cache.update(new_instances)
        self._calculate_interface()

    def _calculate_interface(self):
        bad_members = self.bad_members
        for instance in self._instances:
            inst_attrs = []
            for (attr, obj) in instance.__dict__.items():
                if callable(obj) and attr not in bad_members:
                    inst_attrs.append(attr)

            if len(self._interface) == 0:
                self._interface = set(inst_attrs)
            else:
                self._interface.intersection_update(inst_attrs)

    def __typecheck__(self, func, to_check):
        if to_check.__class__ in self._cache:
            return
        for method in self._interface:
            if not hasattr(to_check, method):
                raise _TC_MissingAttrError(method)
            attr = getattr(to_check, method)
            if not callable(attr):
                raise _TC_AttrError(method, _TC_TypeError(attr, IsCallable()))

        self._cache.add(to_check.__class__)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return self._instances == other._instances

    def __hash__(self):
        return hash(str(self.__class__) + str(hash(frozenset(self._instances))))

    def __repr__(self):
        return object.__repr__(self)

    def __str__(self):
        return 'Typeclass(' + (', ').join(map(str, self._instances)) + ')'


_Self = TypeVariables('this is the class of the invocant')

def Self():
    return _Self


IsOneOf = Or
IsAllOf = And
IsNoneOf = Not
IsOnlyOneOf = Xor

class TypeCheckException(Exception):
    __module__ = __name__


class TypeCheckError(TypeCheckException):
    __module__ = __name__

    def __init__(self, prefix, bad_object, exception):
        TypeCheckException.__init__(self, prefix, bad_object, exception)
        self.prefix = prefix
        self.internal = exception
        self.bad_object = bad_object
        (bad_obj_str, start_message) = exception.format_bad_object(bad_object)
        self.__message = prefix + bad_obj_str + start_message.error_message()

    def __str__(self):
        return self.__message


class TypeSignatureError(Exception):
    __module__ = __name__

    def __init__(self, internal_exc):
        Exception.__init__(self, internal_exc)
        self.internal = internal_exc
        self.__message = internal_exc.error_message()

    def __str__(self):
        return self.__message


def _rec_tuple(obj):
    if isinstance(obj, list):
        return tuple((_rec_tuple(o) for o in obj))
    return obj


def _rec_tuple_str(obj):
    if not isinstance(obj, (list, tuple)):
        return obj
    if len(obj) == 1:
        return '(%s,)' % obj
    return '(' + (', ').join((_rec_tuple_str(o) for o in obj)) + ')'


def _gen_arg_to_param(func, (posargs, varargs, varkw, defaults)):
    sig_args = list()
    dic_args = list()
    for obj in posargs:
        if isinstance(obj, list):
            rts = _rec_tuple_str(obj)
            sig_args.append(rts)
            dic_args.append((_rec_tuple(obj), rts))
        else:
            sig_args.append(str(obj))
            dic_args.append(('"%s"' % obj, obj))

    func_code = ''
    if varargs:
        dic_args.append(('"%s"' % varargs, varargs))
        sig_args.append('*' + varargs)
        func_code = '\n\t%s = list(%s)' % (varargs, varargs)
    if varkw:
        dic_args.append(('"%s"' % varkw, varkw))
        sig_args.append('**' + varkw)
    func_name = func.func_name + '_'
    while func_name in dic_args:
        func_name += '_'

    func_def = 'def %s(' % func.func_name
    func_return = func_code + '\n\treturn {' + (', ').join(('%s: %s' % kv for kv in dic_args)) + '}'
    locals = {}
    exec func_def + (',').join(sig_args) + '):' + func_return in locals
    func = locals[func.func_name]
    func.func_defaults = defaults
    return func


def _validate_tuple(ref, obj):
    if not isinstance(ref, (list, tuple)):
        return
    if not isinstance(obj, (list, tuple)):
        raise _TS_TupleError(ref, obj)
    if len(ref) != len(obj):
        raise _TS_TupleError(ref, obj)
    try:
        for (r, o) in zip(ref, obj):
            _validate_tuple(r, o)

    except _TS_TupleError:
        raise _TS_TupleError(ref, obj)


def _param_to_type((params, varg_name, kwarg_name), vargs, kwargs):
    vargs = list(vargs)
    kwargs = dict(kwargs)
    param_value = dict()
    if len(params) < len(vargs) and varg_name is None:
        raise _TS_ExtraPositionalError(vargs[len(params)])
    if len(params) > len(vargs) and len(kwargs) == 0:
        raise _TS_MissingTypeError(params[len(vargs)])
    if len(vargs):
        for (p, a) in zip(params, vargs):
            _validate_tuple(p, a)
            param_value[_rec_tuple(p)] = a

    if len(kwargs) > 0:
        params = set([ k for k in params if k not in param_value ])
        if kwarg_name and kwarg_name not in param_value:
            params.add(kwarg_name)
        if varg_name and varg_name not in param_value:
            params.add(varg_name)
        no_double_star = kwarg_name is None
        if len(params) == 0 and no_double_star:
            raise _TS_ExtraKeywordError(kwargs.keys()[0])
        for (p, a) in kwargs.items():
            if p in param_value:
                raise _TS_TwiceTypedError(p, a, param_value[p])
            if p not in params and no_double_star:
                raise _TS_ExtraKeywordError(p)
            _validate_tuple(p, a)
            params.remove(p)
            param_value[p] = a

        if len(params):
            raise _TS_MissingTypeError(params.pop())
    return param_value


def _make_fake_function(func):

    def fake_function(*vargs, **kwargs):
        start_checking(func)
        try:
            fake_function.__check_args(vargs, kwargs)
            result = func(*vargs, **kwargs)
        except:
            stop_checking(func)
            raise

        return fake_function.__check_result(func, result)

    def _pass_args(vargs, kwargs):
        pass

    def _pass_result(func, result):
        stop_checking(func)
        return result

    fake_function.__check_args = _pass_args
    fake_function.__check_result = _pass_result
    fake_function.__wrapped_func = func
    fake_function.__module__ = func.__module__
    fake_function.__name__ = func.__name__
    fake_function.__doc__ = func.__doc__
    return fake_function


def typecheck_args(*v_sig, **kw_sig):

    def decorator(func):
        if hasattr(func, '__wrapped_func'):
            if hasattr(func, 'type_args'):
                raise RuntimeError('Cannot use the same typecheck_* function more than once on the same function')
            wrapped_func = func.__wrapped_func
        else:
            wrapped_func = func
        (param_list, varg_name, kwarg_name, defaults) = inspect.getargspec(wrapped_func)
        args_to_params = _gen_arg_to_param(wrapped_func, (param_list, varg_name, kwarg_name, defaults))
        try:
            param_types = _param_to_type((param_list, varg_name, kwarg_name), v_sig, kw_sig)
        except _TS_Exception, e:
            raise TypeSignatureError(e)

        if varg_name:
            if not isinstance(param_types[varg_name], list):
                param_types[varg_name] = [
                 param_types[varg_name]]
        if kwarg_name:
            if not isinstance(param_types[kwarg_name], dict):
                param_types[kwarg_name] = {str: param_types[kwarg_name]}
        check_param_types = dict()
        for (k, v) in param_types.items():
            check_param_types[k] = Type(v)

        def __check_args(__vargs, __kwargs):
            if enable_checking:
                arg_dict = args_to_params(*__vargs, **__kwargs)
                try:
                    for (name, val) in arg_dict.items():
                        check_type(check_param_types[name], wrapped_func, val)

                except _TC_Exception, e:
                    str_name = _rec_tuple_str(name)
                    raise TypeCheckError('Argument %s: ' % str_name, val, e)

        if hasattr(func, '__check_result'):
            fake_function = func
        else:
            fake_function = _make_fake_function(func)
        fake_function.__check_args = __check_args
        fake_function.type_args = param_types
        return fake_function

    return decorator


def _decorator(signature, conflict_field, twice_field, check_result_func):

    def decorator(func):
        if hasattr(func, '__check_result'):
            if hasattr(func, conflict_field):
                raise RuntimeError('Cannot use typecheck_return and typecheck_yield on the same function')
            elif hasattr(func, twice_field):
                raise RuntimeError('Cannot use the same typecheck_* function more than once on the same function')
            fake_function = func
        else:
            fake_function = _make_fake_function(func)
        setattr(fake_function, twice_field, signature)
        fake_function.__check_result = check_result_func
        return fake_function

    return decorator


def typecheck_return(*signature):
    if len(signature) == 1:
        signature = signature[0]
    sig_types = Type(signature)

    def __check_return(func, return_vals):
        if enable_checking:
            try:
                check_type(sig_types, func, return_vals)
            except _TC_Exception, e:
                stop_checking(func)
                raise TypeCheckError('Return value: ', return_vals, e)

        stop_checking(func)
        return return_vals

    return _decorator(signature, 'type_yield', 'type_return', __check_return)


class Fake_generator(object):
    __module__ = __name__

    def __init__(self, real_gen, signature):
        self.type_yield = signature
        self.__yield_no = 0
        self.__real_gen = real_gen
        self.__sig_types = Type(signature)
        self.__needs_stopping = True

    def next(self):
        gen = self.__real_gen
        self.__yield_no += 1
        try:
            return_vals = gen.next()
        except StopIteration:
            if self.__needs_stopping:
                stop_checking(gen)
                self.__needs_stopping = False
            raise

        if enable_checking:
            try:
                check_type(self.__sig_types, gen, return_vals)
            except _TC_Exception, e:
                middle_exc = _TC_GeneratorError(self.__yield_no, e)
                raise TypeCheckError('', return_vals, middle_exc)

        return return_vals

    def __del__(self):
        if self.__needs_stopping:
            stop_checking(self.__real_gen)


def typecheck_yield(*signature):
    if len(signature) == 1:
        signature = signature[0]

    def __check_yield(func, gen):
        if not isinstance(gen, types.GeneratorType):
            stop_checking(func)
            raise TypeError('typecheck_yield only works for generators')
        switch_checking(func, gen)
        return Fake_generator(gen, signature)

    return _decorator(signature, 'type_return', 'type_yield', __check_yield)


typecheck = typecheck_args
accepts = typecheck_args
returns = typecheck_return
yields = typecheck_yield
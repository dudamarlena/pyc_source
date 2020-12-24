# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/utils/lazy.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 10790 bytes
import re, copy, operator
from functools import total_ordering, wraps
from rest_framework.utils.constants import empty

def new_method_proxy(func):
    """
    工厂函数
    先判断包装类是否已经实例化，否则实例它（通过实现_setup()方法实现
    :param func:
    :return:
    """

    def inner(self, *args):
        if self._wrapped is empty:
            self._setup()
        return func(self._wrapped, *args)

    return inner


def unpickle_lazyobject(wrapped):
    return wrapped


class LazyObject(object):
    __doc__ = '\n    延迟加载初始化实例\n    '
    _wrapped = None

    def __init__(self):
        """
        如果子类重写__init__()，它可能需要重写__copy__()和__deepcopy__()
        """
        self._wrapped = empty

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == '_wrapped':
            self.__dict__['_wrapped'] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == '_wrapped':
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)

    def _setup(self):
        """
        必须由子类实现初始化包装对象
        """
        raise NotImplementedError('subclasses of LazyObject must provide a _setup() method')

    def __reduce__(self):
        if self._wrapped is empty:
            self._setup()
        return (unpickle_lazyobject, (self._wrapped,))

    def __getstate__(self):
        return {}

    def __copy__(self):
        if self._wrapped is empty:
            return type(self)()
        else:
            return copy.copy(self._wrapped)

    def __deepcopy__(self, memo):
        if self._wrapped is empty:
            result = type(self)()
            memo[id(self)] = result
            return result
        else:
            return copy.deepcopy(self._wrapped, memo)

    __bytes__ = new_method_proxy(bytes)
    __str__ = new_method_proxy(str)
    __bool__ = new_method_proxy(bool)
    __dir__ = new_method_proxy(dir)
    __class__ = property(new_method_proxy(operator.attrgetter('__class__')))
    __eq__ = new_method_proxy(operator.eq)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)


class SimpleLazyObject(LazyObject):
    __doc__ = '\n    任何函数初始化的懒惰对象\n    此类主要为未知类型的复合对象设计的，对于内建或对象已知类型，使用lazy方法\n    '

    def __init__(self, func):
        self.__dict__['_setupfunc'] = func
        super(SimpleLazyObject, self).__init__()

    def _setup(self):
        self._wrapped = self._setupfunc()

    def __repr__(self):
        if self._wrapped is empty:
            repr_attr = self._setupfunc
        else:
            repr_attr = self._wrapped
        return '<%s: %r>' % (type(self).__name__, repr_attr)

    def __copy__(self):
        if self._wrapped is empty:
            return SimpleLazyObject(self._setupfunc)
        else:
            return copy.copy(self._wrapped)

    def __deepcopy__(self, memo):
        if self._wrapped is empty:
            result = SimpleLazyObject(self._setupfunc)
            memo[id(self)] = result
            return result
        else:
            return copy.deepcopy(self._wrapped, memo)


class Promise(object):
    __doc__ = '\n    This is just a base class for the proxy class created in\n    the closure of the lazy function. It can be used to recognize\n    promises in code.\n    '


def lazy(func, *resultclasses):
    """
    Turns any callable into a lazy evaluated callable. You need to give result
    classes or types -- at least one is needed so that the automatic forcing of
    the lazy evaluation code is triggered. Results are not memoized; the
    function is evaluated on every access.
    """

    @total_ordering
    class __proxy__(Promise):
        __doc__ = '\n        Encapsulate a function call and act as a proxy for methods that are\n        called on the result of that function. The function is not evaluated\n        until one of the methods on the result is called.\n        '
        _proxy____prepared = False

        def __init__(self, args, kw):
            self._proxy____args = args
            self._proxy____kw = kw
            if not self._proxy____prepared:
                self.__prepare_class__()
            self._proxy____prepared = True

        def __reduce__(self):
            return (
             _lazy_proxy_unpickle,
             (
              func, self._proxy____args, self._proxy____kw) + resultclasses)

        def __repr__(self):
            return repr(self._proxy____cast())

        @classmethod
        def __prepare_class__(cls):
            for resultclass in resultclasses:
                for type_ in resultclass.mro():
                    for method_name in type_.__dict__.keys():
                        if hasattr(cls, method_name):
                            pass
                        else:
                            meth = cls.__promise__(method_name)
                            setattr(cls, method_name, meth)

            cls._delegate_bytes = bytes in resultclasses
            cls._delegate_text = str in resultclasses
            assert not (cls._delegate_bytes and cls._delegate_text), 'Cannot call lazy() with both bytes and text return types.'
            if cls._delegate_text:
                cls.__str__ = cls._proxy____text_cast
            elif cls._delegate_bytes:
                cls.__bytes__ = cls._proxy____bytes_cast

        @classmethod
        def __promise__(cls, method_name):

            def __wrapper__(self, *args, **kw):
                res = func(*self._proxy____args, **self._proxy____kw)
                return (getattr(res, method_name))(*args, **kw)

            return __wrapper__

        def __text_cast(self):
            return func(*self._proxy____args, **self._proxy____kw)

        def __bytes_cast(self):
            return bytes(func(*self._proxy____args, **self._proxy____kw))

        def __bytes_cast_encoded(self):
            return func(*self._proxy____args, **self._proxy____kw).encode('utf-8')

        def __cast(self):
            if self._delegate_bytes:
                return self._proxy____bytes_cast()
            else:
                if self._delegate_text:
                    return self._proxy____text_cast()
                return func(*self._proxy____args, **self._proxy____kw)

        def __str__(self):
            return str(self._proxy____cast())

        def __ne__(self, other):
            if isinstance(other, Promise):
                other = other._proxy____cast()
            return self._proxy____cast() != other

        def __eq__(self, other):
            if isinstance(other, Promise):
                other = other._proxy____cast()
            return self._proxy____cast() == other

        def __lt__(self, other):
            if isinstance(other, Promise):
                other = other._proxy____cast()
            return self._proxy____cast() < other

        def __hash__(self):
            return hash(self._proxy____cast())

        def __mod__(self, rhs):
            if self._delegate_text:
                return str(self) % rhs
            else:
                return self._proxy____cast() % rhs

        def __deepcopy__(self, memo):
            memo[id(self)] = self
            return self

    @wraps(func)
    def __wrapper__(*args, **kw):
        return __proxy__(args, kw)

    return __wrapper__


def _lazy_proxy_unpickle(func, args, kwargs, *resultclasses):
    return lazy(func, *resultclasses)(*args, **kwargs)


def lazy_str(text):
    """
    Shortcut for the common case of a lazy callable that returns str.
    """
    from .transcoder import force_text
    return lazy(force_text, str)(text)


def lazy_re_compile(regex, flags=0):
    """
    延迟加载匹配
    :param regex:
    :param flags:
    :return:
    """

    def _compile():
        if isinstance(regex, str):
            return re.compile(regex, flags)
        else:
            assert not flags, 'flags must be empty if regex is passed pre-compiled'
            return regex

    return SimpleLazyObject(_compile)


def lazy_number(func, resultclass, number=None, **kwargs):
    if isinstance(number, int):
        kwargs['number'] = number
        proxy = (lazy(func, resultclass))(**kwargs)
    else:
        original_kwargs = kwargs.copy()

        class NumberAwareString(resultclass):

            def __bool__(self):
                return bool(kwargs['singular'])

            def __nonzero__(self):
                return type(self).__bool__(self)

            def __mod__(self, rhs):
                if isinstance(rhs, dict):
                    if number:
                        try:
                            number_value = rhs[number]
                        except KeyError:
                            raise KeyError("Your dictionary lacks key '%s'. Please provide it, because it is required to determine whether string is singular or plural." % number)

                else:
                    number_value = rhs
                kwargs['number'] = number_value
                translated = func(**kwargs)
                try:
                    translated = translated % rhs
                except TypeError:
                    pass

                return translated

        proxy = (lazy(lambda **kwargs: NumberAwareString(), NumberAwareString))(**kwargs)
        proxy.__reduce__ = lambda : (_lazy_number_unpickle, (func, resultclass, number, original_kwargs))
    return proxy


def _lazy_number_unpickle(func, resultclass, number, kwargs):
    return lazy_number(func, resultclass, number=number, **kwargs)
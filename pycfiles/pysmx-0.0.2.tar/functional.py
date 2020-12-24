# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/utils/functional.py
# Compiled at: 2010-05-30 09:35:01


def curry(_curried_func, *args, **kwargs):

    def _curried(*moreargs, **morekwargs):
        return _curried_func(*(args + moreargs), **dict(kwargs, **morekwargs))

    return _curried


WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
WRAPPER_UPDATES = ('__dict__', )

def update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes off the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        try:
            setattr(wrapper, attr, getattr(wrapped, attr))
        except TypeError:
            pass

    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr))

    return wrapper


def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying curry() to
       update_wrapper().
    """
    return curry(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)


def memoize(func, cache, num_args):
    """
    Wrap a function so that results for any argument tuple are stored in
    'cache'. Note that the args to the function must be usable as dictionary
    keys.

    Only the first num_args are considered when creating the key.
    """

    def wrapper(*args):
        mem_args = args[:num_args]
        if mem_args in cache:
            return cache[mem_args]
        result = func(*args)
        cache[mem_args] = result
        return result

    return wraps(func)(wrapper)


class Promise(object):
    """
    This is just a base class for the proxy class created in
    the closure of the lazy function. It can be used to recognize
    promises in code.
    """


def lazy(func, *resultclasses):
    """
    Turns any callable into a lazy evaluated callable. You need to give result
    classes or types -- at least one is needed so that the automatic forcing of
    the lazy evaluation code is triggered. Results are not memoized; the
    function is evaluated on every access.
    """

    class __proxy__(Promise):
        """
        Encapsulate a function call and act as a proxy for methods that are
        called on the result of that function. The function is not evaluated
        until one of the methods on the result is called.
        """
        __dispatch = None

        def __init__(self, args, kw):
            self.__func = func
            self.__args = args
            self.__kw = kw
            if self.__dispatch is None:
                self.__prepare_class__()
            return

        def __prepare_class__(cls):
            cls.__dispatch = {}
            for resultclass in resultclasses:
                cls.__dispatch[resultclass] = {}
                for (k, v) in resultclass.__dict__.items():
                    if hasattr(cls, k):
                        continue
                    setattr(cls, k, cls.__promise__(resultclass, k, v))

            cls._delegate_str = str in resultclasses
            cls._delegate_unicode = unicode in resultclasses
            assert not (cls._delegate_str and cls._delegate_unicode), 'Cannot call lazy() with both str and unicode return types.'
            if cls._delegate_unicode:
                cls.__unicode__ = cls.__unicode_cast
            elif cls._delegate_str:
                cls.__str__ = cls.__str_cast

        __prepare_class__ = classmethod(__prepare_class__)

        def __promise__(cls, klass, funcname, func):

            def __wrapper__(self, *args, **kw):
                res = self.__func(*self.__args, **self.__kw)
                for t in type(res).mro():
                    if t in self.__dispatch:
                        return self.__dispatch[t][funcname](res, *args, **kw)

                raise TypeError('Lazy object returned unexpected type.')

            if klass not in cls.__dispatch:
                cls.__dispatch[klass] = {}
            cls.__dispatch[klass][funcname] = func
            return __wrapper__

        __promise__ = classmethod(__promise__)

        def __unicode_cast(self):
            return self.__func(*self.__args, **self.__kw)

        def __str_cast(self):
            return str(self.__func(*self.__args, **self.__kw))

        def __cmp__(self, rhs):
            if self._delegate_str:
                s = str(self.__func(*self.__args, **self.__kw))
            elif self._delegate_unicode:
                s = unicode(self.__func(*self.__args, **self.__kw))
            else:
                s = self.__func(*self.__args, **self.__kw)
            if isinstance(rhs, Promise):
                return -cmp(rhs, s)
            else:
                return cmp(s, rhs)

        def __mod__(self, rhs):
            if self._delegate_str:
                return str(self) % rhs
            if self._delegate_unicode:
                return unicode(self) % rhs
            raise AssertionError('__mod__ not supported for non-string types')

        def __deepcopy__(self, memo):
            memo[id(self)] = self
            return self

    def __wrapper__(*args, **kw):
        return __proxy__(args, kw)

    return wraps(func)(__wrapper__)


def allow_lazy(func, *resultclasses):
    """
    A decorator that allows a function to be called with one or more lazy
    arguments. If none of the args are lazy, the function is evaluated
    immediately, otherwise a __proxy__ is returned that will evaluate the
    function when needed.
    """

    def wrapper(*args, **kwargs):
        for arg in list(args) + kwargs.values():
            if isinstance(arg, Promise):
                break
        else:
            return func(*args, **kwargs)

        return lazy(func, *resultclasses)(*args, **kwargs)

    return wraps(func)(wrapper)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/fmriprep/build/lib/python3.7/abc.py
# Compiled at: 2019-09-12 11:41:56
# Size of source mod 2**32: 5580 bytes
"""Abstract Base Classes (ABCs) according to PEP 3119."""

def abstractmethod(funcobj):
    """A decorator indicating abstract methods.

    Requires that the metaclass is ABCMeta or derived from it.  A
    class that has a metaclass derived from ABCMeta cannot be
    instantiated unless all of its abstract methods are overridden.
    The abstract methods can be called using any of the normal
    'super' call mechanisms.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractmethod
            def my_abstract_method(self, ...):
                ...
    """
    funcobj.__isabstractmethod__ = True
    return funcobj


class abstractclassmethod(classmethod):
    __doc__ = "A decorator indicating abstract classmethods.\n\n    Similar to abstractmethod.\n\n    Usage:\n\n        class C(metaclass=ABCMeta):\n            @abstractclassmethod\n            def my_abstract_classmethod(cls, ...):\n                ...\n\n    'abstractclassmethod' is deprecated. Use 'classmethod' with\n    'abstractmethod' instead.\n    "
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super().__init__(callable)


class abstractstaticmethod(staticmethod):
    __doc__ = "A decorator indicating abstract staticmethods.\n\n    Similar to abstractmethod.\n\n    Usage:\n\n        class C(metaclass=ABCMeta):\n            @abstractstaticmethod\n            def my_abstract_staticmethod(...):\n                ...\n\n    'abstractstaticmethod' is deprecated. Use 'staticmethod' with\n    'abstractmethod' instead.\n    "
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super().__init__(callable)


class abstractproperty(property):
    __doc__ = "A decorator indicating abstract properties.\n\n    Requires that the metaclass is ABCMeta or derived from it.  A\n    class that has a metaclass derived from ABCMeta cannot be\n    instantiated unless all of its abstract properties are overridden.\n    The abstract properties can be called using any of the normal\n    'super' call mechanisms.\n\n    Usage:\n\n        class C(metaclass=ABCMeta):\n            @abstractproperty\n            def my_abstract_property(self):\n                ...\n\n    This defines a read-only property; you can also define a read-write\n    abstract property using the 'long' form of property declaration:\n\n        class C(metaclass=ABCMeta):\n            def getx(self): ...\n            def setx(self, value): ...\n            x = abstractproperty(getx, setx)\n\n    'abstractproperty' is deprecated. Use 'property' with 'abstractmethod'\n    instead.\n    "
    __isabstractmethod__ = True


try:
    from _abc import get_cache_token, _abc_init, _abc_register, _abc_instancecheck, _abc_subclasscheck, _get_dump, _reset_registry, _reset_caches
except ImportError:
    from _py_abc import ABCMeta, get_cache_token
    ABCMeta.__module__ = 'abc'
else:

    class ABCMeta(type):
        __doc__ = "Metaclass for defining Abstract Base Classes (ABCs).\n\n        Use this metaclass to create an ABC.  An ABC can be subclassed\n        directly, and then acts as a mix-in class.  You can also register\n        unrelated concrete classes (even built-in classes) and unrelated\n        ABCs as 'virtual subclasses' -- these and their descendants will\n        be considered subclasses of the registering ABC by the built-in\n        issubclass() function, but the registering ABC won't show up in\n        their MRO (Method Resolution Order) nor will method\n        implementations defined by the registering ABC be callable (not\n        even via super()).\n        "

        def __new__(mcls, name, bases, namespace, **kwargs):
            cls = (super().__new__)(mcls, name, bases, namespace, **kwargs)
            _abc_init(cls)
            return cls

        def register(cls, subclass):
            """Register a virtual subclass of an ABC.

            Returns the subclass, to allow usage as a class decorator.
            """
            return _abc_register(cls, subclass)

        def __instancecheck__(cls, instance):
            """Override for isinstance(instance, cls)."""
            return _abc_instancecheck(cls, instance)

        def __subclasscheck__(cls, subclass):
            """Override for issubclass(subclass, cls)."""
            return _abc_subclasscheck(cls, subclass)

        def _dump_registry(cls, file=None):
            """Debug helper to print the ABC registry."""
            print(f"Class: {cls.__module__}.{cls.__qualname__}", file=file)
            print(f"Inv. counter: {get_cache_token()}", file=file)
            _abc_registry, _abc_cache, _abc_negative_cache, _abc_negative_cache_version = _get_dump(cls)
            print(f"_abc_registry: {_abc_registry!r}", file=file)
            print(f"_abc_cache: {_abc_cache!r}", file=file)
            print(f"_abc_negative_cache: {_abc_negative_cache!r}", file=file)
            print(f"_abc_negative_cache_version: {_abc_negative_cache_version!r}", file=file)

        def _abc_registry_clear(cls):
            """Clear the registry (for debugging or testing)."""
            _reset_registry(cls)

        def _abc_caches_clear(cls):
            """Clear the caches (for debugging or testing)."""
            _reset_caches(cls)


class ABC(metaclass=ABCMeta):
    __doc__ = 'Helper class that provides a standard way to create an ABC using\n    inheritance.\n    '
    __slots__ = ()
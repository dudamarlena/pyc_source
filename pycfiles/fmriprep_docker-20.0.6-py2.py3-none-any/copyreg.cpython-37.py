# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/fmriprep/wrapper/build/lib/python3.7/copyreg.py
# Compiled at: 2019-09-12 11:41:56
# Size of source mod 2**32: 7017 bytes
"""Helper to provide extensibility for pickle.

This is only useful to add pickle support for extension types defined in
C, not for instances of user-defined classes.
"""
__all__ = [
 'pickle', 'constructor',
 'add_extension', 'remove_extension', 'clear_extension_cache']
dispatch_table = {}

def pickle(ob_type, pickle_function, constructor_ob=None):
    if not callable(pickle_function):
        raise TypeError('reduction functions must be callable')
    dispatch_table[ob_type] = pickle_function
    if constructor_ob is not None:
        constructor(constructor_ob)


def constructor(object):
    if not callable(object):
        raise TypeError('constructors must be callable')


try:
    complex
except NameError:
    pass
else:

    def pickle_complex(c):
        return (complex, (c.real, c.imag))


    pickle(complex, pickle_complex, complex)

def _reconstructor(cls, base, state):
    if base is object:
        obj = object.__new__(cls)
    else:
        obj = base.__new__(cls, state)
        if base.__init__ != object.__init__:
            base.__init__(obj, state)
    return obj


_HEAPTYPE = 512

def _reduce_ex(self, proto):
    assert proto < 2
    for base in self.__class__.__mro__:
        if hasattr(base, '__flags__') and not base.__flags__ & _HEAPTYPE:
            break
    else:
        base = object

    if base is object:
        state = None
    else:
        if base is self.__class__:
            raise TypeError("can't pickle %s objects" % base.__name__)
        state = base(self)
    args = (
     self.__class__, base, state)
    try:
        getstate = self.__getstate__
    except AttributeError:
        if getattr(self, '__slots__', None):
            raise TypeError('a class that defines __slots__ without defining __getstate__ cannot be pickled') from None
        try:
            dict = self.__dict__
        except AttributeError:
            dict = None

    else:
        dict = getstate()
    if dict:
        return (
         _reconstructor, args, dict)
    return (_reconstructor, args)


def __newobj__(cls, *args):
    return (cls.__new__)(cls, *args)


def __newobj_ex__(cls, args, kwargs):
    """Used by pickle protocol 4, instead of __newobj__ to allow classes with
    keyword-only arguments to be pickled correctly.
    """
    return (cls.__new__)(cls, *args, **kwargs)


def _slotnames(cls):
    """Return a list of slot names for a given class.

    This needs to find slots defined by the class and its bases, so we
    can't simply return the __slots__ attribute.  We must walk down
    the Method Resolution Order and concatenate the __slots__ of each
    class found there.  (This assumes classes don't modify their
    __slots__ attribute to misrepresent their slots after the class is
    defined.)
    """
    names = cls.__dict__.get('__slotnames__')
    if names is not None:
        return names
    else:
        names = []
        if not hasattr(cls, '__slots__'):
            pass
        else:
            for c in cls.__mro__:
                if '__slots__' in c.__dict__:
                    slots = c.__dict__['__slots__']
                    if isinstance(slots, str):
                        slots = (
                         slots,)
                    for name in slots:
                        if name in ('__dict__', '__weakref__'):
                            continue
                        elif name.startswith('__'):
                            if not name.endswith('__'):
                                stripped = c.__name__.lstrip('_')
                                if stripped:
                                    names.append('_%s%s' % (stripped, name))
                            else:
                                names.append(name)
                        else:
                            names.append(name)

    try:
        cls.__slotnames__ = names
    except:
        pass

    return names


_extension_registry = {}
_inverted_registry = {}
_extension_cache = {}

def add_extension(module, name, code):
    """Register an extension code."""
    code = int(code)
    if not 1 <= code <= 2147483647:
        raise ValueError('code out of range')
    key = (
     module, name)
    if _extension_registry.get(key) == code:
        if _inverted_registry.get(code) == key:
            return
    if key in _extension_registry:
        raise ValueError('key %s is already registered with code %s' % (
         key, _extension_registry[key]))
    if code in _inverted_registry:
        raise ValueError('code %s is already in use for key %s' % (
         code, _inverted_registry[code]))
    _extension_registry[key] = code
    _inverted_registry[code] = key


def remove_extension(module, name, code):
    """Unregister an extension code.  For testing only."""
    key = (
     module, name)
    if _extension_registry.get(key) != code or _inverted_registry.get(code) != key:
        raise ValueError('key %s is not registered with code %s' % (
         key, code))
    del _extension_registry[key]
    del _inverted_registry[code]
    if code in _extension_cache:
        del _extension_cache[code]


def clear_extension_cache():
    _extension_cache.clear()
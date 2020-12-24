# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/pyversion.py
# Compiled at: 2014-09-06 21:58:19
"""
This module contains fixups for using nose under different versions of Python.
"""
import sys, os, traceback, types, inspect, nose.util
__all__ = [
 'make_instancemethod', 'cmp_to_key', 'sort_list', 'ClassType',
 'TypeType', 'UNICODE_STRINGS', 'unbound_method', 'ismethod',
 'bytes_', 'is_base_exception', 'force_unicode', 'exc_to_unicode',
 'format_exception']
UNICODE_STRINGS = type(unicode()) == type(str())
if sys.version_info[:2] < (3, 0):

    def force_unicode(s, encoding='UTF-8'):
        try:
            s = unicode(s)
        except UnicodeDecodeError:
            s = str(s).decode(encoding, 'replace')

        return s


else:

    def force_unicode(s, encoding='UTF-8'):
        return str(s)


try:
    import new

    def make_instancemethod(function, instance):
        return new.instancemethod(function.im_func, instance, instance.__class__)


except ImportError:

    def make_instancemethod(function, instance):
        return function.__get__(instance, instance.__class__)


def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""

    class Key(object):

        def __init__(self, obj):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

    return Key


if sys.version_info < (2, 4):

    def sort_list(l, key, reverse=False):
        if reverse:
            return l.sort(lambda a, b: cmp(key(b), key(a)))
        else:
            return l.sort(lambda a, b: cmp(key(a), key(b)))


else:

    def sort_list(l, key, reverse=False):
        return l.sort(key=key, reverse=reverse)


if hasattr(types, 'ClassType'):
    ClassType = types.ClassType
    TypeType = types.TypeType
else:
    ClassType = type
    TypeType = type

class UnboundMethod:

    def __init__(self, cls, func):
        self.__dict__ = func.__dict__.copy()
        self._func = func
        self.__self__ = UnboundSelf(cls)
        if sys.version_info < (3, 0):
            self.im_class = cls

    def address(self):
        cls = self.__self__.cls
        modname = cls.__module__
        module = sys.modules[modname]
        filename = getattr(module, '__file__', None)
        if filename is not None:
            filename = os.path.abspath(filename)
        return (
         nose.util.src(filename), modname,
         '%s.%s' % (cls.__name__,
          self._func.__name__))

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self._func, attr)

    def __repr__(self):
        return '<unbound method %s.%s>' % (self.__self__.cls.__name__,
         self._func.__name__)


class UnboundSelf:

    def __init__(self, cls):
        self.cls = cls

    def __getattribute__(self, attr):
        if attr == '__class__':
            return self.cls
        else:
            return object.__getattribute__(self, attr)


def unbound_method(cls, func):
    if inspect.ismethod(func):
        return func
    if not inspect.isfunction(func):
        raise TypeError('%s is not a function' % (repr(func),))
    return UnboundMethod(cls, func)


def ismethod(obj):
    return inspect.ismethod(obj) or isinstance(obj, UnboundMethod)


if sys.version_info >= (3, 0):

    def bytes_(s, encoding='utf8'):
        if isinstance(s, bytes):
            return s
        return bytes(s, encoding)


else:

    def bytes_(s, encoding=None):
        return str(s)


if sys.version_info[:2] >= (2, 6):

    def isgenerator(o):
        if isinstance(o, UnboundMethod):
            o = o._func
        return inspect.isgeneratorfunction(o) or inspect.isgenerator(o)


else:
    try:
        from compiler.consts import CO_GENERATOR
    except ImportError:
        CO_GENERATOR = 32

    def isgenerator(func):
        try:
            return func.func_code.co_flags & CO_GENERATOR != 0
        except AttributeError:
            return False


if sys.version_info[:2] < (2, 5):

    def is_base_exception(exc):
        return isinstance(exc, Exception)


else:

    def is_base_exception(exc):
        return isinstance(exc, BaseException)


if sys.version_info[:2] < (3, 0):

    def exc_to_unicode(ev, encoding='utf-8'):
        if is_base_exception(ev):
            if not hasattr(ev, '__unicode__'):
                if not hasattr(ev, 'message'):
                    msg = len(ev.args) and ev.args[0] or ''
                else:
                    msg = ev.message
                msg = force_unicode(msg, encoding=encoding)
                clsname = force_unicode(ev.__class__.__name__, encoding=encoding)
                ev = '%s: %s' % (clsname, msg)
        elif not isinstance(ev, unicode):
            ev = repr(ev)
        return force_unicode(ev, encoding=encoding)


else:

    def exc_to_unicode(ev, encoding='utf-8'):
        return str(ev)


def format_exception(exc_info, encoding='UTF-8'):
    ec, ev, tb = exc_info
    if not is_base_exception(ev):
        tb_data = force_unicode(('').join(traceback.format_tb(tb)), encoding)
        ev = exc_to_unicode(ev)
        return tb_data + ev
    else:
        return force_unicode(('').join(traceback.format_exception(*exc_info)), encoding)
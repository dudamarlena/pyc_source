# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\hls501\documents\programming\api\pycgm2\pycgm2\pyCGM2\ma\io.py
# Compiled at: 2018-12-10 10:10:46
from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 6, 0):

    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_io', [dirname(__file__)])
        except ImportError:
            import _io
            return _io

        if fp is not None:
            try:
                _mod = imp.load_module('_io', fp, pathname, description)
            finally:
                fp.close()

            return _mod
        else:
            return


    _io = swig_import_helper()
    del swig_import_helper
else:
    import _io
del _swig_python_version_info
try:
    _swig_property = property
except NameError:
    pass

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == 'thisown':
        return self.this.own(value)
    else:
        if name == 'this':
            if type(value).__name__ == 'SwigPyObject':
                self.__dict__[name] = value
                return
        method = class_type.__swig_setmethods__.get(name, None)
        if method:
            return method(self, value)
        if not static:
            if _newclass:
                object.__setattr__(self, name, value)
            else:
                self.__dict__[name] = value
        else:
            raise AttributeError('You cannot add attributes to %s' % self)
        return


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == 'thisown':
        return self.this.own()
    else:
        method = class_type.__swig_getmethods__.get(name, None)
        if method:
            return method(self)
        raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))
        return


def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ''

    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


try:
    _object = object
    _newclass = 1
except __builtin__.Exception:

    class _object:
        pass


    _newclass = 0

from pyCGM2 import ma

def read(*args):
    return _io.read(*args)


read = _io.read

def write(*args):
    return _io.write(*args)


write = _io.write
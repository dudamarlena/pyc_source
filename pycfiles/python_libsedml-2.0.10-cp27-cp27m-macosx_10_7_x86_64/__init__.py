# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: libsedml/__init__.py
# Compiled at: 2020-04-30 04:13:06
import sys, os.path, inspect
try:
    _filename = inspect.getframeinfo(inspect.currentframe()).filename
except:
    _filename = __file__

_path = os.path.dirname(os.path.abspath(_filename))
if not _path in sys.path:
    sys.path.append(_path)
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _libsedml
else:
    import _libsedml
try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ''

    return '<%s.%s %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


def _swig_setattr_nondynamic_instance_variable(set):

    def set_instance_attr(self, name, value):
        if name == 'thisown':
            self.this.own(value)
        elif name == 'this':
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError('You cannot add instance attributes to %s' % self)

    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):

    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError('You cannot add class attributes to %s' % cls)

    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""

    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())

    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import weakref
SEDML_MAPPINGTYPE_TIME = _libsedml.SEDML_MAPPINGTYPE_TIME
SEDML_MAPPINGTYPE_EXPERIMENTALCONDITION = _libsedml.SEDML_MAPPINGTYPE_EXPERIMENTALCONDITION
SEDML_MAPPINGTYPE_OBSERVABLE = _libsedml.SEDML_MAPPINGTYPE_OBSERVABLE
SEDML_MAPPINGTYPE_INVALID = _libsedml.SEDML_MAPPINGTYPE_INVALID

def MappingType_toString(mt):
    return _libsedml.MappingType_toString(mt)


def MappingType_fromString(code):
    return _libsedml.MappingType_fromString(code)


def MappingType_isValid(mt):
    return _libsedml.MappingType_isValid(mt)


def MappingType_isValidString(code):
    return _libsedml.MappingType_isValidString(code)


SEDML_AXISTYPE_LINEAR = _libsedml.SEDML_AXISTYPE_LINEAR
SEDML_AXISTYPE_LOG10 = _libsedml.SEDML_AXISTYPE_LOG10
SEDML_AXISTYPE_INVALID = _libsedml.SEDML_AXISTYPE_INVALID

def AxisType_toString(at):
    return _libsedml.AxisType_toString(at)


def AxisType_fromString(code):
    return _libsedml.AxisType_fromString(code)


def AxisType_isValid(at):
    return _libsedml.AxisType_isValid(at)


def AxisType_isValidString(code):
    return _libsedml.AxisType_isValidString(code)


SEDML_LINETYPE_NONE = _libsedml.SEDML_LINETYPE_NONE
SEDML_LINETYPE_SOLID = _libsedml.SEDML_LINETYPE_SOLID
SEDML_LINETYPE_DASH = _libsedml.SEDML_LINETYPE_DASH
SEDML_LINETYPE_DOT = _libsedml.SEDML_LINETYPE_DOT
SEDML_LINETYPE_DASHDOT = _libsedml.SEDML_LINETYPE_DASHDOT
SEDML_LINETYPE_DASHDOTDOT = _libsedml.SEDML_LINETYPE_DASHDOTDOT
SEDML_LINETYPE_INVALID = _libsedml.SEDML_LINETYPE_INVALID

def LineType_toString(lt):
    return _libsedml.LineType_toString(lt)


def LineType_fromString(code):
    return _libsedml.LineType_fromString(code)


def LineType_isValid(lt):
    return _libsedml.LineType_isValid(lt)


def LineType_isValidString(code):
    return _libsedml.LineType_isValidString(code)


SEDML_MARKERTYPE_NONE = _libsedml.SEDML_MARKERTYPE_NONE
SEDML_MARKERTYPE_SQUARE = _libsedml.SEDML_MARKERTYPE_SQUARE
SEDML_MARKERTYPE_CIRCLE = _libsedml.SEDML_MARKERTYPE_CIRCLE
SEDML_MARKERTYPE_DIAMOND = _libsedml.SEDML_MARKERTYPE_DIAMOND
SEDML_MARKERTYPE_XCROSS = _libsedml.SEDML_MARKERTYPE_XCROSS
SEDML_MARKERTYPE_PLUS = _libsedml.SEDML_MARKERTYPE_PLUS
SEDML_MARKERTYPE_STAR = _libsedml.SEDML_MARKERTYPE_STAR
SEDML_MARKERTYPE_TRIANGLEUP = _libsedml.SEDML_MARKERTYPE_TRIANGLEUP
SEDML_MARKERTYPE_TRIANGLEDOWN = _libsedml.SEDML_MARKERTYPE_TRIANGLEDOWN
SEDML_MARKERTYPE_TRIANGLELEFT = _libsedml.SEDML_MARKERTYPE_TRIANGLELEFT
SEDML_MARKERTYPE_TRIANGLERIGHT = _libsedml.SEDML_MARKERTYPE_TRIANGLERIGHT
SEDML_MARKERTYPE_HDASH = _libsedml.SEDML_MARKERTYPE_HDASH
SEDML_MARKERTYPE_VDASH = _libsedml.SEDML_MARKERTYPE_VDASH
SEDML_MARKERTYPE_INVALID = _libsedml.SEDML_MARKERTYPE_INVALID

def MarkerType_toString(mt):
    return _libsedml.MarkerType_toString(mt)


def MarkerType_fromString(code):
    return _libsedml.MarkerType_fromString(code)


def MarkerType_isValid(mt):
    return _libsedml.MarkerType_isValid(mt)


def MarkerType_isValidString(code):
    return _libsedml.MarkerType_isValidString(code)


SEDML_CURVETYPE_POINTS = _libsedml.SEDML_CURVETYPE_POINTS
SEDML_CURVETYPE_BAR = _libsedml.SEDML_CURVETYPE_BAR
SEDML_CURVETYPE_BARSTACKED = _libsedml.SEDML_CURVETYPE_BARSTACKED
SEDML_CURVETYPE_HORIZONTALBAR = _libsedml.SEDML_CURVETYPE_HORIZONTALBAR
SEDML_CURVETYPE_HORIZONTALBARSTACKED = _libsedml.SEDML_CURVETYPE_HORIZONTALBARSTACKED
SEDML_CURVETYPE_INVALID = _libsedml.SEDML_CURVETYPE_INVALID

def CurveType_toString(ct):
    return _libsedml.CurveType_toString(ct)


def CurveType_fromString(code):
    return _libsedml.CurveType_fromString(code)


def CurveType_isValid(ct):
    return _libsedml.CurveType_isValid(ct)


def CurveType_isValidString(code):
    return _libsedml.CurveType_isValidString(code)


SEDML_SURFACETYPE_PARAMETRICCURVE = _libsedml.SEDML_SURFACETYPE_PARAMETRICCURVE
SEDML_SURFACETYPE_SURFACEMESH = _libsedml.SEDML_SURFACETYPE_SURFACEMESH
SEDML_SURFACETYPE_SURFACECONTOUR = _libsedml.SEDML_SURFACETYPE_SURFACECONTOUR
SEDML_SURFACETYPE_CONTOUR = _libsedml.SEDML_SURFACETYPE_CONTOUR
SEDML_SURFACETYPE_HEATMAP = _libsedml.SEDML_SURFACETYPE_HEATMAP
SEDML_SURFACETYPE_STACKEDCURVES = _libsedml.SEDML_SURFACETYPE_STACKEDCURVES
SEDML_SURFACETYPE_BAR = _libsedml.SEDML_SURFACETYPE_BAR
SEDML_SURFACETYPE_INVALID = _libsedml.SEDML_SURFACETYPE_INVALID

def SurfaceType_toString(st):
    return _libsedml.SurfaceType_toString(st)


def SurfaceType_fromString(code):
    return _libsedml.SurfaceType_fromString(code)


def SurfaceType_isValid(st):
    return _libsedml.SurfaceType_isValid(st)


def SurfaceType_isValidString(code):
    return _libsedml.SurfaceType_isValidString(code)


SEDML_EXPERIMENTTYPE_STEADYSTATE = _libsedml.SEDML_EXPERIMENTTYPE_STEADYSTATE
SEDML_EXPERIMENTTYPE_TIMECOURSE = _libsedml.SEDML_EXPERIMENTTYPE_TIMECOURSE
SEDML_EXPERIMENTTYPE_INVALID = _libsedml.SEDML_EXPERIMENTTYPE_INVALID

def ExperimentType_toString(et):
    return _libsedml.ExperimentType_toString(et)


def ExperimentType_fromString(code):
    return _libsedml.ExperimentType_fromString(code)


def ExperimentType_isValid(et):
    return _libsedml.ExperimentType_isValid(et)


def ExperimentType_isValidString(code):
    return _libsedml.ExperimentType_isValidString(code)


SEDML_SCALETYPE_LIN = _libsedml.SEDML_SCALETYPE_LIN
SEDML_SCALETYPE_LOG = _libsedml.SEDML_SCALETYPE_LOG
SEDML_SCALETYPE_LOG10 = _libsedml.SEDML_SCALETYPE_LOG10
SEDML_SCALETYPE_INVALID = _libsedml.SEDML_SCALETYPE_INVALID

def ScaleType_toString(st):
    return _libsedml.ScaleType_toString(st)


def ScaleType_fromString(code):
    return _libsedml.ScaleType_fromString(code)


def ScaleType_isValid(st):
    return _libsedml.ScaleType_isValid(st)


def ScaleType_isValidString(code):
    return _libsedml.ScaleType_isValidString(code)


class ASTNodeList(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _libsedml.ASTNodeList_swiginit(self, _libsedml.new_ASTNodeList())

    __swig_destroy__ = _libsedml.delete_ASTNodeList

    def add(self, item):
        return _libsedml.ASTNodeList_add(self, item)

    def get(self, n):
        return _libsedml.ASTNodeList_get(self, n)

    def prepend(self, item):
        return _libsedml.ASTNodeList_prepend(self, item)

    def remove(self, n):
        return _libsedml.ASTNodeList_remove(self, n)

    def getSize(self):
        return _libsedml.ASTNodeList_getSize(self)


_libsedml.ASTNodeList_swigregister(ASTNodeList)

class SedNamespacesList(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _libsedml.SedNamespacesList_swiginit(self, _libsedml.new_SedNamespacesList())

    __swig_destroy__ = _libsedml.delete_SedNamespacesList

    def add(self, item):
        return _libsedml.SedNamespacesList_add(self, item)

    def get(self, n):
        return _libsedml.SedNamespacesList_get(self, n)

    def prepend(self, item):
        return _libsedml.SedNamespacesList_prepend(self, item)

    def remove(self, n):
        return _libsedml.SedNamespacesList_remove(self, n)

    def getSize(self):
        return _libsedml.SedNamespacesList_getSize(self)


_libsedml.SedNamespacesList_swigregister(SedNamespacesList)

class SedBaseList(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _libsedml.SedBaseList_swiginit(self, _libsedml.new_SedBaseList())

    __swig_destroy__ = _libsedml.delete_SedBaseList

    def add(self, item):
        return _libsedml.SedBaseList_add(self, item)

    def get(self, n):
        return _libsedml.SedBaseList_get(self, n)

    def prepend(self, item):
        return _libsedml.SedBaseList_prepend(self, item)

    def remove(self, n):
        return _libsedml.SedBaseList_remove(self, n)

    def getSize(self):
        return _libsedml.SedBaseList_getSize(self)


_libsedml.SedBaseList_swigregister(SedBaseList)

class SBaseList(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _libsedml.SBaseList_swiginit(self, _libsedml.new_SBaseList())

    __swig_destroy__ = _libsedml.delete_SBaseList

    def add(self, item):
        return _libsedml.SBaseList_add(self, item)

    def get(self, n):
        return _libsedml.SBaseList_get(self, n)

    def prepend(self, item):
        return _libsedml.SBaseList_prepend(self, item)

    def remove(self, n):
        return _libsedml.SBaseList_remove(self, n)

    def getSize(self):
        return _libsedml.SBaseList_getSize(self)


_libsedml.SBaseList_swigregister(SBaseList)

class AutoProperty(type):
    """
    A metaclass for automatically detecting getX/setX methods at class creation
    time (not instantiation), and adding properties (directly calling C methods
    where possible) to the class dictionary.
    """

    def __new__(cls, classname, bases, classdict):
        """
        Iterate over the items in the classdict looking for get/set pairs
        and declaring them as properties.
        """
        import re, keyword, sys
        if sys.version_info < (3, 0):
            from inspect import getargspec as mygetargspec
        else:
            from inspect import getfullargspec as mygetargspec
        re_mangle = re.compile('[A-Za-z][a-z]+|[A-Z]+(?=$|[A-Z0-9])|\\d+')
        re_id = re.compile('^[A-Za-z_][A-Za-z0-9_]*$')
        re_getdoc = re.compile('^\\s*[A-Za-z_][A-Za-z0-9_]*\\(self\\)')
        re_setdoc = re.compile('^\\s*[A-Za-z_][A-Za-z0-9_]*\\(self,[^,)]+\\)')
        mangle_name = lambda x: ('_').join(re_mangle.findall(x)).lower()
        get_methods = set()
        set_methods = set()
        swig_setter = classdict.get('__swig_setmethods__', {})
        for k, v in classdict.items():
            name = k[3:]
            prefix = k[:3]
            mangled = mangle_name(name)
            if name:
                if callable(v):
                    if re_id.match(mangled) and mangled not in keyword.kwlist:
                        if prefix == 'get':
                            get_methods.add(name)
                        elif prefix == 'set':
                            set_methods.add(name)

        for name in get_methods | set_methods:
            mangled = mangle_name(name)
            if mangled.startswith('list_of_'):
                mangled = mangled[8:]
            getter = setter = deleter = None
            if name in get_methods:
                getter = classdict[('get' + name)]
                try:
                    argspec = mygetargspec(getter)
                    numargs = len(argspec.args)
                    if numargs > 1 or numargs == 1 and argspec.args[0] != 'self' or argspec.varargs != None and name not in allowed_methods and not name.startswith('ListOf'):
                        continue
                except Exception:
                    continue

                cname = classname + '_get' + name
                try:
                    if getter.func_code.co_names == ('_libsedml', cname):
                        getter = getattr(_libsedml, cname)
                except:
                    if getter.__code__.co_names == ('_libsedml', cname):
                        getter = getattr(_libsedml, cname)

            if name in set_methods:
                setter = classdict[('set' + name)]
                try:
                    argspec = mygetargspec(getter)
                    numargs = len(argspec.args)
                    if numargs > 1 and argspec.args[0] == 'self':
                        cname = classname + '_set' + name
                        try:
                            if setter.func_code.co_names == ('_libsedml', cname):
                                setter = getattr(_libsedml, cname)
                        except:
                            if setter.__code__.co_names == ('_libsedml', cname):
                                setter = getattr(_libsedml, cname)

                        swig_setter[mangled] = setter
                        continue
                except:
                    pass

            if 'unset' + name in classdict:
                deleter = classdict[('unset' + name)]
                try:
                    argspec = mygetargspec(getter)
                    numargs = len(argspec.args)
                    if numargs == 1 and argspec.args[0] == 'self' and (argspec.varargs == None or name in allowed_methods):
                        cname = classname + '_unset' + name
                        try:
                            if deleter.func_code.co_names == ('_libsedml', cname):
                                deleter = getattr(_libsedml, cname)
                        except:
                            if deleter.__code__.co_names == ('_libsedml', cname):
                                deleter = getattr(_libsedml, cname)

                except:
                    pass

            if getter or setter or deleter:
                classdict[mangled] = property(fget=getter, fset=setter, fdel=deleter)

            def __repr__(self):
                desc = self.__class__.__name__
                if hasattr(self, '__len__'):
                    desc += '[%s]' % self.__len__()
                if hasattr(self, 'id') and self.id:
                    desc += ' %s' % self.id
                if hasattr(self, 'name') and self.name:
                    desc += ' "%s"' % self.name
                return '<' + desc + '>'

            if classdict.get('__repr__', None) in (_swig_repr, None):
                classdict['__repr__'] = __repr__

        return type.__new__(cls, classname, bases, classdict)


class SwigPyIterator(object):
    """Proxy of C++ swig::SwigPyIterator class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined - class is abstract')

    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_SwigPyIterator

    def value(self):
        """value(SwigPyIterator self) -> PyObject *"""
        return _libsedml.SwigPyIterator_value(self)

    def incr(self, n=1):
        """incr(SwigPyIterator self, size_t n=1) -> SwigPyIterator"""
        return _libsedml.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        """decr(SwigPyIterator self, size_t n=1) -> SwigPyIterator"""
        return _libsedml.SwigPyIterator_decr(self, n)

    def distance(self, x):
        """distance(SwigPyIterator self, SwigPyIterator x) -> ptrdiff_t"""
        return _libsedml.SwigPyIterator_distance(self, x)

    def equal(self, x):
        """equal(SwigPyIterator self, SwigPyIterator x) -> bool"""
        return _libsedml.SwigPyIterator_equal(self, x)

    def copy(self):
        """copy(SwigPyIterator self) -> SwigPyIterator"""
        return _libsedml.SwigPyIterator_copy(self)

    def next(self):
        """next(SwigPyIterator self) -> PyObject *"""
        return _libsedml.SwigPyIterator_next(self)

    def __next__(self):
        """__next__(SwigPyIterator self) -> PyObject *"""
        return _libsedml.SwigPyIterator___next__(self)

    def previous(self):
        """previous(SwigPyIterator self) -> PyObject *"""
        return _libsedml.SwigPyIterator_previous(self)

    def advance(self, n):
        """advance(SwigPyIterator self, ptrdiff_t n) -> SwigPyIterator"""
        return _libsedml.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        """__eq__(SwigPyIterator self, SwigPyIterator x) -> bool"""
        return _libsedml.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        """__ne__(SwigPyIterator self, SwigPyIterator x) -> bool"""
        return _libsedml.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        """__iadd__(SwigPyIterator self, ptrdiff_t n) -> SwigPyIterator"""
        return _libsedml.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        """__isub__(SwigPyIterator self, ptrdiff_t n) -> SwigPyIterator"""
        return _libsedml.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        """__add__(SwigPyIterator self, ptrdiff_t n) -> SwigPyIterator"""
        return _libsedml.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        """
        __sub__(SwigPyIterator self, ptrdiff_t n) -> SwigPyIterator
        __sub__(SwigPyIterator self, SwigPyIterator x) -> ptrdiff_t
        """
        return _libsedml.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_libsedml.SwigPyIterator_swigregister(SwigPyIterator)

class string(object):
    """Proxy of C++ std::basic_string< char > class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def length(self):
        """length(string self) -> std::basic_string< char >::size_type"""
        return _libsedml.string_length(self)

    def max_size(self):
        """max_size(string self) -> std::basic_string< char >::size_type"""
        return _libsedml.string_max_size(self)

    def copy(self, _string__s, _string__n, _string__pos=0):
        """copy(string self, char * __s, std::basic_string< char >::size_type __n, std::basic_string< char >::size_type __pos=0) -> std::basic_string< char >::size_type"""
        return _libsedml.string_copy(self, __s, __n, __pos)

    def c_str(self):
        """c_str(string self) -> char const *"""
        return _libsedml.string_c_str(self)

    def find(self, *args):
        """
        find(string self, char const * __s, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n) -> std::basic_string< char >::size_type
        find(string self, string __str, std::basic_string< char >::size_type __pos=0) -> std::basic_string< char >::size_type
        find(string self, char __c, std::basic_string< char >::size_type __pos=0) -> std::basic_string< char >::size_type
        """
        return _libsedml.string_find(self, *args)

    def rfind(self, *args):
        """
        rfind(string self, string __str, std::basic_string< char >::size_type __pos=std::basic_string< char >::npos) -> std::basic_string< char >::size_type
        rfind(string self, char const * __s, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n) -> std::basic_string< char >::size_type
        rfind(string self, char __c, std::basic_string< char >::size_type __pos=std::basic_string< char >::npos) -> std::basic_string< char >::size_type
        """
        return _libsedml.string_rfind(self, *args)

    def find_first_of(self, *args):
        """
        find_first_of(string self, string __str, std::basic_string< char >::size_type __pos=0) -> std::basic_string< char >::size_type
        find_first_of(string self, char const * __s, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n) -> std::basic_string< char >::size_type
        find_first_of(string self, char __c, std::basic_string< char >::size_type __pos=0) -> std::basic_string< char >::size_type
        """
        return _libsedml.string_find_first_of(self, *args)

    def find_last_of(self, *args):
        """
        find_last_of(string self, string __str, std::basic_string< char >::size_type __pos=std::basic_string< char >::npos) -> std::basic_string< char >::size_type
        find_last_of(string self, char const * __s, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n) -> std::basic_string< char >::size_type
        find_last_of(string self, char __c, std::basic_string< char >::size_type __pos=std::basic_string< char >::npos) -> std::basic_string< char >::size_type
        """
        return _libsedml.string_find_last_of(self, *args)

    def find_first_not_of(self, *args):
        """
        find_first_not_of(string self, string __str, std::basic_string< char >::size_type __pos=0) -> std::basic_string< char >::size_type
        find_first_not_of(string self, char const * __s, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n) -> std::basic_string< char >::size_type
        find_first_not_of(string self, char __c, std::basic_string< char >::size_type __pos=0) -> std::basic_string< char >::size_type
        """
        return _libsedml.string_find_first_not_of(self, *args)

    def find_last_not_of(self, *args):
        """
        find_last_not_of(string self, string __str, std::basic_string< char >::size_type __pos=std::basic_string< char >::npos) -> std::basic_string< char >::size_type
        find_last_not_of(string self, char const * __s, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n) -> std::basic_string< char >::size_type
        find_last_not_of(string self, char __c, std::basic_string< char >::size_type __pos=std::basic_string< char >::npos) -> std::basic_string< char >::size_type
        """
        return _libsedml.string_find_last_not_of(self, *args)

    def substr(self, *args):
        """substr(string self, std::basic_string< char >::size_type __pos=0, std::basic_string< char >::size_type __n=std::basic_string< char >::npos) -> string"""
        return _libsedml.string_substr(self, *args)

    def empty(self):
        """empty(string self) -> bool"""
        return _libsedml.string_empty(self)

    def size(self):
        """size(string self) -> std::basic_string< char >::size_type"""
        return _libsedml.string_size(self)

    def swap(self, v):
        """swap(string self, string v)"""
        return _libsedml.string_swap(self, v)

    def erase(self, *args):
        """
        erase(string self, std::basic_string< char >::size_type __pos=0, std::basic_string< char >::size_type __n=std::basic_string< char >::npos) -> string
        erase(string self, std::basic_string< char >::iterator pos) -> std::basic_string< char >::iterator
        erase(string self, std::basic_string< char >::iterator first, std::basic_string< char >::iterator last) -> std::basic_string< char >::iterator
        """
        return _libsedml.string_erase(self, *args)

    def __init__(self, *args):
        """
        __init__(string self, char const * __s, std::basic_string< char >::size_type __n) -> string
        __init__(string self) -> string
        __init__(string self, string other) -> string
        __init__(string self, std::basic_string< char >::size_type size, std::basic_string< char >::value_type value) -> string
        """
        _libsedml.string_swiginit(self, _libsedml.new_string(*args))

    def assign(self, *args):
        """
        assign(string self, string __str) -> string
        assign(string self, string __str, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n) -> string
        assign(string self, char const * __s, std::basic_string< char >::size_type __n) -> string
        assign(string self, std::basic_string< char >::size_type n, std::basic_string< char >::value_type x)
        """
        return _libsedml.string_assign(self, *args)

    def resize(self, *args):
        """
        resize(string self, std::basic_string< char >::size_type new_size)
        resize(string self, std::basic_string< char >::size_type new_size, std::basic_string< char >::value_type x)
        """
        return _libsedml.string_resize(self, *args)

    def iterator(self):
        """iterator(string self) -> SwigPyIterator"""
        return _libsedml.string_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        """__nonzero__(string self) -> bool"""
        return _libsedml.string___nonzero__(self)

    def __bool__(self):
        """__bool__(string self) -> bool"""
        return _libsedml.string___bool__(self)

    def __len__(self):
        """__len__(string self) -> std::basic_string< char >::size_type"""
        return _libsedml.string___len__(self)

    def __getslice__(self, i, j):
        """__getslice__(string self, std::basic_string< char >::difference_type i, std::basic_string< char >::difference_type j) -> string"""
        return _libsedml.string___getslice__(self, i, j)

    def __setslice__(self, *args):
        """
        __setslice__(string self, std::basic_string< char >::difference_type i, std::basic_string< char >::difference_type j)
        __setslice__(string self, std::basic_string< char >::difference_type i, std::basic_string< char >::difference_type j, string v)
        """
        return _libsedml.string___setslice__(self, *args)

    def __delslice__(self, i, j):
        """__delslice__(string self, std::basic_string< char >::difference_type i, std::basic_string< char >::difference_type j)"""
        return _libsedml.string___delslice__(self, i, j)

    def __delitem__(self, *args):
        """
        __delitem__(string self, std::basic_string< char >::difference_type i)
        __delitem__(string self, PySliceObject * slice)
        """
        return _libsedml.string___delitem__(self, *args)

    def __getitem__(self, *args):
        """
        __getitem__(string self, PySliceObject * slice) -> string
        __getitem__(string self, std::basic_string< char >::difference_type i) -> std::basic_string< char >::value_type
        """
        return _libsedml.string___getitem__(self, *args)

    def __setitem__(self, *args):
        """
        __setitem__(string self, PySliceObject * slice, string v)
        __setitem__(string self, PySliceObject * slice)
        __setitem__(string self, std::basic_string< char >::difference_type i, std::basic_string< char >::value_type x)
        """
        return _libsedml.string___setitem__(self, *args)

    def insert(self, *args):
        """
        insert(string self, std::basic_string< char >::size_type __pos1, string __str) -> string
        insert(string self, std::basic_string< char >::size_type __pos1, string __str, std::basic_string< char >::size_type __pos2, std::basic_string< char >::size_type __n) -> string
        insert(string self, std::basic_string< char >::size_type __pos, char const * __s, std::basic_string< char >::size_type __n) -> string
        insert(string self, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n, char __c) -> string
        insert(string self, std::basic_string< char >::iterator pos, std::basic_string< char >::value_type x) -> std::basic_string< char >::iterator
        insert(string self, std::basic_string< char >::iterator pos, std::basic_string< char >::size_type n, std::basic_string< char >::value_type x)
        insert(string self, std::basic_string< char >::iterator __p, std::basic_string< char >::size_type __n, char __c)
        """
        return _libsedml.string_insert(self, *args)

    def replace(self, *args):
        """
        replace(string self, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n, string __str) -> string
        replace(string self, std::basic_string< char >::size_type __pos1, std::basic_string< char >::size_type __n1, string __str, std::basic_string< char >::size_type __pos2, std::basic_string< char >::size_type __n2) -> string
        replace(string self, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n1, char const * __s, std::basic_string< char >::size_type __n2) -> string
        replace(string self, std::basic_string< char >::size_type __pos, std::basic_string< char >::size_type __n1, std::basic_string< char >::size_type __n2, char __c) -> string
        replace(string self, std::basic_string< char >::iterator __i1, std::basic_string< char >::iterator __i2, string __str) -> string
        replace(string self, std::basic_string< char >::iterator __i1, std::basic_string< char >::iterator __i2, char const * __s, std::basic_string< char >::size_type __n) -> string
        replace(string self, std::basic_string< char >::iterator __i1, std::basic_string< char >::iterator __i2, std::basic_string< char >::size_type __n, char __c) -> string
        replace(string self, std::basic_string< char >::iterator __i1, std::basic_string< char >::iterator __i2, char const * __k1, char const * __k2) -> string
        replace(string self, std::basic_string< char >::iterator __i1, std::basic_string< char >::iterator __i2, std::basic_string< char >::const_iterator __k1, std::basic_string< char >::const_iterator __k2) -> string
        """
        return _libsedml.string_replace(self, *args)

    def __iadd__(self, v):
        """__iadd__(string self, string v) -> string"""
        return _libsedml.string___iadd__(self, v)

    def __add__(self, v):
        """__add__(string self, string v) -> string"""
        return _libsedml.string___add__(self, v)

    def __radd__(self, v):
        """__radd__(string self, string v) -> string"""
        return _libsedml.string___radd__(self, v)

    def __str__(self):
        """__str__(string self) -> string"""
        return _libsedml.string___str__(self)

    def __rlshift__(self, out):
        """__rlshift__(string self, ostream out) -> ostream"""
        return _libsedml.string___rlshift__(self, out)

    def __eq__(self, v):
        """__eq__(string self, string v) -> bool"""
        return _libsedml.string___eq__(self, v)

    def __ne__(self, v):
        """__ne__(string self, string v) -> bool"""
        return _libsedml.string___ne__(self, v)

    def __gt__(self, v):
        """__gt__(string self, string v) -> bool"""
        return _libsedml.string___gt__(self, v)

    def __lt__(self, v):
        """__lt__(string self, string v) -> bool"""
        return _libsedml.string___lt__(self, v)

    def __ge__(self, v):
        """__ge__(string self, string v) -> bool"""
        return _libsedml.string___ge__(self, v)

    def __le__(self, v):
        """__le__(string self, string v) -> bool"""
        return _libsedml.string___le__(self, v)

    __swig_destroy__ = _libsedml.delete_string


_libsedml.string_swigregister(string)
cvar = _libsedml.cvar
string.npos = _libsedml.cvar.string_npos

class ostream(object):
    """Proxy of C++ std::basic_ostream< char > class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, _ostream__sb):
        """__init__(ostream self, std::basic_streambuf< char,std::char_traits< char > > * __sb) -> ostream"""
        _libsedml.ostream_swiginit(self, _libsedml.new_ostream(__sb))

    __swig_destroy__ = _libsedml.delete_ostream


_libsedml.ostream_swigregister(ostream)

class ostringstream(ostream):
    """Proxy of C++ std::basic_ostringstream< char > class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """__init__(ostringstream self, std::ios_base::openmode __mode=std::ios_base::out) -> ostringstream"""
        _libsedml.ostringstream_swiginit(self, _libsedml.new_ostringstream(*args))

    __swig_destroy__ = _libsedml.delete_ostringstream

    def str(self, *args):
        """
        str(ostringstream self) -> string
        str(ostringstream self, string __s)
        """
        return _libsedml.ostringstream_str(self, *args)


_libsedml.ostringstream_swigregister(ostringstream)

def endl(arg1):
    """endl(ostream arg1) -> ostream"""
    return _libsedml.endl(arg1)


def flush(arg1):
    """flush(ostream arg1) -> ostream"""
    return _libsedml.flush(arg1)


import sys, os.path

def conditional_abspath(filename):
    """conditional_abspath (filename) -> filename

  Returns filename with an absolute path prepended, if necessary.
  Some combinations of platforms and underlying XML parsers *require*
  an absolute path to a filename while others do not.  This function
  encapsulates the appropriate logic.  It is used by readSedML() and
  SedReader.readSedML().
  """
    if sys.platform.find('cygwin') != -1:
        return filename
    else:
        return os.path.abspath(filename)


def readSedML(*args):
    """
  readSedML(self, string filename) -> SedDocument

  Reads an Sed document from a file.

  This method is identical to readSedMLFromFile().

  If the file named 'filename' does not exist or its content is not
  valid Sed, one or more errors will be logged with the SedDocument
  object returned by this method.  Callers can use the methods on
  SedDocument such as SedDocument.getNumErrors() and
  SedDocument.getError() to get the errors.  The object returned by
  SedDocument.getError() is an SedError object, and it has methods to
  get the error code, category, and severity level of the problem, as
  well as a textual description of the problem.  The possible severity
  levels range from informational messages to fatal errors see the
  documentation for SedError for more information.

  If the file 'filename' could not be read, the file-reading error will
  appear first.  The error code can provide a clue about what happened.
  For example, a file might be unreadable (either because it does not
  actually exist or because the user does not have the necessary access
  priviledges to read it) or some sort of file operation error may have
  been reported by the underlying operating system.  Callers can check
  for these situations using a program fragment such as the following:

   reader = SedReader()
   doc    = reader.readSedML(filename)

   if doc.getNumErrors() > 0:
     if doc.getError(0).getErrorId() == libsedml.XMLFileUnreadable:
# Handle case of unreadable file here.
     elif doc.getError(0).getErrorId() == libsedml.XMLFileOperationError:
# Handle case of other file error here.
     else:
# Handle other error cases here.

  If the given filename ends with the suffix ".gz" (for example,
  "myfile.xml.gz"), the file is assumed to be compressed in gzip format
  and will be automatically decompressed upon reading.  Similarly, if the
  given filename ends with ".zip" or ".bz2", the file is assumed to be
  compressed in zip or bzip2 format (respectively).  Files whose names
  lack these suffixes will be read uncompressed.  Note that if the file
  is in zip format but the archive contains more than one file, only the
  first file in the archive will be read and the rest ignored.

  To read a gzip/zip file, libSEDML needs to be configured and linked with
  the zlib library at compile time.  It also needs to be linked with the
  bzip2 library to read files in bzip2 format.  (Both of these are the
  default configurations for libSEDML.)  Errors about unreadable files
  will be logged if a compressed filename is given and libSEDML was not
  linked with the corresponding required library.

  Parameter 'filename is the name or full pathname of the file to be
  read.

  Returns a pointer to the SedDocument created from the Sed content.

  See also SedError.

  Note:

  LibSEDML versions 2.x and later versions behave differently in
  error handling in several respects.  One difference is how early some
  errors are caught and whether libSEDML continues processing a file in
  the face of some early errors.  In general, libSEDML versions after 2.x
  stop parsing Sed inputs sooner than libSEDML version 2.x in the face
  of XML errors, because the errors may invalidate any further Sed
  content.  For example, a missing XML declaration at the beginning of
  the file was ignored by libSEDML 2.x but in version 3.x and later, it
  will cause libSEDML to stop parsing the rest of the input altogether.
  While this behavior may seem more severe and intolerant, it was
  necessary in order to provide uniform behavior regardless of which
  underlying XML parser (Expat, Xerces, libxml2) is being used by
  libSEDML.  The XML parsers themselves behave differently in their error
  reporting, and sometimes libSEDML has to resort to the lowest common
  denominator.
  """
    reader = SedReader()
    return reader.readSedML(args[0])


class DoubleStdVector(object):
    """Proxy of C++ std::vector< double > class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self):
        """iterator(DoubleStdVector self) -> SwigPyIterator"""
        return _libsedml.DoubleStdVector_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        """__nonzero__(DoubleStdVector self) -> bool"""
        return _libsedml.DoubleStdVector___nonzero__(self)

    def __bool__(self):
        """__bool__(DoubleStdVector self) -> bool"""
        return _libsedml.DoubleStdVector___bool__(self)

    def __len__(self):
        """__len__(DoubleStdVector self) -> std::vector< double >::size_type"""
        return _libsedml.DoubleStdVector___len__(self)

    def __getslice__(self, i, j):
        """__getslice__(DoubleStdVector self, std::vector< double >::difference_type i, std::vector< double >::difference_type j) -> DoubleStdVector"""
        return _libsedml.DoubleStdVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        """
        __setslice__(DoubleStdVector self, std::vector< double >::difference_type i, std::vector< double >::difference_type j)
        __setslice__(DoubleStdVector self, std::vector< double >::difference_type i, std::vector< double >::difference_type j, DoubleStdVector v)
        """
        return _libsedml.DoubleStdVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        """__delslice__(DoubleStdVector self, std::vector< double >::difference_type i, std::vector< double >::difference_type j)"""
        return _libsedml.DoubleStdVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        """
        __delitem__(DoubleStdVector self, std::vector< double >::difference_type i)
        __delitem__(DoubleStdVector self, PySliceObject * slice)
        """
        return _libsedml.DoubleStdVector___delitem__(self, *args)

    def __getitem__(self, *args):
        """
        __getitem__(DoubleStdVector self, PySliceObject * slice) -> DoubleStdVector
        __getitem__(DoubleStdVector self, std::vector< double >::difference_type i) -> std::vector< double >::value_type const &
        """
        return _libsedml.DoubleStdVector___getitem__(self, *args)

    def __setitem__(self, *args):
        """
        __setitem__(DoubleStdVector self, PySliceObject * slice, DoubleStdVector v)
        __setitem__(DoubleStdVector self, PySliceObject * slice)
        __setitem__(DoubleStdVector self, std::vector< double >::difference_type i, std::vector< double >::value_type const & x)
        """
        return _libsedml.DoubleStdVector___setitem__(self, *args)

    def pop(self):
        """pop(DoubleStdVector self) -> std::vector< double >::value_type"""
        return _libsedml.DoubleStdVector_pop(self)

    def append(self, x):
        """append(DoubleStdVector self, std::vector< double >::value_type const & x)"""
        return _libsedml.DoubleStdVector_append(self, x)

    def empty(self):
        """empty(DoubleStdVector self) -> bool"""
        return _libsedml.DoubleStdVector_empty(self)

    def size(self):
        """size(DoubleStdVector self) -> std::vector< double >::size_type"""
        return _libsedml.DoubleStdVector_size(self)

    def swap(self, v):
        """swap(DoubleStdVector self, DoubleStdVector v)"""
        return _libsedml.DoubleStdVector_swap(self, v)

    def begin(self):
        """begin(DoubleStdVector self) -> std::vector< double >::iterator"""
        return _libsedml.DoubleStdVector_begin(self)

    def end(self):
        """end(DoubleStdVector self) -> std::vector< double >::iterator"""
        return _libsedml.DoubleStdVector_end(self)

    def rbegin(self):
        """rbegin(DoubleStdVector self) -> std::vector< double >::reverse_iterator"""
        return _libsedml.DoubleStdVector_rbegin(self)

    def rend(self):
        """rend(DoubleStdVector self) -> std::vector< double >::reverse_iterator"""
        return _libsedml.DoubleStdVector_rend(self)

    def clear(self):
        """clear(DoubleStdVector self)"""
        return _libsedml.DoubleStdVector_clear(self)

    def get_allocator(self):
        """get_allocator(DoubleStdVector self) -> std::vector< double >::allocator_type"""
        return _libsedml.DoubleStdVector_get_allocator(self)

    def pop_back(self):
        """pop_back(DoubleStdVector self)"""
        return _libsedml.DoubleStdVector_pop_back(self)

    def erase(self, *args):
        """
        erase(DoubleStdVector self, std::vector< double >::iterator pos) -> std::vector< double >::iterator
        erase(DoubleStdVector self, std::vector< double >::iterator first, std::vector< double >::iterator last) -> std::vector< double >::iterator
        """
        return _libsedml.DoubleStdVector_erase(self, *args)

    def __init__(self, *args):
        """
        __init__(DoubleStdVector self) -> DoubleStdVector
        __init__(DoubleStdVector self, DoubleStdVector other) -> DoubleStdVector
        __init__(DoubleStdVector self, std::vector< double >::size_type size) -> DoubleStdVector
        __init__(DoubleStdVector self, std::vector< double >::size_type size, std::vector< double >::value_type const & value) -> DoubleStdVector
        """
        _libsedml.DoubleStdVector_swiginit(self, _libsedml.new_DoubleStdVector(*args))

    def push_back(self, x):
        """push_back(DoubleStdVector self, std::vector< double >::value_type const & x)"""
        return _libsedml.DoubleStdVector_push_back(self, x)

    def front(self):
        """front(DoubleStdVector self) -> std::vector< double >::value_type const &"""
        return _libsedml.DoubleStdVector_front(self)

    def back(self):
        """back(DoubleStdVector self) -> std::vector< double >::value_type const &"""
        return _libsedml.DoubleStdVector_back(self)

    def assign(self, n, x):
        """assign(DoubleStdVector self, std::vector< double >::size_type n, std::vector< double >::value_type const & x)"""
        return _libsedml.DoubleStdVector_assign(self, n, x)

    def resize(self, *args):
        """
        resize(DoubleStdVector self, std::vector< double >::size_type new_size)
        resize(DoubleStdVector self, std::vector< double >::size_type new_size, std::vector< double >::value_type const & x)
        """
        return _libsedml.DoubleStdVector_resize(self, *args)

    def insert(self, *args):
        """
        insert(DoubleStdVector self, std::vector< double >::iterator pos, std::vector< double >::value_type const & x) -> std::vector< double >::iterator
        insert(DoubleStdVector self, std::vector< double >::iterator pos, std::vector< double >::size_type n, std::vector< double >::value_type const & x)
        """
        return _libsedml.DoubleStdVector_insert(self, *args)

    def reserve(self, n):
        """reserve(DoubleStdVector self, std::vector< double >::size_type n)"""
        return _libsedml.DoubleStdVector_reserve(self, n)

    def capacity(self):
        """capacity(DoubleStdVector self) -> std::vector< double >::size_type"""
        return _libsedml.DoubleStdVector_capacity(self)

    __swig_destroy__ = _libsedml.delete_DoubleStdVector


_libsedml.DoubleStdVector_swigregister(DoubleStdVector)
cout = cvar.cout
cerr = cvar.cerr
clog = cvar.clog

class XmlErrorStdVector(object):
    """Proxy of C++ std::vector< XMLError * > class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self):
        """iterator(XmlErrorStdVector self) -> SwigPyIterator"""
        return _libsedml.XmlErrorStdVector_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        """__nonzero__(XmlErrorStdVector self) -> bool"""
        return _libsedml.XmlErrorStdVector___nonzero__(self)

    def __bool__(self):
        """__bool__(XmlErrorStdVector self) -> bool"""
        return _libsedml.XmlErrorStdVector___bool__(self)

    def __len__(self):
        """__len__(XmlErrorStdVector self) -> std::vector< XMLError * >::size_type"""
        return _libsedml.XmlErrorStdVector___len__(self)

    def __getslice__(self, i, j):
        """__getslice__(XmlErrorStdVector self, std::vector< XMLError * >::difference_type i, std::vector< XMLError * >::difference_type j) -> XmlErrorStdVector"""
        return _libsedml.XmlErrorStdVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        """
        __setslice__(XmlErrorStdVector self, std::vector< XMLError * >::difference_type i, std::vector< XMLError * >::difference_type j)
        __setslice__(XmlErrorStdVector self, std::vector< XMLError * >::difference_type i, std::vector< XMLError * >::difference_type j, XmlErrorStdVector v)
        """
        return _libsedml.XmlErrorStdVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        """__delslice__(XmlErrorStdVector self, std::vector< XMLError * >::difference_type i, std::vector< XMLError * >::difference_type j)"""
        return _libsedml.XmlErrorStdVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        """
        __delitem__(XmlErrorStdVector self, std::vector< XMLError * >::difference_type i)
        __delitem__(XmlErrorStdVector self, PySliceObject * slice)
        """
        return _libsedml.XmlErrorStdVector___delitem__(self, *args)

    def __getitem__(self, *args):
        """
        __getitem__(XmlErrorStdVector self, PySliceObject * slice) -> XmlErrorStdVector
        __getitem__(XmlErrorStdVector self, std::vector< XMLError * >::difference_type i) -> XMLError
        """
        return _libsedml.XmlErrorStdVector___getitem__(self, *args)

    def __setitem__(self, *args):
        """
        __setitem__(XmlErrorStdVector self, PySliceObject * slice, XmlErrorStdVector v)
        __setitem__(XmlErrorStdVector self, PySliceObject * slice)
        __setitem__(XmlErrorStdVector self, std::vector< XMLError * >::difference_type i, XMLError x)
        """
        return _libsedml.XmlErrorStdVector___setitem__(self, *args)

    def pop(self):
        """pop(XmlErrorStdVector self) -> XMLError"""
        return _libsedml.XmlErrorStdVector_pop(self)

    def append(self, x):
        """append(XmlErrorStdVector self, XMLError x)"""
        return _libsedml.XmlErrorStdVector_append(self, x)

    def empty(self):
        """empty(XmlErrorStdVector self) -> bool"""
        return _libsedml.XmlErrorStdVector_empty(self)

    def size(self):
        """size(XmlErrorStdVector self) -> std::vector< XMLError * >::size_type"""
        return _libsedml.XmlErrorStdVector_size(self)

    def swap(self, v):
        """swap(XmlErrorStdVector self, XmlErrorStdVector v)"""
        return _libsedml.XmlErrorStdVector_swap(self, v)

    def begin(self):
        """begin(XmlErrorStdVector self) -> std::vector< XMLError * >::iterator"""
        return _libsedml.XmlErrorStdVector_begin(self)

    def end(self):
        """end(XmlErrorStdVector self) -> std::vector< XMLError * >::iterator"""
        return _libsedml.XmlErrorStdVector_end(self)

    def rbegin(self):
        """rbegin(XmlErrorStdVector self) -> std::vector< XMLError * >::reverse_iterator"""
        return _libsedml.XmlErrorStdVector_rbegin(self)

    def rend(self):
        """rend(XmlErrorStdVector self) -> std::vector< XMLError * >::reverse_iterator"""
        return _libsedml.XmlErrorStdVector_rend(self)

    def clear(self):
        """clear(XmlErrorStdVector self)"""
        return _libsedml.XmlErrorStdVector_clear(self)

    def get_allocator(self):
        """get_allocator(XmlErrorStdVector self) -> std::vector< XMLError * >::allocator_type"""
        return _libsedml.XmlErrorStdVector_get_allocator(self)

    def pop_back(self):
        """pop_back(XmlErrorStdVector self)"""
        return _libsedml.XmlErrorStdVector_pop_back(self)

    def erase(self, *args):
        """
        erase(XmlErrorStdVector self, std::vector< XMLError * >::iterator pos) -> std::vector< XMLError * >::iterator
        erase(XmlErrorStdVector self, std::vector< XMLError * >::iterator first, std::vector< XMLError * >::iterator last) -> std::vector< XMLError * >::iterator
        """
        return _libsedml.XmlErrorStdVector_erase(self, *args)

    def __init__(self, *args):
        """
        __init__(XmlErrorStdVector self) -> XmlErrorStdVector
        __init__(XmlErrorStdVector self, XmlErrorStdVector other) -> XmlErrorStdVector
        __init__(XmlErrorStdVector self, std::vector< XMLError * >::size_type size) -> XmlErrorStdVector
        __init__(XmlErrorStdVector self, std::vector< XMLError * >::size_type size, XMLError value) -> XmlErrorStdVector
        """
        _libsedml.XmlErrorStdVector_swiginit(self, _libsedml.new_XmlErrorStdVector(*args))

    def push_back(self, x):
        """push_back(XmlErrorStdVector self, XMLError x)"""
        return _libsedml.XmlErrorStdVector_push_back(self, x)

    def front(self):
        """front(XmlErrorStdVector self) -> XMLError"""
        return _libsedml.XmlErrorStdVector_front(self)

    def back(self):
        """back(XmlErrorStdVector self) -> XMLError"""
        return _libsedml.XmlErrorStdVector_back(self)

    def assign(self, n, x):
        """assign(XmlErrorStdVector self, std::vector< XMLError * >::size_type n, XMLError x)"""
        return _libsedml.XmlErrorStdVector_assign(self, n, x)

    def resize(self, *args):
        """
        resize(XmlErrorStdVector self, std::vector< XMLError * >::size_type new_size)
        resize(XmlErrorStdVector self, std::vector< XMLError * >::size_type new_size, XMLError x)
        """
        return _libsedml.XmlErrorStdVector_resize(self, *args)

    def insert(self, *args):
        """
        insert(XmlErrorStdVector self, std::vector< XMLError * >::iterator pos, XMLError x) -> std::vector< XMLError * >::iterator
        insert(XmlErrorStdVector self, std::vector< XMLError * >::iterator pos, std::vector< XMLError * >::size_type n, XMLError x)
        """
        return _libsedml.XmlErrorStdVector_insert(self, *args)

    def reserve(self, n):
        """reserve(XmlErrorStdVector self, std::vector< XMLError * >::size_type n)"""
        return _libsedml.XmlErrorStdVector_reserve(self, n)

    def capacity(self):
        """capacity(XmlErrorStdVector self) -> std::vector< XMLError * >::size_type"""
        return _libsedml.XmlErrorStdVector_capacity(self)

    __swig_destroy__ = _libsedml.delete_XmlErrorStdVector


_libsedml.XmlErrorStdVector_swigregister(XmlErrorStdVector)

class SedErrorStdVector(object):
    """Proxy of C++ std::vector< SedError > class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self):
        """iterator(SedErrorStdVector self) -> SwigPyIterator"""
        return _libsedml.SedErrorStdVector_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        """__nonzero__(SedErrorStdVector self) -> bool"""
        return _libsedml.SedErrorStdVector___nonzero__(self)

    def __bool__(self):
        """__bool__(SedErrorStdVector self) -> bool"""
        return _libsedml.SedErrorStdVector___bool__(self)

    def __len__(self):
        """__len__(SedErrorStdVector self) -> std::vector< SedError >::size_type"""
        return _libsedml.SedErrorStdVector___len__(self)

    def __getslice__(self, i, j):
        """__getslice__(SedErrorStdVector self, std::vector< SedError >::difference_type i, std::vector< SedError >::difference_type j) -> SedErrorStdVector"""
        return _libsedml.SedErrorStdVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        """
        __setslice__(SedErrorStdVector self, std::vector< SedError >::difference_type i, std::vector< SedError >::difference_type j)
        __setslice__(SedErrorStdVector self, std::vector< SedError >::difference_type i, std::vector< SedError >::difference_type j, SedErrorStdVector v)
        """
        return _libsedml.SedErrorStdVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        """__delslice__(SedErrorStdVector self, std::vector< SedError >::difference_type i, std::vector< SedError >::difference_type j)"""
        return _libsedml.SedErrorStdVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        """
        __delitem__(SedErrorStdVector self, std::vector< SedError >::difference_type i)
        __delitem__(SedErrorStdVector self, PySliceObject * slice)
        """
        return _libsedml.SedErrorStdVector___delitem__(self, *args)

    def __getitem__(self, *args):
        """
        __getitem__(SedErrorStdVector self, PySliceObject * slice) -> SedErrorStdVector
        __getitem__(SedErrorStdVector self, std::vector< SedError >::difference_type i) -> SedError
        """
        return _libsedml.SedErrorStdVector___getitem__(self, *args)

    def __setitem__(self, *args):
        """
        __setitem__(SedErrorStdVector self, PySliceObject * slice, SedErrorStdVector v)
        __setitem__(SedErrorStdVector self, PySliceObject * slice)
        __setitem__(SedErrorStdVector self, std::vector< SedError >::difference_type i, SedError x)
        """
        return _libsedml.SedErrorStdVector___setitem__(self, *args)

    def pop(self):
        """pop(SedErrorStdVector self) -> SedError"""
        return _libsedml.SedErrorStdVector_pop(self)

    def append(self, x):
        """append(SedErrorStdVector self, SedError x)"""
        return _libsedml.SedErrorStdVector_append(self, x)

    def empty(self):
        """empty(SedErrorStdVector self) -> bool"""
        return _libsedml.SedErrorStdVector_empty(self)

    def size(self):
        """size(SedErrorStdVector self) -> std::vector< SedError >::size_type"""
        return _libsedml.SedErrorStdVector_size(self)

    def swap(self, v):
        """swap(SedErrorStdVector self, SedErrorStdVector v)"""
        return _libsedml.SedErrorStdVector_swap(self, v)

    def begin(self):
        """begin(SedErrorStdVector self) -> std::vector< SedError >::iterator"""
        return _libsedml.SedErrorStdVector_begin(self)

    def end(self):
        """end(SedErrorStdVector self) -> std::vector< SedError >::iterator"""
        return _libsedml.SedErrorStdVector_end(self)

    def rbegin(self):
        """rbegin(SedErrorStdVector self) -> std::vector< SedError >::reverse_iterator"""
        return _libsedml.SedErrorStdVector_rbegin(self)

    def rend(self):
        """rend(SedErrorStdVector self) -> std::vector< SedError >::reverse_iterator"""
        return _libsedml.SedErrorStdVector_rend(self)

    def clear(self):
        """clear(SedErrorStdVector self)"""
        return _libsedml.SedErrorStdVector_clear(self)

    def get_allocator(self):
        """get_allocator(SedErrorStdVector self) -> std::vector< SedError >::allocator_type"""
        return _libsedml.SedErrorStdVector_get_allocator(self)

    def pop_back(self):
        """pop_back(SedErrorStdVector self)"""
        return _libsedml.SedErrorStdVector_pop_back(self)

    def erase(self, *args):
        """
        erase(SedErrorStdVector self, std::vector< SedError >::iterator pos) -> std::vector< SedError >::iterator
        erase(SedErrorStdVector self, std::vector< SedError >::iterator first, std::vector< SedError >::iterator last) -> std::vector< SedError >::iterator
        """
        return _libsedml.SedErrorStdVector_erase(self, *args)

    def __init__(self, *args):
        """
        __init__(SedErrorStdVector self) -> SedErrorStdVector
        __init__(SedErrorStdVector self, SedErrorStdVector other) -> SedErrorStdVector
        __init__(SedErrorStdVector self, std::vector< SedError >::size_type size) -> SedErrorStdVector
        __init__(SedErrorStdVector self, std::vector< SedError >::size_type size, SedError value) -> SedErrorStdVector
        """
        _libsedml.SedErrorStdVector_swiginit(self, _libsedml.new_SedErrorStdVector(*args))

    def push_back(self, x):
        """push_back(SedErrorStdVector self, SedError x)"""
        return _libsedml.SedErrorStdVector_push_back(self, x)

    def front(self):
        """front(SedErrorStdVector self) -> SedError"""
        return _libsedml.SedErrorStdVector_front(self)

    def back(self):
        """back(SedErrorStdVector self) -> SedError"""
        return _libsedml.SedErrorStdVector_back(self)

    def assign(self, n, x):
        """assign(SedErrorStdVector self, std::vector< SedError >::size_type n, SedError x)"""
        return _libsedml.SedErrorStdVector_assign(self, n, x)

    def resize(self, *args):
        """
        resize(SedErrorStdVector self, std::vector< SedError >::size_type new_size)
        resize(SedErrorStdVector self, std::vector< SedError >::size_type new_size, SedError x)
        """
        return _libsedml.SedErrorStdVector_resize(self, *args)

    def insert(self, *args):
        """
        insert(SedErrorStdVector self, std::vector< SedError >::iterator pos, SedError x) -> std::vector< SedError >::iterator
        insert(SedErrorStdVector self, std::vector< SedError >::iterator pos, std::vector< SedError >::size_type n, SedError x)
        """
        return _libsedml.SedErrorStdVector_insert(self, *args)

    def reserve(self, n):
        """reserve(SedErrorStdVector self, std::vector< SedError >::size_type n)"""
        return _libsedml.SedErrorStdVector_reserve(self, n)

    def capacity(self):
        """capacity(SedErrorStdVector self) -> std::vector< SedError >::size_type"""
        return _libsedml.SedErrorStdVector_capacity(self)

    __swig_destroy__ = _libsedml.delete_SedErrorStdVector


_libsedml.SedErrorStdVector_swigregister(SedErrorStdVector)
LIBSEDML_DOTTED_VERSION = _libsedml.LIBSEDML_DOTTED_VERSION
LIBSEDML_VERSION = _libsedml.LIBSEDML_VERSION
LIBSEDML_VERSION_STRING = _libsedml.LIBSEDML_VERSION_STRING

def getLibSEDMLVersion():
    """getLibSEDMLVersion() -> int"""
    return _libsedml.getLibSEDMLVersion()


def getLibSEDMLDottedVersion():
    """getLibSEDMLDottedVersion() -> char const *"""
    return _libsedml.getLibSEDMLDottedVersion()


def getLibSEDMLVersionString():
    """getLibSEDMLVersionString() -> char const *"""
    return _libsedml.getLibSEDMLVersionString()


LIBSEDML_OPERATION_SUCCESS = _libsedml.LIBSEDML_OPERATION_SUCCESS
LIBSEDML_INDEX_EXCEEDS_SIZE = _libsedml.LIBSEDML_INDEX_EXCEEDS_SIZE
LIBSEDML_UNEXPECTED_ATTRIBUTE = _libsedml.LIBSEDML_UNEXPECTED_ATTRIBUTE
LIBSEDML_OPERATION_FAILED = _libsedml.LIBSEDML_OPERATION_FAILED
LIBSEDML_INVALID_ATTRIBUTE_VALUE = _libsedml.LIBSEDML_INVALID_ATTRIBUTE_VALUE
LIBSEDML_INVALID_OBJECT = _libsedml.LIBSEDML_INVALID_OBJECT
LIBSEDML_DUPLICATE_OBJECT_ID = _libsedml.LIBSEDML_DUPLICATE_OBJECT_ID
LIBSEDML_LEVEL_MISMATCH = _libsedml.LIBSEDML_LEVEL_MISMATCH
LIBSEDML_VERSION_MISMATCH = _libsedml.LIBSEDML_VERSION_MISMATCH
LIBSEDML_INVALID_XML_OPERATION = _libsedml.LIBSEDML_INVALID_XML_OPERATION
LIBSEDML_NAMESPACES_MISMATCH = _libsedml.LIBSEDML_NAMESPACES_MISMATCH
LIBSEDML_DUPLICATE_ANNOTATION_NS = _libsedml.LIBSEDML_DUPLICATE_ANNOTATION_NS
LIBSEDML_ANNOTATION_NAME_NOT_FOUND = _libsedml.LIBSEDML_ANNOTATION_NAME_NOT_FOUND
LIBSEDML_ANNOTATION_NS_NOT_FOUND = _libsedml.LIBSEDML_ANNOTATION_NS_NOT_FOUND
LIBSEDML_MISSING_METAID = _libsedml.LIBSEDML_MISSING_METAID
LIBSEDML_DEPRECATED_ATTRIBUTE = _libsedml.LIBSEDML_DEPRECATED_ATTRIBUTE

def SedOperationReturnValue_toString(returnValue):
    """SedOperationReturnValue_toString(int returnValue) -> char const *"""
    return _libsedml.SedOperationReturnValue_toString(returnValue)


LIBSBML_DOTTED_VERSION = _libsedml.LIBSBML_DOTTED_VERSION
LIBSBML_VERSION = _libsedml.LIBSBML_VERSION
LIBSBML_VERSION_STRING = _libsedml.LIBSBML_VERSION_STRING

def getLibSBMLVersion():
    """getLibSBMLVersion() -> int"""
    return _libsedml.getLibSBMLVersion()


def getLibSBMLDottedVersion():
    """getLibSBMLDottedVersion() -> char const *"""
    return _libsedml.getLibSBMLDottedVersion()


def getLibSBMLVersionString():
    """getLibSBMLVersionString() -> char const *"""
    return _libsedml.getLibSBMLVersionString()


def isLibSBMLCompiledWith(option):
    """isLibSBMLCompiledWith(char const * option) -> int"""
    return _libsedml.isLibSBMLCompiledWith(option)


def getLibSBMLDependencyVersionOf(option):
    """getLibSBMLDependencyVersionOf(char const * option) -> char const *"""
    return _libsedml.getLibSBMLDependencyVersionOf(option)


LIBSBML_OPERATION_SUCCESS = _libsedml.LIBSBML_OPERATION_SUCCESS
LIBSBML_INDEX_EXCEEDS_SIZE = _libsedml.LIBSBML_INDEX_EXCEEDS_SIZE
LIBSBML_UNEXPECTED_ATTRIBUTE = _libsedml.LIBSBML_UNEXPECTED_ATTRIBUTE
LIBSBML_OPERATION_FAILED = _libsedml.LIBSBML_OPERATION_FAILED
LIBSBML_INVALID_ATTRIBUTE_VALUE = _libsedml.LIBSBML_INVALID_ATTRIBUTE_VALUE
LIBSBML_INVALID_OBJECT = _libsedml.LIBSBML_INVALID_OBJECT
LIBSBML_DUPLICATE_OBJECT_ID = _libsedml.LIBSBML_DUPLICATE_OBJECT_ID
LIBSBML_LEVEL_MISMATCH = _libsedml.LIBSBML_LEVEL_MISMATCH
LIBSBML_VERSION_MISMATCH = _libsedml.LIBSBML_VERSION_MISMATCH
LIBSBML_INVALID_XML_OPERATION = _libsedml.LIBSBML_INVALID_XML_OPERATION
LIBSBML_NAMESPACES_MISMATCH = _libsedml.LIBSBML_NAMESPACES_MISMATCH
LIBSBML_DUPLICATE_ANNOTATION_NS = _libsedml.LIBSBML_DUPLICATE_ANNOTATION_NS
LIBSBML_ANNOTATION_NAME_NOT_FOUND = _libsedml.LIBSBML_ANNOTATION_NAME_NOT_FOUND
LIBSBML_ANNOTATION_NS_NOT_FOUND = _libsedml.LIBSBML_ANNOTATION_NS_NOT_FOUND
LIBSBML_MISSING_METAID = _libsedml.LIBSBML_MISSING_METAID
LIBSBML_DEPRECATED_ATTRIBUTE = _libsedml.LIBSBML_DEPRECATED_ATTRIBUTE
LIBSBML_USE_ID_ATTRIBUTE_FUNCTION = _libsedml.LIBSBML_USE_ID_ATTRIBUTE_FUNCTION
LIBSBML_PKG_VERSION_MISMATCH = _libsedml.LIBSBML_PKG_VERSION_MISMATCH
LIBSBML_PKG_UNKNOWN = _libsedml.LIBSBML_PKG_UNKNOWN
LIBSBML_PKG_UNKNOWN_VERSION = _libsedml.LIBSBML_PKG_UNKNOWN_VERSION
LIBSBML_PKG_DISABLED = _libsedml.LIBSBML_PKG_DISABLED
LIBSBML_PKG_CONFLICTED_VERSION = _libsedml.LIBSBML_PKG_CONFLICTED_VERSION
LIBSBML_PKG_CONFLICT = _libsedml.LIBSBML_PKG_CONFLICT
LIBSBML_CONV_INVALID_TARGET_NAMESPACE = _libsedml.LIBSBML_CONV_INVALID_TARGET_NAMESPACE
LIBSBML_CONV_PKG_CONVERSION_NOT_AVAILABLE = _libsedml.LIBSBML_CONV_PKG_CONVERSION_NOT_AVAILABLE
LIBSBML_CONV_INVALID_SRC_DOCUMENT = _libsedml.LIBSBML_CONV_INVALID_SRC_DOCUMENT
LIBSBML_CONV_CONVERSION_NOT_AVAILABLE = _libsedml.LIBSBML_CONV_CONVERSION_NOT_AVAILABLE
LIBSBML_CONV_PKG_CONSIDERED_UNKNOWN = _libsedml.LIBSBML_CONV_PKG_CONSIDERED_UNKNOWN

def OperationReturnValue_toString(returnValue):
    """OperationReturnValue_toString(int returnValue) -> char const *"""
    return _libsedml.OperationReturnValue_toString(returnValue)


XMLUnknownError = _libsedml.XMLUnknownError
XMLOutOfMemory = _libsedml.XMLOutOfMemory
XMLFileUnreadable = _libsedml.XMLFileUnreadable
XMLFileUnwritable = _libsedml.XMLFileUnwritable
XMLFileOperationError = _libsedml.XMLFileOperationError
XMLNetworkAccessError = _libsedml.XMLNetworkAccessError
InternalXMLParserError = _libsedml.InternalXMLParserError
UnrecognizedXMLParserCode = _libsedml.UnrecognizedXMLParserCode
XMLTranscoderError = _libsedml.XMLTranscoderError
MissingXMLDecl = _libsedml.MissingXMLDecl
MissingXMLEncoding = _libsedml.MissingXMLEncoding
BadXMLDecl = _libsedml.BadXMLDecl
BadXMLDOCTYPE = _libsedml.BadXMLDOCTYPE
InvalidCharInXML = _libsedml.InvalidCharInXML
BadlyFormedXML = _libsedml.BadlyFormedXML
UnclosedXMLToken = _libsedml.UnclosedXMLToken
InvalidXMLConstruct = _libsedml.InvalidXMLConstruct
XMLTagMismatch = _libsedml.XMLTagMismatch
DuplicateXMLAttribute = _libsedml.DuplicateXMLAttribute
UndefinedXMLEntity = _libsedml.UndefinedXMLEntity
BadProcessingInstruction = _libsedml.BadProcessingInstruction
BadXMLPrefix = _libsedml.BadXMLPrefix
BadXMLPrefixValue = _libsedml.BadXMLPrefixValue
MissingXMLRequiredAttribute = _libsedml.MissingXMLRequiredAttribute
XMLAttributeTypeMismatch = _libsedml.XMLAttributeTypeMismatch
XMLBadUTF8Content = _libsedml.XMLBadUTF8Content
MissingXMLAttributeValue = _libsedml.MissingXMLAttributeValue
BadXMLAttributeValue = _libsedml.BadXMLAttributeValue
BadXMLAttribute = _libsedml.BadXMLAttribute
UnrecognizedXMLElement = _libsedml.UnrecognizedXMLElement
BadXMLComment = _libsedml.BadXMLComment
BadXMLDeclLocation = _libsedml.BadXMLDeclLocation
XMLUnexpectedEOF = _libsedml.XMLUnexpectedEOF
BadXMLIDValue = _libsedml.BadXMLIDValue
BadXMLIDRef = _libsedml.BadXMLIDRef
UninterpretableXMLContent = _libsedml.UninterpretableXMLContent
BadXMLDocumentStructure = _libsedml.BadXMLDocumentStructure
InvalidAfterXMLContent = _libsedml.InvalidAfterXMLContent
XMLExpectedQuotedString = _libsedml.XMLExpectedQuotedString
XMLEmptyValueNotPermitted = _libsedml.XMLEmptyValueNotPermitted
XMLBadNumber = _libsedml.XMLBadNumber
XMLBadColon = _libsedml.XMLBadColon
MissingXMLElements = _libsedml.MissingXMLElements
XMLContentEmpty = _libsedml.XMLContentEmpty
XMLErrorCodesUpperBound = _libsedml.XMLErrorCodesUpperBound
LIBSBML_CAT_INTERNAL = _libsedml.LIBSBML_CAT_INTERNAL
LIBSBML_CAT_SYSTEM = _libsedml.LIBSBML_CAT_SYSTEM
LIBSBML_CAT_XML = _libsedml.LIBSBML_CAT_XML
LIBSBML_SEV_INFO = _libsedml.LIBSBML_SEV_INFO
LIBSBML_SEV_WARNING = _libsedml.LIBSBML_SEV_WARNING
LIBSBML_SEV_ERROR = _libsedml.LIBSBML_SEV_ERROR
LIBSBML_SEV_FATAL = _libsedml.LIBSBML_SEV_FATAL
LIBSBML_OVERRIDE_DISABLED = _libsedml.LIBSBML_OVERRIDE_DISABLED
LIBSBML_OVERRIDE_DONT_LOG = _libsedml.LIBSBML_OVERRIDE_DONT_LOG
LIBSBML_OVERRIDE_WARNING = _libsedml.LIBSBML_OVERRIDE_WARNING
LIBSBML_OVERRIDE_ERROR = _libsedml.LIBSBML_OVERRIDE_ERROR

class XMLError(object):
    """Proxy of C++ XMLError class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(XMLError self, int const errorId=0, string details="", unsigned int const line=0, unsigned int const column=0, unsigned int const severity=LIBSBML_SEV_FATAL, unsigned int const category=LIBSBML_CAT_INTERNAL) -> XMLError
        __init__(XMLError self, XMLError orig) -> XMLError
        """
        _libsedml.XMLError_swiginit(self, _libsedml.new_XMLError(*args))

    __swig_destroy__ = _libsedml.delete_XMLError

    def getErrorId(self):
        """getErrorId(XMLError self) -> unsigned int"""
        return _libsedml.XMLError_getErrorId(self)

    def getMessage(self):
        """getMessage(XMLError self) -> string"""
        return _libsedml.XMLError_getMessage(self)

    def getShortMessage(self):
        """getShortMessage(XMLError self) -> string"""
        return _libsedml.XMLError_getShortMessage(self)

    def getLine(self):
        """getLine(XMLError self) -> unsigned int"""
        return _libsedml.XMLError_getLine(self)

    def getColumn(self):
        """getColumn(XMLError self) -> unsigned int"""
        return _libsedml.XMLError_getColumn(self)

    def getSeverity(self):
        """getSeverity(XMLError self) -> unsigned int"""
        return _libsedml.XMLError_getSeverity(self)

    def getSeverityAsString(self):
        """getSeverityAsString(XMLError self) -> string"""
        return _libsedml.XMLError_getSeverityAsString(self)

    def getCategory(self):
        """getCategory(XMLError self) -> unsigned int"""
        return _libsedml.XMLError_getCategory(self)

    def getCategoryAsString(self):
        """getCategoryAsString(XMLError self) -> string"""
        return _libsedml.XMLError_getCategoryAsString(self)

    def isInfo(self):
        """isInfo(XMLError self) -> bool"""
        return _libsedml.XMLError_isInfo(self)

    def isWarning(self):
        """isWarning(XMLError self) -> bool"""
        return _libsedml.XMLError_isWarning(self)

    def isError(self):
        """isError(XMLError self) -> bool"""
        return _libsedml.XMLError_isError(self)

    def isFatal(self):
        """isFatal(XMLError self) -> bool"""
        return _libsedml.XMLError_isFatal(self)

    def isInternal(self):
        """isInternal(XMLError self) -> bool"""
        return _libsedml.XMLError_isInternal(self)

    def isSystem(self):
        """isSystem(XMLError self) -> bool"""
        return _libsedml.XMLError_isSystem(self)

    def isXML(self):
        """isXML(XMLError self) -> bool"""
        return _libsedml.XMLError_isXML(self)

    def isValid(self):
        """isValid(XMLError self) -> bool"""
        return _libsedml.XMLError_isValid(self)

    def setLine(self, line):
        """setLine(XMLError self, unsigned int line) -> int"""
        return _libsedml.XMLError_setLine(self, line)

    def setColumn(self, column):
        """setColumn(XMLError self, unsigned int column) -> int"""
        return _libsedml.XMLError_setColumn(self, column)

    @staticmethod
    def getStandardMessage(code):
        """getStandardMessage(int const code) -> string"""
        return _libsedml.XMLError_getStandardMessage(code)

    def getPackage(self):
        """getPackage(XMLError self) -> string"""
        return _libsedml.XMLError_getPackage(self)

    def getErrorIdOffset(self):
        """getErrorIdOffset(XMLError self) -> unsigned int"""
        return _libsedml.XMLError_getErrorIdOffset(self)

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True


_libsedml.XMLError_swigregister(XMLError)

def XMLError_getStandardMessage(code):
    """XMLError_getStandardMessage(int const code) -> string"""
    return _libsedml.XMLError_getStandardMessage(code)


class XMLErrorLog(object):
    """Proxy of C++ XMLErrorLog class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getNumErrors(self):
        """getNumErrors(XMLErrorLog self) -> unsigned int"""
        return _libsedml.XMLErrorLog_getNumErrors(self)

    def getError(self, n):
        """getError(XMLErrorLog self, unsigned int n) -> XMLError"""
        return _libsedml.XMLErrorLog_getError(self, n)

    def clearLog(self):
        """clearLog(XMLErrorLog self)"""
        return _libsedml.XMLErrorLog_clearLog(self)

    def __init__(self, *args):
        """
        __init__(XMLErrorLog self) -> XMLErrorLog
        __init__(XMLErrorLog self, XMLErrorLog other) -> XMLErrorLog
        """
        _libsedml.XMLErrorLog_swiginit(self, _libsedml.new_XMLErrorLog(*args))

    __swig_destroy__ = _libsedml.delete_XMLErrorLog

    def add(self, *args):
        """
        add(XMLErrorLog self, XMLError error)
        add(XMLErrorLog self, XmlErrorStdVector errors)
        """
        return _libsedml.XMLErrorLog_add(self, *args)

    def toString(self):
        """toString(XMLErrorLog self) -> string"""
        return _libsedml.XMLErrorLog_toString(self)

    def printErrors(self, *args):
        """
        printErrors(XMLErrorLog self, ostream stream=cerr)
        printErrors(XMLErrorLog self, ostream stream, unsigned int severity)
        """
        return _libsedml.XMLErrorLog_printErrors(self, *args)

    def isSeverityOverridden(self):
        """isSeverityOverridden(XMLErrorLog self) -> bool"""
        return _libsedml.XMLErrorLog_isSeverityOverridden(self)

    def unsetSeverityOverride(self):
        """unsetSeverityOverride(XMLErrorLog self)"""
        return _libsedml.XMLErrorLog_unsetSeverityOverride(self)

    def getSeverityOverride(self):
        """getSeverityOverride(XMLErrorLog self) -> XMLErrorSeverityOverride_t"""
        return _libsedml.XMLErrorLog_getSeverityOverride(self)

    def setSeverityOverride(self, severity):
        """setSeverityOverride(XMLErrorLog self, XMLErrorSeverityOverride_t severity)"""
        return _libsedml.XMLErrorLog_setSeverityOverride(self, severity)

    def changeErrorSeverity(self, *args):
        """changeErrorSeverity(XMLErrorLog self, XMLErrorSeverity_t originalSeverity, XMLErrorSeverity_t targetSeverity, string package="all")"""
        return _libsedml.XMLErrorLog_changeErrorSeverity(self, *args)

    def contains(self, errorId):
        """contains(XMLErrorLog self, unsigned int const errorId) -> bool"""
        return _libsedml.XMLErrorLog_contains(self, errorId)

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True


_libsedml.XMLErrorLog_swigregister(XMLErrorLog)

class SedReader(object):
    """Proxy of C++ SedReader class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        """__init__(SedReader self) -> SedReader"""
        _libsedml.SedReader_swiginit(self, _libsedml.new_SedReader())

    __swig_destroy__ = _libsedml.delete_SedReader

    def readSedML(*args):
        """
      readSedML(self, string filename) -> SedDocument

      Reads an Sed document from a file.

      This method is identical to readSedMLFromFile().

      If the file named 'filename' does not exist or its content is not
      valid Sed, one or more errors will be logged with the SedDocument
      object returned by this method.  Callers can use the methods on
      SedDocument such as SedDocument.getNumErrors() and
      SedDocument.getError() to get the errors.  The object returned by
      SedDocument.getError() is an SedError object, and it has methods to
      get the error code, category, and severity level of the problem, as
      well as a textual description of the problem.  The possible severity
      levels range from informational messages to fatal errors see the
      documentation for SedError for more information.

      If the file 'filename' could not be read, the file-reading error will
      appear first.  The error code can provide a clue about what happened.
      For example, a file might be unreadable (either because it does not
      actually exist or because the user does not have the necessary access
      priviledges to read it) or some sort of file operation error may have
      been reported by the underlying operating system.  Callers can check
      for these situations using a program fragment such as the following:

       reader = SedReader()
       doc    = reader.readSedML(filename)

       if doc.getNumErrors() > 0:
         if doc.getError(0).getErrorId() == libsedml.XMLFileUnreadable:
    # Handle case of unreadable file here.
         elif doc.getError(0).getErrorId() == libsedml.XMLFileOperationError:
    # Handle case of other file error here.
         else:
    # Handle other error cases here.

      If the given filename ends with the suffix ".gz" (for example,
      "myfile.xml.gz"), the file is assumed to be compressed in gzip format
      and will be automatically decompressed upon reading.  Similarly, if the
      given filename ends with ".zip" or ".bz2", the file is assumed to be
      compressed in zip or bzip2 format (respectively).  Files whose names
      lack these suffixes will be read uncompressed.  Note that if the file
      is in zip format but the archive contains more than one file, only the
      first file in the archive will be read and the rest ignored.

      To read a gzip/zip file, libSEDML needs to be configured and linked with
      the zlib library at compile time.  It also needs to be linked with the
      bzip2 library to read files in bzip2 format.  (Both of these are the
      default configurations for libSEDML.)  Errors about unreadable files
      will be logged if a compressed filename is given and libSEDML was not
      linked with the corresponding required library.

      Parameter 'filename is the name or full pathname of the file to be
      read.

      Returns a pointer to the SedDocument created from the Sed content.

      See also SedError.

      Note:

      LibSEDML versions 2.x and later versions behave differently in
      error handling in several respects.  One difference is how early some
      errors are caught and whether libSEDML continues processing a file in
      the face of some early errors.  In general, libSEDML versions after 2.x
      stop parsing Sed inputs sooner than libSEDML version 2.x in the face
      of XML errors, because the errors may invalidate any further Sed
      content.  For example, a missing XML declaration at the beginning of
      the file was ignored by libSEDML 2.x but in version 3.x and later, it
      will cause libSEDML to stop parsing the rest of the input altogether.
      While this behavior may seem more severe and intolerant, it was
      necessary in order to provide uniform behavior regardless of which
      underlying XML parser (Expat, Xerces, libxml2) is being used by
      libSEDML.  The XML parsers themselves behave differently in their error
      reporting, and sometimes libSEDML has to resort to the lowest common
      denominator.
      """
        args_copy = list(args)
        args_copy[1] = conditional_abspath(args[1])
        return _libsedml.SedReader_readSedML(*args_copy)

    def readSedMLFromFile(*args):
        """
      readSedMLFromFile(self, string filename) -> SedDocument

      Reads an Sed document from a file.

      This method is identical to readSedMLFromFile().

      If the file named 'filename' does not exist or its content is not
      valid Sed, one or more errors will be logged with the SedDocument
      object returned by this method.  Callers can use the methods on
      SedDocument such as SedDocument.getNumErrors() and
      SedDocument.getError() to get the errors.  The object returned by
      SedDocument.getError() is an SedError object, and it has methods to
      get the error code, category, and severity level of the problem, as
      well as a textual description of the problem.  The possible severity
      levels range from informational messages to fatal errors see the
      documentation for SedError for more information.

      If the file 'filename' could not be read, the file-reading error will
      appear first.  The error code can provide a clue about what happened.
      For example, a file might be unreadable (either because it does not
      actually exist or because the user does not have the necessary access
      priviledges to read it) or some sort of file operation error may have
      been reported by the underlying operating system.  Callers can check
      for these situations using a program fragment such as the following:

       reader = SedReader()
       doc    = reader.readSedML(filename)

       if doc.getNumErrors() > 0:
         if doc.getError(0).getErrorId() == libsedml.XMLFileUnreadable:
    # Handle case of unreadable file here.
         elif doc.getError(0).getErrorId() == libsedml.XMLFileOperationError:
    # Handle case of other file error here.
         else:
    # Handle other error cases here.

      If the given filename ends with the suffix ".gz" (for example,
      "myfile.xml.gz"), the file is assumed to be compressed in gzip format
      and will be automatically decompressed upon reading.  Similarly, if the
      given filename ends with ".zip" or ".bz2", the file is assumed to be
      compressed in zip or bzip2 format (respectively).  Files whose names
      lack these suffixes will be read uncompressed.  Note that if the file
      is in zip format but the archive contains more than one file, only the
      first file in the archive will be read and the rest ignored.

      To read a gzip/zip file, libSEDML needs to be configured and linked with
      the zlib library at compile time.  It also needs to be linked with the
      bzip2 library to read files in bzip2 format.  (Both of these are the
      default configurations for libSEDML.)  Errors about unreadable files
      will be logged if a compressed filename is given and libSEDML was not
      linked with the corresponding required library.

      Parameter 'filename is the name or full pathname of the file to be
      read.

      Returns a pointer to the SedDocument created from the Sed content.

      See also SedError.

      Note:

      LibSEDML versions 2.x and later versions behave differently in
      error handling in several respects.  One difference is how early some
      errors are caught and whether libSEDML continues processing a file in
      the face of some early errors.  In general, libSEDML versions after 2.x
      stop parsing Sed inputs sooner than libSEDML version 2.x in the face
      of XML errors, because the errors may invalidate any further Sed
      content.  For example, a missing XML declaration at the beginning of
      the file was ignored by libSEDML 2.x but in version 3.x and later, it
      will cause libSEDML to stop parsing the rest of the input altogether.
      While this behavior may seem more severe and intolerant, it was
      necessary in order to provide uniform behavior regardless of which
      underlying XML parser (Expat, Xerces, libxml2) is being used by
      libSEDML.  The XML parsers themselves behave differently in their error
      reporting, and sometimes libSEDML has to resort to the lowest common
      denominator.
      """
        args_copy = list(args)
        args_copy[1] = conditional_abspath(args[1])
        return _libsedml.SedReader_readSedML(*args_copy)

    def readSedMLFromString(self, xml):
        """readSedMLFromString(SedReader self, string xml) -> SedDocument"""
        return _libsedml.SedReader_readSedMLFromString(self, xml)

    @staticmethod
    def hasZlib():
        """hasZlib() -> bool"""
        return _libsedml.SedReader_hasZlib()

    @staticmethod
    def hasBzip2():
        """hasBzip2() -> bool"""
        return _libsedml.SedReader_hasBzip2()

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True


_libsedml.SedReader_swigregister(SedReader)

def SedReader_hasZlib():
    """SedReader_hasZlib() -> bool"""
    return _libsedml.SedReader_hasZlib()


def SedReader_hasBzip2():
    """SedReader_hasBzip2() -> bool"""
    return _libsedml.SedReader_hasBzip2()


def readSedMLFromFile(filename):
    """readSedMLFromFile(char const * filename) -> SedDocument"""
    return _libsedml.readSedMLFromFile(filename)


def readSedMLFromString(xml):
    """readSedMLFromString(char const * xml) -> SedDocument"""
    return _libsedml.readSedMLFromString(xml)


class SedWriter(object):
    """Proxy of C++ SedWriter class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        """__init__(SedWriter self) -> SedWriter"""
        _libsedml.SedWriter_swiginit(self, _libsedml.new_SedWriter())

    __swig_destroy__ = _libsedml.delete_SedWriter

    def setProgramName(self, name):
        """setProgramName(SedWriter self, string name) -> int"""
        return _libsedml.SedWriter_setProgramName(self, name)

    def setProgramVersion(self, version):
        """setProgramVersion(SedWriter self, string version) -> int"""
        return _libsedml.SedWriter_setProgramVersion(self, version)

    def writeSedML(self, *args):
        """
        writeSedML(SedWriter self, SedDocument d, string filename) -> bool
        writeSedML(SedWriter self, SedDocument d, ostream stream) -> bool
        """
        return _libsedml.SedWriter_writeSedML(self, *args)

    def writeToString(self, d):
        """writeToString(SedWriter self, SedDocument d) -> char *"""
        return _libsedml.SedWriter_writeToString(self, d)

    def writeSedMLToFile(self, d, filename):
        """writeSedMLToFile(SedWriter self, SedDocument d, string filename) -> bool"""
        return _libsedml.SedWriter_writeSedMLToFile(self, d, filename)

    def writeSedMLToString(self, d):
        """writeSedMLToString(SedWriter self, SedDocument d) -> char *"""
        return _libsedml.SedWriter_writeSedMLToString(self, d)

    @staticmethod
    def hasZlib():
        """hasZlib() -> bool"""
        return _libsedml.SedWriter_hasZlib()

    @staticmethod
    def hasBzip2():
        """hasBzip2() -> bool"""
        return _libsedml.SedWriter_hasBzip2()

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True


_libsedml.SedWriter_swigregister(SedWriter)

def SedWriter_hasZlib():
    """SedWriter_hasZlib() -> bool"""
    return _libsedml.SedWriter_hasZlib()


def SedWriter_hasBzip2():
    """SedWriter_hasBzip2() -> bool"""
    return _libsedml.SedWriter_hasBzip2()


def writeSedML(d, filename):
    """writeSedML(SedDocument d, char const * filename) -> int"""
    return _libsedml.writeSedML(d, filename)


def writeSedMLToString(d):
    """writeSedMLToString(SedDocument d) -> char *"""
    return _libsedml.writeSedMLToString(d)


def writeSedMLToFile(d, filename):
    """writeSedMLToFile(SedDocument d, char const * filename) -> int"""
    return _libsedml.writeSedMLToFile(d, filename)


SEDML_UNKNOWN = _libsedml.SEDML_UNKNOWN
SEDML_DOCUMENT = _libsedml.SEDML_DOCUMENT
SEDML_MODEL = _libsedml.SEDML_MODEL
SEDML_CHANGE = _libsedml.SEDML_CHANGE
SEDML_CHANGE_ADDXML = _libsedml.SEDML_CHANGE_ADDXML
SEDML_CHANGE_ATTRIBUTE = _libsedml.SEDML_CHANGE_ATTRIBUTE
SEDML_VARIABLE = _libsedml.SEDML_VARIABLE
SEDML_PARAMETER = _libsedml.SEDML_PARAMETER
SEDML_SIMULATION = _libsedml.SEDML_SIMULATION
SEDML_SIMULATION_UNIFORMTIMECOURSE = _libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE
SEDML_SIMULATION_ALGORITHM = _libsedml.SEDML_SIMULATION_ALGORITHM
SEDML_SEDML_ABSTRACTTASK = _libsedml.SEDML_SEDML_ABSTRACTTASK
SEDML_TASK = _libsedml.SEDML_TASK
SEDML_DATAGENERATOR = _libsedml.SEDML_DATAGENERATOR
SEDML_OUTPUT = _libsedml.SEDML_OUTPUT
SEDML_OUTPUT_PLOT = _libsedml.SEDML_OUTPUT_PLOT
SEDML_OUTPUT_PLOT2D = _libsedml.SEDML_OUTPUT_PLOT2D
SEDML_OUTPUT_PLOT3D = _libsedml.SEDML_OUTPUT_PLOT3D
SEDML_ABSTRACTCURVE = _libsedml.SEDML_ABSTRACTCURVE
SEDML_OUTPUT_CURVE = _libsedml.SEDML_OUTPUT_CURVE
SEDML_OUTPUT_SURFACE = _libsedml.SEDML_OUTPUT_SURFACE
SEDML_OUTPUT_DATASET = _libsedml.SEDML_OUTPUT_DATASET
SEDML_OUTPUT_REPORT = _libsedml.SEDML_OUTPUT_REPORT
SEDML_SIMULATION_ALGORITHM_PARAMETER = _libsedml.SEDML_SIMULATION_ALGORITHM_PARAMETER
SEDML_RANGE = _libsedml.SEDML_RANGE
SEDML_CHANGE_CHANGEXML = _libsedml.SEDML_CHANGE_CHANGEXML
SEDML_CHANGE_REMOVEXML = _libsedml.SEDML_CHANGE_REMOVEXML
SEDML_TASK_SETVALUE = _libsedml.SEDML_TASK_SETVALUE
SEDML_RANGE_UNIFORMRANGE = _libsedml.SEDML_RANGE_UNIFORMRANGE
SEDML_RANGE_VECTORRANGE = _libsedml.SEDML_RANGE_VECTORRANGE
SEDML_RANGE_FUNCTIONALRANGE = _libsedml.SEDML_RANGE_FUNCTIONALRANGE
SEDML_TASK_SUBTASK = _libsedml.SEDML_TASK_SUBTASK
SEDML_SIMULATION_ONESTEP = _libsedml.SEDML_SIMULATION_ONESTEP
SEDML_SIMULATION_STEADYSTATE = _libsedml.SEDML_SIMULATION_STEADYSTATE
SEDML_TASK_REPEATEDTASK = _libsedml.SEDML_TASK_REPEATEDTASK
SEDML_CHANGE_COMPUTECHANGE = _libsedml.SEDML_CHANGE_COMPUTECHANGE
SEDML_DATA_DESCRIPTION = _libsedml.SEDML_DATA_DESCRIPTION
SEDML_DATA_SOURCE = _libsedml.SEDML_DATA_SOURCE
SEDML_DATA_SLICE = _libsedml.SEDML_DATA_SLICE
SEDML_TASK_PARAMETER_ESTIMATION = _libsedml.SEDML_TASK_PARAMETER_ESTIMATION
SEDML_OBJECTIVE = _libsedml.SEDML_OBJECTIVE
SEDML_LEAST_SQUARE_OBJECTIVE = _libsedml.SEDML_LEAST_SQUARE_OBJECTIVE
SEDML_ADJUSTABLE_PARAMETER = _libsedml.SEDML_ADJUSTABLE_PARAMETER
SEDML_EXPERIMENT_REF = _libsedml.SEDML_EXPERIMENT_REF
SEDML_FIT_EXPERIMENT = _libsedml.SEDML_FIT_EXPERIMENT
SEDML_FITMAPPING = _libsedml.SEDML_FITMAPPING
SEDML_BOUNDS = _libsedml.SEDML_BOUNDS
SEDML_FIGURE = _libsedml.SEDML_FIGURE
SEDML_SUBPLOT = _libsedml.SEDML_SUBPLOT
SEDML_AXIS = _libsedml.SEDML_AXIS
SEDML_STYLE = _libsedml.SEDML_STYLE
SEDML_LINE = _libsedml.SEDML_LINE
SEDML_MARKER = _libsedml.SEDML_MARKER
SEDML_FILL = _libsedml.SEDML_FILL
SEDML_DEPENDENTVARIABLE = _libsedml.SEDML_DEPENDENTVARIABLE
SEDML_REMAININGDIMENSION = _libsedml.SEDML_REMAININGDIMENSION
SEDML_DATA_RANGE = _libsedml.SEDML_DATA_RANGE
SEDML_TASK_SIMPLEREPEATEDTASK = _libsedml.SEDML_TASK_SIMPLEREPEATEDTASK
SEDML_SHADEDAREA = _libsedml.SEDML_SHADEDAREA
SEDML_PARAMETERESTIMATIONRESULTPLOT = _libsedml.SEDML_PARAMETERESTIMATIONRESULTPLOT
SEDML_WATERFALLPLOT = _libsedml.SEDML_WATERFALLPLOT
SEDML_PARAMETERESTIMATIONREPORT = _libsedml.SEDML_PARAMETERESTIMATIONREPORT
SEDML_LIST_OF = _libsedml.SEDML_LIST_OF

def SedTypeCode_toString(tc):
    """SedTypeCode_toString(int tc) -> char const *"""
    return _libsedml.SedTypeCode_toString(tc)


class SedBase(object):
    """Proxy of C++ SedBase class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined - class is abstract')

    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_SedBase

    def clone(self):
        """clone(SedBase self) -> SedBase"""
        return _libsedml.SedBase_clone(self)

    def getElementBySId(self, *args):
        """
        getElementBySId(SedBase self, string id) -> SedBase
        getElementBySId(SedBase self, string metaid) -> SedBase
        """
        return _libsedml.SedBase_getElementBySId(self, *args)

    def getElementByMetaId(self, *args):
        """
        getElementByMetaId(SedBase self, string metaid) -> SedBase
        getElementByMetaId(SedBase self, string metaid) -> SedBase
        """
        return _libsedml.SedBase_getElementByMetaId(self, *args)

    def getMetaId(self):
        """getMetaId(SedBase self) -> string"""
        return _libsedml.SedBase_getMetaId(self)

    def getId(self):
        """getId(SedBase self) -> string"""
        return _libsedml.SedBase_getId(self)

    def getNotes(self, *args):
        """
        getNotes(SedBase self) -> XMLNode
        getNotes(SedBase self) -> XMLNode
        """
        return _libsedml.SedBase_getNotes(self, *args)

    def getNotesString(self, *args):
        """
        getNotesString(SedBase self) -> string
        getNotesString(SedBase self) -> string
        """
        return _libsedml.SedBase_getNotesString(self, *args)

    def getAnnotation(self, *args):
        """
        getAnnotation(SedBase self) -> XMLNode
        getAnnotation(SedBase self) -> XMLNode
        """
        return _libsedml.SedBase_getAnnotation(self, *args)

    def getAnnotationString(self, *args):
        """
        getAnnotationString(SedBase self) -> string
        getAnnotationString(SedBase self) -> string
        """
        return _libsedml.SedBase_getAnnotationString(self, *args)

    def getNamespaces(self, *args):
        """
        getNamespaces(SedBase self) -> XMLNamespaces
        getNamespaces(SedBase self) -> XMLNamespaces
        """
        return _libsedml.SedBase_getNamespaces(self, *args)

    def getSedDocument(self, *args):
        """
        getSedDocument(SedBase self) -> SedDocument
        getSedDocument(SedBase self) -> SedDocument
        """
        return _libsedml.SedBase_getSedDocument(self, *args)

    def getParentSedObject(self, *args):
        """
        getParentSedObject(SedBase self) -> SedBase
        getParentSedObject(SedBase self) -> SedBase
        """
        return _libsedml.SedBase_getParentSedObject(self, *args)

    def getAncestorOfType(self, *args):
        """
        getAncestorOfType(SedBase self, int type) -> SedBase
        getAncestorOfType(SedBase self, int type) -> SedBase
        """
        return _libsedml.SedBase_getAncestorOfType(self, *args)

    def getLine(self):
        """getLine(SedBase self) -> unsigned int"""
        return _libsedml.SedBase_getLine(self)

    def getColumn(self):
        """getColumn(SedBase self) -> unsigned int"""
        return _libsedml.SedBase_getColumn(self)

    def isSetMetaId(self):
        """isSetMetaId(SedBase self) -> bool"""
        return _libsedml.SedBase_isSetMetaId(self)

    def isSetId(self):
        """isSetId(SedBase self) -> bool"""
        return _libsedml.SedBase_isSetId(self)

    def isSetNotes(self):
        """isSetNotes(SedBase self) -> bool"""
        return _libsedml.SedBase_isSetNotes(self)

    def isSetAnnotation(self):
        """isSetAnnotation(SedBase self) -> bool"""
        return _libsedml.SedBase_isSetAnnotation(self)

    def setMetaId(self, metaid):
        """setMetaId(SedBase self, string metaid) -> int"""
        return _libsedml.SedBase_setMetaId(self, metaid)

    def setId(self, sid):
        """setId(SedBase self, string sid) -> int"""
        return _libsedml.SedBase_setId(self, sid)

    def setAnnotation(self, *args):
        """
        setAnnotation(SedBase self, XMLNode annotation) -> int
        setAnnotation(SedBase self, string annotation) -> int
        """
        return _libsedml.SedBase_setAnnotation(self, *args)

    def appendAnnotation(self, *args):
        """
        appendAnnotation(SedBase self, XMLNode annotation) -> int
        appendAnnotation(SedBase self, string annotation) -> int
        """
        return _libsedml.SedBase_appendAnnotation(self, *args)

    def removeTopLevelAnnotationElement(self, *args):
        """removeTopLevelAnnotationElement(SedBase self, string elementName, string elementURI="") -> int"""
        return _libsedml.SedBase_removeTopLevelAnnotationElement(self, *args)

    def replaceTopLevelAnnotationElement(self, *args):
        """
        replaceTopLevelAnnotationElement(SedBase self, XMLNode annotation) -> int
        replaceTopLevelAnnotationElement(SedBase self, string annotation) -> int
        """
        return _libsedml.SedBase_replaceTopLevelAnnotationElement(self, *args)

    def setNotes(self, *args):
        """
        setNotes(SedBase self, XMLNode notes) -> int
        setNotes(SedBase self, string notes, bool addXHTMLMarkup=False) -> int
        """
        return _libsedml.SedBase_setNotes(self, *args)

    def appendNotes(self, *args):
        """
        appendNotes(SedBase self, XMLNode notes) -> int
        appendNotes(SedBase self, string notes) -> int
        """
        return _libsedml.SedBase_appendNotes(self, *args)

    def connectToParent(self, parent):
        """connectToParent(SedBase self, SedBase parent)"""
        return _libsedml.SedBase_connectToParent(self, parent)

    def connectToChild(self):
        """connectToChild(SedBase self)"""
        return _libsedml.SedBase_connectToChild(self)

    def setNamespaces(self, xmlns):
        """setNamespaces(SedBase self, XMLNamespaces xmlns) -> int"""
        return _libsedml.SedBase_setNamespaces(self, xmlns)

    def unsetMetaId(self):
        """unsetMetaId(SedBase self) -> int"""
        return _libsedml.SedBase_unsetMetaId(self)

    def unsetId(self):
        """unsetId(SedBase self) -> int"""
        return _libsedml.SedBase_unsetId(self)

    def unsetNotes(self):
        """unsetNotes(SedBase self) -> int"""
        return _libsedml.SedBase_unsetNotes(self)

    def unsetAnnotation(self):
        """unsetAnnotation(SedBase self) -> int"""
        return _libsedml.SedBase_unsetAnnotation(self)

    def getLevel(self):
        """getLevel(SedBase self) -> unsigned int"""
        return _libsedml.SedBase_getLevel(self)

    def getVersion(self):
        """getVersion(SedBase self) -> unsigned int"""
        return _libsedml.SedBase_getVersion(self)

    def getTypeCode(self):
        """getTypeCode(SedBase self) -> int"""
        return _libsedml.SedBase_getTypeCode(self)

    def hasValidLevelVersionNamespaceCombination(self):
        """hasValidLevelVersionNamespaceCombination(SedBase self) -> bool"""
        return _libsedml.SedBase_hasValidLevelVersionNamespaceCombination(self)

    def getElementName(self):
        """getElementName(SedBase self) -> string"""
        return _libsedml.SedBase_getElementName(self)

    def toSed(self):
        """toSed(SedBase self) -> char *"""
        return _libsedml.SedBase_toSed(self)

    def read(self, stream):
        """read(SedBase self, XMLInputStream stream)"""
        return _libsedml.SedBase_read(self, stream)

    def write(self, stream):
        """write(SedBase self, XMLOutputStream stream)"""
        return _libsedml.SedBase_write(self, stream)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedBase self) -> bool"""
        return _libsedml.SedBase_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedBase self) -> bool"""
        return _libsedml.SedBase_hasRequiredElements(self)

    def checkCompatibility(self, object):
        """checkCompatibility(SedBase self, SedBase object) -> int"""
        return _libsedml.SedBase_checkCompatibility(self, object)

    def setSedNamespaces(self, sedmlns):
        """setSedNamespaces(SedBase self, SedNamespaces sedmlns) -> int"""
        return _libsedml.SedBase_setSedNamespaces(self, sedmlns)

    def setSedNamespacesAndOwn(self, disownedNs):
        """setSedNamespacesAndOwn(SedBase self, SedNamespaces disownedNs)"""
        return _libsedml.SedBase_setSedNamespacesAndOwn(self, disownedNs)

    def getSedNamespaces(self):
        """getSedNamespaces(SedBase self) -> SedNamespaces"""
        return _libsedml.SedBase_getSedNamespaces(self)

    def removeFromParentAndDelete(self):
        """removeFromParentAndDelete(SedBase self) -> int"""
        return _libsedml.SedBase_removeFromParentAndDelete(self)

    def matchesSedNamespaces(self, *args):
        """
        matchesSedNamespaces(SedBase self, SedBase sb) -> bool
        matchesSedNamespaces(SedBase self, SedBase sb) -> bool
        """
        return _libsedml.SedBase_matchesSedNamespaces(self, *args)

    def matchesRequiredSedNamespacesForAddition(self, *args):
        """
        matchesRequiredSedNamespacesForAddition(SedBase self, SedBase sb) -> bool
        matchesRequiredSedNamespacesForAddition(SedBase self, SedBase sb) -> bool
        """
        return _libsedml.SedBase_matchesRequiredSedNamespacesForAddition(self, *args)

    def isSetUserData(self):
        """isSetUserData(SedBase self) -> bool"""
        return _libsedml.SedBase_isSetUserData(self)

    def unsetUserData(self):
        """unsetUserData(SedBase self) -> int"""
        return _libsedml.SedBase_unsetUserData(self)

    def getErrorLog(self):
        """getErrorLog(SedBase self) -> SedErrorLog"""
        return _libsedml.SedBase_getErrorLog(self)

    __metaclass__ = AutoProperty

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True

    def getListOfAllElements(self):
        """getListOfAllElements(SedBase self) -> SedBaseList"""
        return _libsedml.SedBase_getListOfAllElements(self)


_libsedml.SedBase_swigregister(SedBase)

class SedListOf(SedBase):
    """Proxy of C++ SedListOf class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_SedListOf

    def __init__(self, *args):
        """
        __init__(SedListOf self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOf
        __init__(SedListOf self, SedNamespaces sedmlns) -> SedListOf
        __init__(SedListOf self, SedListOf orig) -> SedListOf
        """
        _libsedml.SedListOf_swiginit(self, _libsedml.new_SedListOf(*args))

    def clone(self):
        """clone(SedListOf self) -> SedListOf"""
        return _libsedml.SedListOf_clone(self)

    def append(self, item):
        """append(SedListOf self, SedBase item) -> int"""
        return _libsedml.SedListOf_append(self, item)

    def appendAndOwn(self, disownedItem):
        """appendAndOwn(SedListOf self, SedBase disownedItem) -> int"""
        if item is not None:
            item.thisown = 0
        return _libsedml.SedListOf_appendAndOwn(self, disownedItem)

    def appendFrom(self, list):
        """appendFrom(SedListOf self, SedListOf list) -> int"""
        return _libsedml.SedListOf_appendFrom(self, list)

    def insert(self, location, item):
        """insert(SedListOf self, int location, SedBase item) -> int"""
        return _libsedml.SedListOf_insert(self, location, item)

    def insertAndOwn(self, location, disownedItem):
        """insertAndOwn(SedListOf self, int location, SedBase disownedItem) -> int"""
        return _libsedml.SedListOf_insertAndOwn(self, location, disownedItem)

    def get(self, *args):
        """
        get(SedListOf self, unsigned int n) -> SedBase
        get(SedListOf self, unsigned int n) -> SedBase
        """
        return _libsedml.SedListOf_get(self, *args)

    def getElementBySId(self, id):
        """getElementBySId(SedListOf self, string id) -> SedBase"""
        return _libsedml.SedListOf_getElementBySId(self, id)

    def getElementByMetaId(self, metaid):
        """getElementByMetaId(SedListOf self, string metaid) -> SedBase"""
        return _libsedml.SedListOf_getElementByMetaId(self, metaid)

    def clear(self, doDelete=True):
        """clear(SedListOf self, bool doDelete=True)"""
        return _libsedml.SedListOf_clear(self, doDelete)

    def removeFromParentAndDelete(self):
        """removeFromParentAndDelete(SedListOf self) -> int"""
        return _libsedml.SedListOf_removeFromParentAndDelete(self)

    def remove(self, n):
        """remove(SedListOf self, unsigned int n) -> SedBase"""
        return _libsedml.SedListOf_remove(self, n)

    def size(self):
        """size(SedListOf self) -> unsigned int"""
        return _libsedml.SedListOf_size(self)

    def connectToChild(self):
        """connectToChild(SedListOf self)"""
        return _libsedml.SedListOf_connectToChild(self)

    def getTypeCode(self):
        """getTypeCode(SedListOf self) -> int"""
        return _libsedml.SedListOf_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOf self) -> int"""
        return _libsedml.SedListOf_getItemTypeCode(self)

    def getElementName(self):
        """getElementName(SedListOf self) -> string"""
        return _libsedml.SedListOf_getElementName(self)

    def __len__(self):
        """__len__(SedListOf self) -> int"""
        return _libsedml.SedListOf___len__(self)

    def __getitem__(self, key):
        try:
            keyIsSlice = isinstance(key, slice)
        except:
            keyIsSlice = 0

        if keyIsSlice:
            start = key.start
            if start is None:
                start = 0
            stop = key.stop
            if stop is None:
                stop = self.size()
            return [ self[i] for i in range(self._fixNegativeIndex(start), self._fixNegativeIndex(stop))
                   ]
        else:
            key = self._fixNegativeIndex(key)
            if key < 0 or key >= self.size():
                raise IndexError(key)
            return self.get(key)

    def _fixNegativeIndex(self, index):
        if index < 0:
            return index + self.size()
        else:
            return index

    def __iter__(self):
        for i in range(self.size()):
            yield self[i]

    def __repr__(self):
        return '[' + (', ').join([ repr(self[i]) for i in range(len(self)) ]) + ']'

    def __str__(self):
        return repr(self)


_libsedml.SedListOf_swigregister(SedListOf)

class SedDocument(SedBase):
    """Proxy of C++ SedDocument class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedDocument self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedDocument
        __init__(SedDocument self, SedNamespaces sedmlns) -> SedDocument
        __init__(SedDocument self, SedDocument orig) -> SedDocument
        """
        _libsedml.SedDocument_swiginit(self, _libsedml.new_SedDocument(*args))

    def clone(self):
        """clone(SedDocument self) -> SedDocument"""
        return _libsedml.SedDocument_clone(self)

    __swig_destroy__ = _libsedml.delete_SedDocument

    def getLevel(self):
        """getLevel(SedDocument self) -> unsigned int"""
        return _libsedml.SedDocument_getLevel(self)

    def getVersion(self):
        """getVersion(SedDocument self) -> unsigned int"""
        return _libsedml.SedDocument_getVersion(self)

    def isSetLevel(self):
        """isSetLevel(SedDocument self) -> bool"""
        return _libsedml.SedDocument_isSetLevel(self)

    def isSetVersion(self):
        """isSetVersion(SedDocument self) -> bool"""
        return _libsedml.SedDocument_isSetVersion(self)

    def setLevel(self, level):
        """setLevel(SedDocument self, unsigned int level) -> int"""
        return _libsedml.SedDocument_setLevel(self, level)

    def setVersion(self, version):
        """setVersion(SedDocument self, unsigned int version) -> int"""
        return _libsedml.SedDocument_setVersion(self, version)

    def unsetLevel(self):
        """unsetLevel(SedDocument self) -> int"""
        return _libsedml.SedDocument_unsetLevel(self)

    def unsetVersion(self):
        """unsetVersion(SedDocument self) -> int"""
        return _libsedml.SedDocument_unsetVersion(self)

    def getListOfDataDescriptions(self, *args):
        """
        getListOfDataDescriptions(SedDocument self) -> SedListOfDataDescriptions
        getListOfDataDescriptions(SedDocument self) -> SedListOfDataDescriptions
        """
        return _libsedml.SedDocument_getListOfDataDescriptions(self, *args)

    def getDataDescription(self, *args):
        """
        getDataDescription(SedDocument self, unsigned int n) -> SedDataDescription
        getDataDescription(SedDocument self, unsigned int n) -> SedDataDescription
        getDataDescription(SedDocument self, string sid) -> SedDataDescription
        getDataDescription(SedDocument self, string sid) -> SedDataDescription
        """
        return _libsedml.SedDocument_getDataDescription(self, *args)

    def addDataDescription(self, sdd):
        """addDataDescription(SedDocument self, SedDataDescription sdd) -> int"""
        return _libsedml.SedDocument_addDataDescription(self, sdd)

    def getNumDataDescriptions(self):
        """getNumDataDescriptions(SedDocument self) -> unsigned int"""
        return _libsedml.SedDocument_getNumDataDescriptions(self)

    def createDataDescription(self):
        """createDataDescription(SedDocument self) -> SedDataDescription"""
        return _libsedml.SedDocument_createDataDescription(self)

    def removeDataDescription(self, *args):
        """
        removeDataDescription(SedDocument self, unsigned int n) -> SedDataDescription
        removeDataDescription(SedDocument self, string sid) -> SedDataDescription
        """
        return _libsedml.SedDocument_removeDataDescription(self, *args)

    def getListOfModels(self, *args):
        """
        getListOfModels(SedDocument self) -> SedListOfModels
        getListOfModels(SedDocument self) -> SedListOfModels
        """
        return _libsedml.SedDocument_getListOfModels(self, *args)

    def getModel(self, *args):
        """
        getModel(SedDocument self, unsigned int n) -> SedModel
        getModel(SedDocument self, unsigned int n) -> SedModel
        getModel(SedDocument self, string sid) -> SedModel
        getModel(SedDocument self, string sid) -> SedModel
        """
        return _libsedml.SedDocument_getModel(self, *args)

    def addModel(self, sm):
        """addModel(SedDocument self, SedModel sm) -> int"""
        return _libsedml.SedDocument_addModel(self, sm)

    def getNumModels(self):
        """getNumModels(SedDocument self) -> unsigned int"""
        return _libsedml.SedDocument_getNumModels(self)

    def createModel(self):
        """createModel(SedDocument self) -> SedModel"""
        return _libsedml.SedDocument_createModel(self)

    def removeModel(self, *args):
        """
        removeModel(SedDocument self, unsigned int n) -> SedModel
        removeModel(SedDocument self, string sid) -> SedModel
        """
        return _libsedml.SedDocument_removeModel(self, *args)

    def getListOfSimulations(self, *args):
        """
        getListOfSimulations(SedDocument self) -> SedListOfSimulations
        getListOfSimulations(SedDocument self) -> SedListOfSimulations
        """
        return _libsedml.SedDocument_getListOfSimulations(self, *args)

    def getSimulation(self, *args):
        """
        getSimulation(SedDocument self, unsigned int n) -> SedSimulation
        getSimulation(SedDocument self, unsigned int n) -> SedSimulation
        getSimulation(SedDocument self, string sid) -> SedSimulation
        getSimulation(SedDocument self, string sid) -> SedSimulation
        """
        return _libsedml.SedDocument_getSimulation(self, *args)

    def addSimulation(self, ss):
        """addSimulation(SedDocument self, SedSimulation ss) -> int"""
        return _libsedml.SedDocument_addSimulation(self, ss)

    def getNumSimulations(self):
        """getNumSimulations(SedDocument self) -> unsigned int"""
        return _libsedml.SedDocument_getNumSimulations(self)

    def createUniformTimeCourse(self):
        """createUniformTimeCourse(SedDocument self) -> SedUniformTimeCourse"""
        return _libsedml.SedDocument_createUniformTimeCourse(self)

    def createOneStep(self):
        """createOneStep(SedDocument self) -> SedOneStep"""
        return _libsedml.SedDocument_createOneStep(self)

    def createSteadyState(self):
        """createSteadyState(SedDocument self) -> SedSteadyState"""
        return _libsedml.SedDocument_createSteadyState(self)

    def removeSimulation(self, *args):
        """
        removeSimulation(SedDocument self, unsigned int n) -> SedSimulation
        removeSimulation(SedDocument self, string sid) -> SedSimulation
        """
        return _libsedml.SedDocument_removeSimulation(self, *args)

    def getListOfTasks(self, *args):
        """
        getListOfTasks(SedDocument self) -> SedListOfTasks
        getListOfTasks(SedDocument self) -> SedListOfTasks
        """
        return _libsedml.SedDocument_getListOfTasks(self, *args)

    def getTask(self, *args):
        """
        getTask(SedDocument self, unsigned int n) -> SedAbstractTask
        getTask(SedDocument self, unsigned int n) -> SedAbstractTask
        getTask(SedDocument self, string sid) -> SedAbstractTask
        getTask(SedDocument self, string sid) -> SedAbstractTask
        """
        return _libsedml.SedDocument_getTask(self, *args)

    def addTask(self, sat):
        """addTask(SedDocument self, SedAbstractTask sat) -> int"""
        return _libsedml.SedDocument_addTask(self, sat)

    def getNumTasks(self):
        """getNumTasks(SedDocument self) -> unsigned int"""
        return _libsedml.SedDocument_getNumTasks(self)

    def createTask(self):
        """createTask(SedDocument self) -> SedTask"""
        return _libsedml.SedDocument_createTask(self)

    def createRepeatedTask(self):
        """createRepeatedTask(SedDocument self) -> SedRepeatedTask"""
        return _libsedml.SedDocument_createRepeatedTask(self)

    def createParameterEstimationTask(self):
        """createParameterEstimationTask(SedDocument self) -> SedParameterEstimationTask"""
        return _libsedml.SedDocument_createParameterEstimationTask(self)

    def createSimpleRepeatedTask(self):
        """createSimpleRepeatedTask(SedDocument self) -> SedSimpleRepeatedTask"""
        return _libsedml.SedDocument_createSimpleRepeatedTask(self)

    def removeTask(self, *args):
        """
        removeTask(SedDocument self, unsigned int n) -> SedAbstractTask
        removeTask(SedDocument self, string sid) -> SedAbstractTask
        """
        return _libsedml.SedDocument_removeTask(self, *args)

    def getListOfDataGenerators(self, *args):
        """
        getListOfDataGenerators(SedDocument self) -> SedListOfDataGenerators
        getListOfDataGenerators(SedDocument self) -> SedListOfDataGenerators
        """
        return _libsedml.SedDocument_getListOfDataGenerators(self, *args)

    def getDataGenerator(self, *args):
        """
        getDataGenerator(SedDocument self, unsigned int n) -> SedDataGenerator
        getDataGenerator(SedDocument self, unsigned int n) -> SedDataGenerator
        getDataGenerator(SedDocument self, string sid) -> SedDataGenerator
        getDataGenerator(SedDocument self, string sid) -> SedDataGenerator
        """
        return _libsedml.SedDocument_getDataGenerator(self, *args)

    def addDataGenerator(self, sdg):
        """addDataGenerator(SedDocument self, SedDataGenerator sdg) -> int"""
        return _libsedml.SedDocument_addDataGenerator(self, sdg)

    def getNumDataGenerators(self):
        """getNumDataGenerators(SedDocument self) -> unsigned int"""
        return _libsedml.SedDocument_getNumDataGenerators(self)

    def createDataGenerator(self):
        """createDataGenerator(SedDocument self) -> SedDataGenerator"""
        return _libsedml.SedDocument_createDataGenerator(self)

    def removeDataGenerator(self, *args):
        """
        removeDataGenerator(SedDocument self, unsigned int n) -> SedDataGenerator
        removeDataGenerator(SedDocument self, string sid) -> SedDataGenerator
        """
        return _libsedml.SedDocument_removeDataGenerator(self, *args)

    def getListOfOutputs(self, *args):
        """
        getListOfOutputs(SedDocument self) -> SedListOfOutputs
        getListOfOutputs(SedDocument self) -> SedListOfOutputs
        """
        return _libsedml.SedDocument_getListOfOutputs(self, *args)

    def getOutput(self, *args):
        """
        getOutput(SedDocument self, unsigned int n) -> SedOutput
        getOutput(SedDocument self, unsigned int n) -> SedOutput
        getOutput(SedDocument self, string sid) -> SedOutput
        getOutput(SedDocument self, string sid) -> SedOutput
        """
        return _libsedml.SedDocument_getOutput(self, *args)

    def addOutput(self, so):
        """addOutput(SedDocument self, SedOutput so) -> int"""
        return _libsedml.SedDocument_addOutput(self, so)

    def getNumOutputs(self):
        """getNumOutputs(SedDocument self) -> unsigned int"""
        return _libsedml.SedDocument_getNumOutputs(self)

    def createReport(self):
        """createReport(SedDocument self) -> SedReport"""
        return _libsedml.SedDocument_createReport(self)

    def createPlot2D(self):
        """createPlot2D(SedDocument self) -> SedPlot2D"""
        return _libsedml.SedDocument_createPlot2D(self)

    def createPlot3D(self):
        """createPlot3D(SedDocument self) -> SedPlot3D"""
        return _libsedml.SedDocument_createPlot3D(self)

    def createFigure(self):
        """createFigure(SedDocument self) -> SedFigure"""
        return _libsedml.SedDocument_createFigure(self)

    def createParameterEstimationResultPlot(self):
        """createParameterEstimationResultPlot(SedDocument self) -> SedParameterEstimationResultPlot"""
        return _libsedml.SedDocument_createParameterEstimationResultPlot(self)

    def removeOutput(self, *args):
        """
        removeOutput(SedDocument self, unsigned int n) -> SedOutput
        removeOutput(SedDocument self, string sid) -> SedOutput
        """
        return _libsedml.SedDocument_removeOutput(self, *args)

    def getListOfStyles(self, *args):
        """
        getListOfStyles(SedDocument self) -> SedListOfStyles const
        getListOfStyles(SedDocument self) -> SedListOfStyles *
        """
        return _libsedml.SedDocument_getListOfStyles(self, *args)

    def getStyle(self, *args):
        """
        getStyle(SedDocument self, unsigned int n) -> SedStyle
        getStyle(SedDocument self, unsigned int n) -> SedStyle
        getStyle(SedDocument self, string sid) -> SedStyle
        getStyle(SedDocument self, string sid) -> SedStyle
        """
        return _libsedml.SedDocument_getStyle(self, *args)

    def getStyleByBaseStyle(self, *args):
        """
        getStyleByBaseStyle(SedDocument self, string sid) -> SedStyle
        getStyleByBaseStyle(SedDocument self, string sid) -> SedStyle
        """
        return _libsedml.SedDocument_getStyleByBaseStyle(self, *args)

    def addStyle(self, ss):
        """addStyle(SedDocument self, SedStyle ss) -> int"""
        return _libsedml.SedDocument_addStyle(self, ss)

    def getNumStyles(self):
        """getNumStyles(SedDocument self) -> unsigned int"""
        return _libsedml.SedDocument_getNumStyles(self)

    def createStyle(self):
        """createStyle(SedDocument self) -> SedStyle"""
        return _libsedml.SedDocument_createStyle(self)

    def removeStyle(self, *args):
        """
        removeStyle(SedDocument self, unsigned int n) -> SedStyle
        removeStyle(SedDocument self, string sid) -> SedStyle
        """
        return _libsedml.SedDocument_removeStyle(self, *args)

    def getElementName(self):
        """getElementName(SedDocument self) -> string"""
        return _libsedml.SedDocument_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedDocument self) -> int"""
        return _libsedml.SedDocument_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedDocument self) -> bool"""
        return _libsedml.SedDocument_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedDocument self)"""
        return _libsedml.SedDocument_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedDocument self, string id) -> SedBase"""
        return _libsedml.SedDocument_getElementBySId(self, id)

    def getNamespaces(self, *args):
        """
        getNamespaces(SedDocument self) -> XMLNamespaces
        getNamespaces(SedDocument self) -> XMLNamespaces
        """
        return _libsedml.SedDocument_getNamespaces(self, *args)

    def getErrorLog(self, *args):
        """
        getErrorLog(SedDocument self) -> SedErrorLog
        getErrorLog(SedDocument self) -> SedErrorLog
        """
        return _libsedml.SedDocument_getErrorLog(self, *args)

    def getError(self, *args):
        """
        getError(SedDocument self, unsigned int n) -> SedError
        getError(SedDocument self, unsigned int n) -> SedError
        """
        return _libsedml.SedDocument_getError(self, *args)

    def getNumErrors(self, *args):
        """
        getNumErrors(SedDocument self) -> unsigned int
        getNumErrors(SedDocument self, unsigned int severity) -> unsigned int
        """
        return _libsedml.SedDocument_getNumErrors(self, *args)


_libsedml.SedDocument_swigregister(SedDocument)

class SedErrorLog(XMLErrorLog):
    """Proxy of C++ SedErrorLog class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getError(self, n):
        """getError(SedErrorLog self, unsigned int n) -> SedError"""
        return _libsedml.SedErrorLog_getError(self, n)

    def getErrorWithSeverity(self, n, severity):
        """getErrorWithSeverity(SedErrorLog self, unsigned int n, unsigned int severity) -> SedError"""
        return _libsedml.SedErrorLog_getErrorWithSeverity(self, n, severity)

    def getNumFailsWithSeverity(self, *args):
        """
        getNumFailsWithSeverity(SedErrorLog self, unsigned int severity) -> unsigned int
        getNumFailsWithSeverity(SedErrorLog self, unsigned int severity) -> unsigned int
        """
        return _libsedml.SedErrorLog_getNumFailsWithSeverity(self, *args)

    def __init__(self, *args):
        """
        __init__(SedErrorLog self) -> SedErrorLog
        __init__(SedErrorLog self, SedErrorLog other) -> SedErrorLog
        """
        _libsedml.SedErrorLog_swiginit(self, _libsedml.new_SedErrorLog(*args))

    __swig_destroy__ = _libsedml.delete_SedErrorLog

    def logError(self, *args):
        """logError(SedErrorLog self, unsigned int const errorId=0, unsigned int const level=SEDML_DEFAULT_LEVEL, unsigned int const version=SEDML_DEFAULT_VERSION, string details="", unsigned int const line=0, unsigned int const column=0, unsigned int const severity=LIBSEDML_SEV_ERROR, unsigned int const category=LIBSEDML_CAT_SEDML)"""
        return _libsedml.SedErrorLog_logError(self, *args)

    def add(self, error):
        """add(SedErrorLog self, SedError error)"""
        return _libsedml.SedErrorLog_add(self, error)

    def remove(self, errorId):
        """remove(SedErrorLog self, unsigned int const errorId)"""
        return _libsedml.SedErrorLog_remove(self, errorId)

    def removeAll(self, errorId):
        """removeAll(SedErrorLog self, unsigned int const errorId)"""
        return _libsedml.SedErrorLog_removeAll(self, errorId)

    def contains(self, errorId):
        """contains(SedErrorLog self, unsigned int const errorId) -> bool"""
        return _libsedml.SedErrorLog_contains(self, errorId)


_libsedml.SedErrorLog_swigregister(SedErrorLog)
SedUnknown = _libsedml.SedUnknown
SedNotUTF8 = _libsedml.SedNotUTF8
SedUnrecognizedElement = _libsedml.SedUnrecognizedElement
SedNotSchemaConformant = _libsedml.SedNotSchemaConformant
SedInvalidMathElement = _libsedml.SedInvalidMathElement
SedMissingAnnotationNamespace = _libsedml.SedMissingAnnotationNamespace
SedDuplicateAnnotationNamespaces = _libsedml.SedDuplicateAnnotationNamespaces
SedNamespaceInAnnotation = _libsedml.SedNamespaceInAnnotation
SedMultipleAnnotations = _libsedml.SedMultipleAnnotations
SedAnnotationNotElement = _libsedml.SedAnnotationNotElement
SedNotesNotInXHTMLNamespace = _libsedml.SedNotesNotInXHTMLNamespace
SedNotesContainsXMLDecl = _libsedml.SedNotesContainsXMLDecl
SedNotesContainsDOCTYPE = _libsedml.SedNotesContainsDOCTYPE
SedInvalidNotesContent = _libsedml.SedInvalidNotesContent
SedOnlyOneNotesElementAllowed = _libsedml.SedOnlyOneNotesElementAllowed
SedmlNSUndeclared = _libsedml.SedmlNSUndeclared
SedmlElementNotInNs = _libsedml.SedmlElementNotInNs
SedmlDuplicateComponentId = _libsedml.SedmlDuplicateComponentId
SedmlIdSyntaxRule = _libsedml.SedmlIdSyntaxRule
SedInvalidMetaidSyntax = _libsedml.SedInvalidMetaidSyntax
InvalidNamespaceOnSed = _libsedml.InvalidNamespaceOnSed
AllowedAttributes = _libsedml.AllowedAttributes
SedEmptyListElement = _libsedml.SedEmptyListElement
SedmlDocumentAllowedCoreAttributes = _libsedml.SedmlDocumentAllowedCoreAttributes
SedmlDocumentAllowedCoreElements = _libsedml.SedmlDocumentAllowedCoreElements
SedmlDocumentAllowedAttributes = _libsedml.SedmlDocumentAllowedAttributes
SedmlDocumentAllowedElements = _libsedml.SedmlDocumentAllowedElements
SedmlDocumentLevelMustBeNonNegativeInteger = _libsedml.SedmlDocumentLevelMustBeNonNegativeInteger
SedmlDocumentVersionMustBeNonNegativeInteger = _libsedml.SedmlDocumentVersionMustBeNonNegativeInteger
SedmlDocumentLODataDescriptionsAllowedCoreElements = _libsedml.SedmlDocumentLODataDescriptionsAllowedCoreElements
SedmlDocumentLOModelsAllowedCoreElements = _libsedml.SedmlDocumentLOModelsAllowedCoreElements
SedmlDocumentLOSimulationsAllowedCoreElements = _libsedml.SedmlDocumentLOSimulationsAllowedCoreElements
SedmlDocumentLOTasksAllowedCoreElements = _libsedml.SedmlDocumentLOTasksAllowedCoreElements
SedmlDocumentLODataGeneratorsAllowedCoreElements = _libsedml.SedmlDocumentLODataGeneratorsAllowedCoreElements
SedmlDocumentLOOutputsAllowedCoreElements = _libsedml.SedmlDocumentLOOutputsAllowedCoreElements
SedmlDocumentLOStylesAllowedCoreElements = _libsedml.SedmlDocumentLOStylesAllowedCoreElements
SedmlDocumentLODataDescriptionsAllowedCoreAttributes = _libsedml.SedmlDocumentLODataDescriptionsAllowedCoreAttributes
SedmlDocumentLOModelsAllowedCoreAttributes = _libsedml.SedmlDocumentLOModelsAllowedCoreAttributes
SedmlDocumentLOSimulationsAllowedCoreAttributes = _libsedml.SedmlDocumentLOSimulationsAllowedCoreAttributes
SedmlDocumentLOTasksAllowedCoreAttributes = _libsedml.SedmlDocumentLOTasksAllowedCoreAttributes
SedmlDocumentLODataGeneratorsAllowedCoreAttributes = _libsedml.SedmlDocumentLODataGeneratorsAllowedCoreAttributes
SedmlDocumentLOOutputsAllowedCoreAttributes = _libsedml.SedmlDocumentLOOutputsAllowedCoreAttributes
SedmlDocumentLOStylesAllowedCoreAttributes = _libsedml.SedmlDocumentLOStylesAllowedCoreAttributes
SedmlModelAllowedCoreAttributes = _libsedml.SedmlModelAllowedCoreAttributes
SedmlModelAllowedCoreElements = _libsedml.SedmlModelAllowedCoreElements
SedmlModelAllowedAttributes = _libsedml.SedmlModelAllowedAttributes
SedmlModelAllowedElements = _libsedml.SedmlModelAllowedElements
SedmlModelSourceMustBeString = _libsedml.SedmlModelSourceMustBeString
SedmlModelNameMustBeString = _libsedml.SedmlModelNameMustBeString
SedmlModelLanguageMustBeString = _libsedml.SedmlModelLanguageMustBeString
SedmlModelLOChangesAllowedCoreElements = _libsedml.SedmlModelLOChangesAllowedCoreElements
SedmlModelLOChangesAllowedCoreAttributes = _libsedml.SedmlModelLOChangesAllowedCoreAttributes
SedmlChangeAllowedCoreAttributes = _libsedml.SedmlChangeAllowedCoreAttributes
SedmlChangeAllowedCoreElements = _libsedml.SedmlChangeAllowedCoreElements
SedmlChangeAllowedAttributes = _libsedml.SedmlChangeAllowedAttributes
SedmlChangeTargetMustBeString = _libsedml.SedmlChangeTargetMustBeString
SedmlAddXMLAllowedCoreAttributes = _libsedml.SedmlAddXMLAllowedCoreAttributes
SedmlAddXMLAllowedCoreElements = _libsedml.SedmlAddXMLAllowedCoreElements
SedmlAddXMLAllowedElements = _libsedml.SedmlAddXMLAllowedElements
SedmlChangeAttributeAllowedCoreAttributes = _libsedml.SedmlChangeAttributeAllowedCoreAttributes
SedmlChangeAttributeAllowedCoreElements = _libsedml.SedmlChangeAttributeAllowedCoreElements
SedmlChangeAttributeAllowedAttributes = _libsedml.SedmlChangeAttributeAllowedAttributes
SedmlChangeAttributeNewValueMustBeString = _libsedml.SedmlChangeAttributeNewValueMustBeString
SedmlVariableAllowedCoreAttributes = _libsedml.SedmlVariableAllowedCoreAttributes
SedmlVariableAllowedCoreElements = _libsedml.SedmlVariableAllowedCoreElements
SedmlVariableAllowedAttributes = _libsedml.SedmlVariableAllowedAttributes
SedmlVariableAllowedElements = _libsedml.SedmlVariableAllowedElements
SedmlVariableNameMustBeString = _libsedml.SedmlVariableNameMustBeString
SedmlVariableSymbolMustBeString = _libsedml.SedmlVariableSymbolMustBeString
SedmlVariableTargetMustBeString = _libsedml.SedmlVariableTargetMustBeString
SedmlVariableTaskReferenceMustBeTask = _libsedml.SedmlVariableTaskReferenceMustBeTask
SedmlVariableModelReferenceMustBeModel = _libsedml.SedmlVariableModelReferenceMustBeModel
SedmlVariableLORemainingDimensionsAllowedCoreElements = _libsedml.SedmlVariableLORemainingDimensionsAllowedCoreElements
SedmlVariableLORemainingDimensionsAllowedCoreAttributes = _libsedml.SedmlVariableLORemainingDimensionsAllowedCoreAttributes
SedmlParameterAllowedCoreAttributes = _libsedml.SedmlParameterAllowedCoreAttributes
SedmlParameterAllowedCoreElements = _libsedml.SedmlParameterAllowedCoreElements
SedmlParameterAllowedAttributes = _libsedml.SedmlParameterAllowedAttributes
SedmlParameterValueMustBeDouble = _libsedml.SedmlParameterValueMustBeDouble
SedmlParameterNameMustBeString = _libsedml.SedmlParameterNameMustBeString
SedmlSimulationAllowedCoreAttributes = _libsedml.SedmlSimulationAllowedCoreAttributes
SedmlSimulationAllowedCoreElements = _libsedml.SedmlSimulationAllowedCoreElements
SedmlSimulationAllowedAttributes = _libsedml.SedmlSimulationAllowedAttributes
SedmlSimulationAllowedElements = _libsedml.SedmlSimulationAllowedElements
SedmlSimulationNameMustBeString = _libsedml.SedmlSimulationNameMustBeString
SedmlUniformTimeCourseAllowedCoreAttributes = _libsedml.SedmlUniformTimeCourseAllowedCoreAttributes
SedmlUniformTimeCourseAllowedCoreElements = _libsedml.SedmlUniformTimeCourseAllowedCoreElements
SedmlUniformTimeCourseAllowedAttributes = _libsedml.SedmlUniformTimeCourseAllowedAttributes
SedmlUniformTimeCourseInitialTimeMustBeDouble = _libsedml.SedmlUniformTimeCourseInitialTimeMustBeDouble
SedmlUniformTimeCourseOutputStartTimeMustBeDouble = _libsedml.SedmlUniformTimeCourseOutputStartTimeMustBeDouble
SedmlUniformTimeCourseOutputEndTimeMustBeDouble = _libsedml.SedmlUniformTimeCourseOutputEndTimeMustBeDouble
SedmlUniformTimeCourseNumberOfPointsMustBeInteger = _libsedml.SedmlUniformTimeCourseNumberOfPointsMustBeInteger
SedmlUniformTimeCourseNumberOfStepsMustBeInteger = _libsedml.SedmlUniformTimeCourseNumberOfStepsMustBeInteger
SedmlAlgorithmAllowedCoreAttributes = _libsedml.SedmlAlgorithmAllowedCoreAttributes
SedmlAlgorithmAllowedCoreElements = _libsedml.SedmlAlgorithmAllowedCoreElements
SedmlAlgorithmAllowedAttributes = _libsedml.SedmlAlgorithmAllowedAttributes
SedmlAlgorithmAllowedElements = _libsedml.SedmlAlgorithmAllowedElements
SedmlAlgorithmKisaoIDMustBeString = _libsedml.SedmlAlgorithmKisaoIDMustBeString
SedmlAlgorithmLOAlgorithmParametersAllowedCoreElements = _libsedml.SedmlAlgorithmLOAlgorithmParametersAllowedCoreElements
SedmlAlgorithmLOAlgorithmParametersAllowedCoreAttributes = _libsedml.SedmlAlgorithmLOAlgorithmParametersAllowedCoreAttributes
SedmlAbstractTaskAllowedCoreAttributes = _libsedml.SedmlAbstractTaskAllowedCoreAttributes
SedmlAbstractTaskAllowedCoreElements = _libsedml.SedmlAbstractTaskAllowedCoreElements
SedmlAbstractTaskAllowedAttributes = _libsedml.SedmlAbstractTaskAllowedAttributes
SedmlAbstractTaskNameMustBeString = _libsedml.SedmlAbstractTaskNameMustBeString
SedmlTaskAllowedCoreAttributes = _libsedml.SedmlTaskAllowedCoreAttributes
SedmlTaskAllowedCoreElements = _libsedml.SedmlTaskAllowedCoreElements
SedmlTaskAllowedAttributes = _libsedml.SedmlTaskAllowedAttributes
SedmlTaskModelReferenceMustBeModel = _libsedml.SedmlTaskModelReferenceMustBeModel
SedmlTaskSimulationReferenceMustBeSimulation = _libsedml.SedmlTaskSimulationReferenceMustBeSimulation
SedmlDataGeneratorAllowedCoreAttributes = _libsedml.SedmlDataGeneratorAllowedCoreAttributes
SedmlDataGeneratorAllowedCoreElements = _libsedml.SedmlDataGeneratorAllowedCoreElements
SedmlDataGeneratorAllowedAttributes = _libsedml.SedmlDataGeneratorAllowedAttributes
SedmlDataGeneratorAllowedElements = _libsedml.SedmlDataGeneratorAllowedElements
SedmlDataGeneratorNameMustBeString = _libsedml.SedmlDataGeneratorNameMustBeString
SedmlDataGeneratorLOVariablesAllowedCoreElements = _libsedml.SedmlDataGeneratorLOVariablesAllowedCoreElements
SedmlDataGeneratorLOParametersAllowedCoreElements = _libsedml.SedmlDataGeneratorLOParametersAllowedCoreElements
SedmlDataGeneratorLOVariablesAllowedCoreAttributes = _libsedml.SedmlDataGeneratorLOVariablesAllowedCoreAttributes
SedmlDataGeneratorLOParametersAllowedCoreAttributes = _libsedml.SedmlDataGeneratorLOParametersAllowedCoreAttributes
SedmlOutputAllowedCoreAttributes = _libsedml.SedmlOutputAllowedCoreAttributes
SedmlOutputAllowedCoreElements = _libsedml.SedmlOutputAllowedCoreElements
SedmlOutputAllowedAttributes = _libsedml.SedmlOutputAllowedAttributes
SedmlOutputNameMustBeString = _libsedml.SedmlOutputNameMustBeString
SedmlPlotAllowedCoreAttributes = _libsedml.SedmlPlotAllowedCoreAttributes
SedmlPlotAllowedCoreElements = _libsedml.SedmlPlotAllowedCoreElements
SedmlPlotAllowedAttributes = _libsedml.SedmlPlotAllowedAttributes
SedmlPlotAllowedElements = _libsedml.SedmlPlotAllowedElements
SedmlPlotLegendMustBeBoolean = _libsedml.SedmlPlotLegendMustBeBoolean
SedmlPlotHeightMustBeDouble = _libsedml.SedmlPlotHeightMustBeDouble
SedmlPlotWidthMustBeDouble = _libsedml.SedmlPlotWidthMustBeDouble
SedmlPlot2DAllowedCoreAttributes = _libsedml.SedmlPlot2DAllowedCoreAttributes
SedmlPlot2DAllowedCoreElements = _libsedml.SedmlPlot2DAllowedCoreElements
SedmlPlot2DAllowedElements = _libsedml.SedmlPlot2DAllowedElements
SedmlPlot2DLOCurvesAllowedCoreElements = _libsedml.SedmlPlot2DLOCurvesAllowedCoreElements
SedmlPlot2DLOCurvesAllowedCoreAttributes = _libsedml.SedmlPlot2DLOCurvesAllowedCoreAttributes
SedmlPlot3DAllowedCoreAttributes = _libsedml.SedmlPlot3DAllowedCoreAttributes
SedmlPlot3DAllowedCoreElements = _libsedml.SedmlPlot3DAllowedCoreElements
SedmlPlot3DAllowedElements = _libsedml.SedmlPlot3DAllowedElements
SedmlPlot3DLOSurfacesAllowedCoreElements = _libsedml.SedmlPlot3DLOSurfacesAllowedCoreElements
SedmlPlot3DLOSurfacesAllowedCoreAttributes = _libsedml.SedmlPlot3DLOSurfacesAllowedCoreAttributes
SedmlAbstractCurveAllowedCoreAttributes = _libsedml.SedmlAbstractCurveAllowedCoreAttributes
SedmlAbstractCurveAllowedCoreElements = _libsedml.SedmlAbstractCurveAllowedCoreElements
SedmlAbstractCurveAllowedAttributes = _libsedml.SedmlAbstractCurveAllowedAttributes
SedmlAbstractCurveNameMustBeString = _libsedml.SedmlAbstractCurveNameMustBeString
SedmlAbstractCurveLogXMustBeBoolean = _libsedml.SedmlAbstractCurveLogXMustBeBoolean
SedmlAbstractCurveOrderMustBeInteger = _libsedml.SedmlAbstractCurveOrderMustBeInteger
SedmlAbstractCurveStyleMustBeStyle = _libsedml.SedmlAbstractCurveStyleMustBeStyle
SedmlAbstractCurveYAxisMustBeString = _libsedml.SedmlAbstractCurveYAxisMustBeString
SedmlAbstractCurveXDataReferenceMustBeDataReference = _libsedml.SedmlAbstractCurveXDataReferenceMustBeDataReference
SedmlCurveAllowedCoreAttributes = _libsedml.SedmlCurveAllowedCoreAttributes
SedmlCurveAllowedCoreElements = _libsedml.SedmlCurveAllowedCoreElements
SedmlCurveAllowedAttributes = _libsedml.SedmlCurveAllowedAttributes
SedmlCurveYDataReferenceMustBeDataGenerator = _libsedml.SedmlCurveYDataReferenceMustBeDataGenerator
SedmlCurveLogYMustBeBoolean = _libsedml.SedmlCurveLogYMustBeBoolean
SedmlCurveTypeMustBeCurveTypeEnum = _libsedml.SedmlCurveTypeMustBeCurveTypeEnum
SedmlCurveXErrorUpperMustBeDataGenerator = _libsedml.SedmlCurveXErrorUpperMustBeDataGenerator
SedmlCurveXErrorLowerMustBeDataGenerator = _libsedml.SedmlCurveXErrorLowerMustBeDataGenerator
SedmlCurveYErrorUpperMustBeDataGenerator = _libsedml.SedmlCurveYErrorUpperMustBeDataGenerator
SedmlCurveYErrorLowerMustBeDataGenerator = _libsedml.SedmlCurveYErrorLowerMustBeDataGenerator
SedmlSurfaceAllowedCoreAttributes = _libsedml.SedmlSurfaceAllowedCoreAttributes
SedmlSurfaceAllowedCoreElements = _libsedml.SedmlSurfaceAllowedCoreElements
SedmlSurfaceAllowedAttributes = _libsedml.SedmlSurfaceAllowedAttributes
SedmlSurfaceZDataReferenceMustBeDataGenerator = _libsedml.SedmlSurfaceZDataReferenceMustBeDataGenerator
SedmlSurfaceNameMustBeString = _libsedml.SedmlSurfaceNameMustBeString
SedmlSurfaceXDataReferenceMustBeDataGenerator = _libsedml.SedmlSurfaceXDataReferenceMustBeDataGenerator
SedmlSurfaceYDataReferenceMustBeDataGenerator = _libsedml.SedmlSurfaceYDataReferenceMustBeDataGenerator
SedmlSurfaceTypeMustBeSurfaceTypeEnum = _libsedml.SedmlSurfaceTypeMustBeSurfaceTypeEnum
SedmlSurfaceStyleMustBeStyle = _libsedml.SedmlSurfaceStyleMustBeStyle
SedmlSurfaceLogXMustBeBoolean = _libsedml.SedmlSurfaceLogXMustBeBoolean
SedmlSurfaceLogYMustBeBoolean = _libsedml.SedmlSurfaceLogYMustBeBoolean
SedmlSurfaceLogZMustBeBoolean = _libsedml.SedmlSurfaceLogZMustBeBoolean
SedmlSurfaceOrderMustBeInteger = _libsedml.SedmlSurfaceOrderMustBeInteger
SedmlDataSetAllowedCoreAttributes = _libsedml.SedmlDataSetAllowedCoreAttributes
SedmlDataSetAllowedCoreElements = _libsedml.SedmlDataSetAllowedCoreElements
SedmlDataSetAllowedAttributes = _libsedml.SedmlDataSetAllowedAttributes
SedmlDataSetLabelMustBeString = _libsedml.SedmlDataSetLabelMustBeString
SedmlDataSetDataReferenceMustBeDataGenerator = _libsedml.SedmlDataSetDataReferenceMustBeDataGenerator
SedmlDataSetNameMustBeString = _libsedml.SedmlDataSetNameMustBeString
SedmlReportAllowedCoreAttributes = _libsedml.SedmlReportAllowedCoreAttributes
SedmlReportAllowedCoreElements = _libsedml.SedmlReportAllowedCoreElements
SedmlReportAllowedElements = _libsedml.SedmlReportAllowedElements
SedmlReportLODataSetsAllowedCoreElements = _libsedml.SedmlReportLODataSetsAllowedCoreElements
SedmlReportLODataSetsAllowedCoreAttributes = _libsedml.SedmlReportLODataSetsAllowedCoreAttributes
SedmlAlgorithmParameterAllowedCoreAttributes = _libsedml.SedmlAlgorithmParameterAllowedCoreAttributes
SedmlAlgorithmParameterAllowedCoreElements = _libsedml.SedmlAlgorithmParameterAllowedCoreElements
SedmlAlgorithmParameterAllowedAttributes = _libsedml.SedmlAlgorithmParameterAllowedAttributes
SedmlAlgorithmParameterAllowedElements = _libsedml.SedmlAlgorithmParameterAllowedElements
SedmlAlgorithmParameterKisaoIDMustBeString = _libsedml.SedmlAlgorithmParameterKisaoIDMustBeString
SedmlAlgorithmParameterValueMustBeString = _libsedml.SedmlAlgorithmParameterValueMustBeString
SedmlAlgorithmParameterLOAlgorithmParametersAllowedCoreElements = _libsedml.SedmlAlgorithmParameterLOAlgorithmParametersAllowedCoreElements
SedmlAlgorithmParameterLOAlgorithmParametersAllowedCoreAttributes = _libsedml.SedmlAlgorithmParameterLOAlgorithmParametersAllowedCoreAttributes
SedmlRangeAllowedCoreAttributes = _libsedml.SedmlRangeAllowedCoreAttributes
SedmlRangeAllowedCoreElements = _libsedml.SedmlRangeAllowedCoreElements
SedmlRangeAllowedAttributes = _libsedml.SedmlRangeAllowedAttributes
SedmlChangeXMLAllowedCoreAttributes = _libsedml.SedmlChangeXMLAllowedCoreAttributes
SedmlChangeXMLAllowedCoreElements = _libsedml.SedmlChangeXMLAllowedCoreElements
SedmlChangeXMLAllowedElements = _libsedml.SedmlChangeXMLAllowedElements
SedmlRemoveXMLAllowedCoreAttributes = _libsedml.SedmlRemoveXMLAllowedCoreAttributes
SedmlRemoveXMLAllowedCoreElements = _libsedml.SedmlRemoveXMLAllowedCoreElements
SedmlSetValueAllowedCoreAttributes = _libsedml.SedmlSetValueAllowedCoreAttributes
SedmlSetValueAllowedCoreElements = _libsedml.SedmlSetValueAllowedCoreElements
SedmlSetValueAllowedAttributes = _libsedml.SedmlSetValueAllowedAttributes
SedmlSetValueAllowedElements = _libsedml.SedmlSetValueAllowedElements
SedmlSetValueModelReferenceMustBeModel = _libsedml.SedmlSetValueModelReferenceMustBeModel
SedmlSetValueSymbolMustBeString = _libsedml.SedmlSetValueSymbolMustBeString
SedmlSetValueTargetMustBeString = _libsedml.SedmlSetValueTargetMustBeString
SedmlSetValueRangeMustBeRange = _libsedml.SedmlSetValueRangeMustBeRange
SedmlUniformRangeAllowedCoreAttributes = _libsedml.SedmlUniformRangeAllowedCoreAttributes
SedmlUniformRangeAllowedCoreElements = _libsedml.SedmlUniformRangeAllowedCoreElements
SedmlUniformRangeAllowedAttributes = _libsedml.SedmlUniformRangeAllowedAttributes
SedmlUniformRangeStartMustBeDouble = _libsedml.SedmlUniformRangeStartMustBeDouble
SedmlUniformRangeEndMustBeDouble = _libsedml.SedmlUniformRangeEndMustBeDouble
SedmlUniformRangeNumberOfPointsMustBeInteger = _libsedml.SedmlUniformRangeNumberOfPointsMustBeInteger
SedmlUniformRangeTypeMustBeString = _libsedml.SedmlUniformRangeTypeMustBeString
SedmlVectorRangeAllowedCoreAttributes = _libsedml.SedmlVectorRangeAllowedCoreAttributes
SedmlVectorRangeAllowedCoreElements = _libsedml.SedmlVectorRangeAllowedCoreElements
SedmlVectorRangeAllowedAttributes = _libsedml.SedmlVectorRangeAllowedAttributes
SedmlVectorRangeValueMustBeString = _libsedml.SedmlVectorRangeValueMustBeString
SedmlFunctionalRangeAllowedCoreAttributes = _libsedml.SedmlFunctionalRangeAllowedCoreAttributes
SedmlFunctionalRangeAllowedCoreElements = _libsedml.SedmlFunctionalRangeAllowedCoreElements
SedmlFunctionalRangeAllowedAttributes = _libsedml.SedmlFunctionalRangeAllowedAttributes
SedmlFunctionalRangeAllowedElements = _libsedml.SedmlFunctionalRangeAllowedElements
SedmlFunctionalRangeRangeMustBeRange = _libsedml.SedmlFunctionalRangeRangeMustBeRange
SedmlFunctionalRangeLOVariablesAllowedCoreElements = _libsedml.SedmlFunctionalRangeLOVariablesAllowedCoreElements
SedmlFunctionalRangeLOParametersAllowedCoreElements = _libsedml.SedmlFunctionalRangeLOParametersAllowedCoreElements
SedmlFunctionalRangeLOVariablesAllowedCoreAttributes = _libsedml.SedmlFunctionalRangeLOVariablesAllowedCoreAttributes
SedmlFunctionalRangeLOParametersAllowedCoreAttributes = _libsedml.SedmlFunctionalRangeLOParametersAllowedCoreAttributes
SedmlSubTaskAllowedCoreAttributes = _libsedml.SedmlSubTaskAllowedCoreAttributes
SedmlSubTaskAllowedCoreElements = _libsedml.SedmlSubTaskAllowedCoreElements
SedmlSubTaskAllowedAttributes = _libsedml.SedmlSubTaskAllowedAttributes
SedmlSubTaskOrderMustBeInteger = _libsedml.SedmlSubTaskOrderMustBeInteger
SedmlSubTaskTaskMustBeAbstractTask = _libsedml.SedmlSubTaskTaskMustBeAbstractTask
SedmlOneStepAllowedCoreAttributes = _libsedml.SedmlOneStepAllowedCoreAttributes
SedmlOneStepAllowedCoreElements = _libsedml.SedmlOneStepAllowedCoreElements
SedmlOneStepAllowedAttributes = _libsedml.SedmlOneStepAllowedAttributes
SedmlOneStepStepMustBeDouble = _libsedml.SedmlOneStepStepMustBeDouble
SedmlSteadyStateAllowedCoreAttributes = _libsedml.SedmlSteadyStateAllowedCoreAttributes
SedmlSteadyStateAllowedCoreElements = _libsedml.SedmlSteadyStateAllowedCoreElements
SedmlRepeatedTaskAllowedCoreAttributes = _libsedml.SedmlRepeatedTaskAllowedCoreAttributes
SedmlRepeatedTaskAllowedCoreElements = _libsedml.SedmlRepeatedTaskAllowedCoreElements
SedmlRepeatedTaskAllowedAttributes = _libsedml.SedmlRepeatedTaskAllowedAttributes
SedmlRepeatedTaskAllowedElements = _libsedml.SedmlRepeatedTaskAllowedElements
SedmlRepeatedTaskRangeIdMustBeRange = _libsedml.SedmlRepeatedTaskRangeIdMustBeRange
SedmlRepeatedTaskResetModelMustBeBoolean = _libsedml.SedmlRepeatedTaskResetModelMustBeBoolean
SedmlRepeatedTaskLORangesAllowedCoreElements = _libsedml.SedmlRepeatedTaskLORangesAllowedCoreElements
SedmlRepeatedTaskLOSetValuesAllowedCoreElements = _libsedml.SedmlRepeatedTaskLOSetValuesAllowedCoreElements
SedmlRepeatedTaskLOSubTasksAllowedCoreElements = _libsedml.SedmlRepeatedTaskLOSubTasksAllowedCoreElements
SedmlRepeatedTaskLORangesAllowedCoreAttributes = _libsedml.SedmlRepeatedTaskLORangesAllowedCoreAttributes
SedmlRepeatedTaskLOSetValuesAllowedCoreAttributes = _libsedml.SedmlRepeatedTaskLOSetValuesAllowedCoreAttributes
SedmlRepeatedTaskLOSubTasksAllowedCoreAttributes = _libsedml.SedmlRepeatedTaskLOSubTasksAllowedCoreAttributes
SedmlComputeChangeAllowedCoreAttributes = _libsedml.SedmlComputeChangeAllowedCoreAttributes
SedmlComputeChangeAllowedCoreElements = _libsedml.SedmlComputeChangeAllowedCoreElements
SedmlComputeChangeAllowedElements = _libsedml.SedmlComputeChangeAllowedElements
SedmlComputeChangeLOVariablesAllowedCoreElements = _libsedml.SedmlComputeChangeLOVariablesAllowedCoreElements
SedmlComputeChangeLOParametersAllowedCoreElements = _libsedml.SedmlComputeChangeLOParametersAllowedCoreElements
SedmlComputeChangeLOVariablesAllowedCoreAttributes = _libsedml.SedmlComputeChangeLOVariablesAllowedCoreAttributes
SedmlComputeChangeLOParametersAllowedCoreAttributes = _libsedml.SedmlComputeChangeLOParametersAllowedCoreAttributes
SedmlDataDescriptionAllowedCoreAttributes = _libsedml.SedmlDataDescriptionAllowedCoreAttributes
SedmlDataDescriptionAllowedCoreElements = _libsedml.SedmlDataDescriptionAllowedCoreElements
SedmlDataDescriptionAllowedAttributes = _libsedml.SedmlDataDescriptionAllowedAttributes
SedmlDataDescriptionAllowedElements = _libsedml.SedmlDataDescriptionAllowedElements
SedmlDataDescriptionNameMustBeString = _libsedml.SedmlDataDescriptionNameMustBeString
SedmlDataDescriptionFormatMustBeString = _libsedml.SedmlDataDescriptionFormatMustBeString
SedmlDataDescriptionSourceMustBeString = _libsedml.SedmlDataDescriptionSourceMustBeString
SedmlDataDescriptionLODataSourcesAllowedCoreElements = _libsedml.SedmlDataDescriptionLODataSourcesAllowedCoreElements
SedmlDataDescriptionLODataSourcesAllowedCoreAttributes = _libsedml.SedmlDataDescriptionLODataSourcesAllowedCoreAttributes
SedmlDataSourceAllowedCoreAttributes = _libsedml.SedmlDataSourceAllowedCoreAttributes
SedmlDataSourceAllowedCoreElements = _libsedml.SedmlDataSourceAllowedCoreElements
SedmlDataSourceAllowedAttributes = _libsedml.SedmlDataSourceAllowedAttributes
SedmlDataSourceAllowedElements = _libsedml.SedmlDataSourceAllowedElements
SedmlDataSourceNameMustBeString = _libsedml.SedmlDataSourceNameMustBeString
SedmlDataSourceIndexSetMustBeSId = _libsedml.SedmlDataSourceIndexSetMustBeSId
SedmlDataSourceLOSlicesAllowedCoreElements = _libsedml.SedmlDataSourceLOSlicesAllowedCoreElements
SedmlDataSourceLOSlicesAllowedCoreAttributes = _libsedml.SedmlDataSourceLOSlicesAllowedCoreAttributes
SedmlSliceAllowedCoreAttributes = _libsedml.SedmlSliceAllowedCoreAttributes
SedmlSliceAllowedCoreElements = _libsedml.SedmlSliceAllowedCoreElements
SedmlSliceAllowedAttributes = _libsedml.SedmlSliceAllowedAttributes
SedmlSliceReferenceMustBeSId = _libsedml.SedmlSliceReferenceMustBeSId
SedmlSliceValueMustBeString = _libsedml.SedmlSliceValueMustBeString
SedmlSliceIndexMustBeSId = _libsedml.SedmlSliceIndexMustBeSId
SedmlSliceStartIndexMustBeInteger = _libsedml.SedmlSliceStartIndexMustBeInteger
SedmlSliceEndIndexMustBeInteger = _libsedml.SedmlSliceEndIndexMustBeInteger
SedmlParameterEstimationTaskAllowedCoreAttributes = _libsedml.SedmlParameterEstimationTaskAllowedCoreAttributes
SedmlParameterEstimationTaskAllowedCoreElements = _libsedml.SedmlParameterEstimationTaskAllowedCoreElements
SedmlParameterEstimationTaskAllowedElements = _libsedml.SedmlParameterEstimationTaskAllowedElements
SedmlParameterEstimationTaskLOAdjustableParametersAllowedCoreElements = _libsedml.SedmlParameterEstimationTaskLOAdjustableParametersAllowedCoreElements
SedmlParameterEstimationTaskLOFitExperimentsAllowedCoreElements = _libsedml.SedmlParameterEstimationTaskLOFitExperimentsAllowedCoreElements
SedmlParameterEstimationTaskLOAdjustableParametersAllowedCoreAttributes = _libsedml.SedmlParameterEstimationTaskLOAdjustableParametersAllowedCoreAttributes
SedmlParameterEstimationTaskLOFitExperimentsAllowedCoreAttributes = _libsedml.SedmlParameterEstimationTaskLOFitExperimentsAllowedCoreAttributes
SedmlObjectiveAllowedCoreAttributes = _libsedml.SedmlObjectiveAllowedCoreAttributes
SedmlObjectiveAllowedCoreElements = _libsedml.SedmlObjectiveAllowedCoreElements
SedmlLeastSquareObjectiveFunctionAllowedCoreAttributes = _libsedml.SedmlLeastSquareObjectiveFunctionAllowedCoreAttributes
SedmlLeastSquareObjectiveFunctionAllowedCoreElements = _libsedml.SedmlLeastSquareObjectiveFunctionAllowedCoreElements
SedmlAdjustableParameterAllowedCoreAttributes = _libsedml.SedmlAdjustableParameterAllowedCoreAttributes
SedmlAdjustableParameterAllowedCoreElements = _libsedml.SedmlAdjustableParameterAllowedCoreElements
SedmlAdjustableParameterAllowedAttributes = _libsedml.SedmlAdjustableParameterAllowedAttributes
SedmlAdjustableParameterAllowedElements = _libsedml.SedmlAdjustableParameterAllowedElements
SedmlAdjustableParameterInitialValueMustBeDouble = _libsedml.SedmlAdjustableParameterInitialValueMustBeDouble
SedmlAdjustableParameterModelReferenceMustBeModel = _libsedml.SedmlAdjustableParameterModelReferenceMustBeModel
SedmlAdjustableParameterTargetMustBeString = _libsedml.SedmlAdjustableParameterTargetMustBeString
SedmlAdjustableParameterLOExperimentRefsAllowedCoreElements = _libsedml.SedmlAdjustableParameterLOExperimentRefsAllowedCoreElements
SedmlAdjustableParameterLOExperimentRefsAllowedCoreAttributes = _libsedml.SedmlAdjustableParameterLOExperimentRefsAllowedCoreAttributes
SedmlExperimentRefAllowedCoreAttributes = _libsedml.SedmlExperimentRefAllowedCoreAttributes
SedmlExperimentRefAllowedCoreElements = _libsedml.SedmlExperimentRefAllowedCoreElements
SedmlExperimentRefAllowedAttributes = _libsedml.SedmlExperimentRefAllowedAttributes
SedmlExperimentRefExperimentIdMustBeFitExperiment = _libsedml.SedmlExperimentRefExperimentIdMustBeFitExperiment
SedmlFitExperimentAllowedCoreAttributes = _libsedml.SedmlFitExperimentAllowedCoreAttributes
SedmlFitExperimentAllowedCoreElements = _libsedml.SedmlFitExperimentAllowedCoreElements
SedmlFitExperimentAllowedAttributes = _libsedml.SedmlFitExperimentAllowedAttributes
SedmlFitExperimentAllowedElements = _libsedml.SedmlFitExperimentAllowedElements
SedmlFitExperimentTypeMustBeExperimentTypeEnum = _libsedml.SedmlFitExperimentTypeMustBeExperimentTypeEnum
SedmlFitExperimentLOFitMappingsAllowedCoreElements = _libsedml.SedmlFitExperimentLOFitMappingsAllowedCoreElements
SedmlFitExperimentLOFitMappingsAllowedCoreAttributes = _libsedml.SedmlFitExperimentLOFitMappingsAllowedCoreAttributes
SedmlFitMappingAllowedCoreAttributes = _libsedml.SedmlFitMappingAllowedCoreAttributes
SedmlFitMappingAllowedCoreElements = _libsedml.SedmlFitMappingAllowedCoreElements
SedmlFitMappingAllowedAttributes = _libsedml.SedmlFitMappingAllowedAttributes
SedmlFitMappingDataSourceMustBeDataSource = _libsedml.SedmlFitMappingDataSourceMustBeDataSource
SedmlFitMappingTargetMustBeDataGenerator = _libsedml.SedmlFitMappingTargetMustBeDataGenerator
SedmlFitMappingTypeMustBeMappingTypeEnum = _libsedml.SedmlFitMappingTypeMustBeMappingTypeEnum
SedmlFitMappingWeightMustBeDouble = _libsedml.SedmlFitMappingWeightMustBeDouble
SedmlFitMappingPointWeightMustBeDataSource = _libsedml.SedmlFitMappingPointWeightMustBeDataSource
SedmlBoundsAllowedCoreAttributes = _libsedml.SedmlBoundsAllowedCoreAttributes
SedmlBoundsAllowedCoreElements = _libsedml.SedmlBoundsAllowedCoreElements
SedmlBoundsAllowedAttributes = _libsedml.SedmlBoundsAllowedAttributes
SedmlBoundsLowerBoundMustBeDouble = _libsedml.SedmlBoundsLowerBoundMustBeDouble
SedmlBoundsUpperBoundMustBeDouble = _libsedml.SedmlBoundsUpperBoundMustBeDouble
SedmlBoundsScaleMustBeScaleTypeEnum = _libsedml.SedmlBoundsScaleMustBeScaleTypeEnum
SedmlFigureAllowedCoreAttributes = _libsedml.SedmlFigureAllowedCoreAttributes
SedmlFigureAllowedCoreElements = _libsedml.SedmlFigureAllowedCoreElements
SedmlFigureAllowedAttributes = _libsedml.SedmlFigureAllowedAttributes
SedmlFigureAllowedElements = _libsedml.SedmlFigureAllowedElements
SedmlFigureNumRowsMustBeInteger = _libsedml.SedmlFigureNumRowsMustBeInteger
SedmlFigureNumColsMustBeInteger = _libsedml.SedmlFigureNumColsMustBeInteger
SedmlFigureLOSubPlotsAllowedCoreElements = _libsedml.SedmlFigureLOSubPlotsAllowedCoreElements
SedmlFigureLOSubPlotsAllowedCoreAttributes = _libsedml.SedmlFigureLOSubPlotsAllowedCoreAttributes
SedmlSubPlotAllowedCoreAttributes = _libsedml.SedmlSubPlotAllowedCoreAttributes
SedmlSubPlotAllowedCoreElements = _libsedml.SedmlSubPlotAllowedCoreElements
SedmlSubPlotAllowedAttributes = _libsedml.SedmlSubPlotAllowedAttributes
SedmlSubPlotPlotMustBePlot = _libsedml.SedmlSubPlotPlotMustBePlot
SedmlSubPlotRowMustBeInteger = _libsedml.SedmlSubPlotRowMustBeInteger
SedmlSubPlotColMustBeInteger = _libsedml.SedmlSubPlotColMustBeInteger
SedmlSubPlotRowSpanMustBeInteger = _libsedml.SedmlSubPlotRowSpanMustBeInteger
SedmlSubPlotColSpanMustBeInteger = _libsedml.SedmlSubPlotColSpanMustBeInteger
SedmlAxisAllowedCoreAttributes = _libsedml.SedmlAxisAllowedCoreAttributes
SedmlAxisAllowedCoreElements = _libsedml.SedmlAxisAllowedCoreElements
SedmlAxisAllowedAttributes = _libsedml.SedmlAxisAllowedAttributes
SedmlAxisTypeMustBeAxisTypeEnum = _libsedml.SedmlAxisTypeMustBeAxisTypeEnum
SedmlAxisMinMustBeDouble = _libsedml.SedmlAxisMinMustBeDouble
SedmlAxisMaxMustBeDouble = _libsedml.SedmlAxisMaxMustBeDouble
SedmlAxisGridMustBeBoolean = _libsedml.SedmlAxisGridMustBeBoolean
SedmlAxisStyleMustBeStyle = _libsedml.SedmlAxisStyleMustBeStyle
SedmlStyleAllowedCoreAttributes = _libsedml.SedmlStyleAllowedCoreAttributes
SedmlStyleAllowedCoreElements = _libsedml.SedmlStyleAllowedCoreElements
SedmlStyleAllowedAttributes = _libsedml.SedmlStyleAllowedAttributes
SedmlStyleAllowedElements = _libsedml.SedmlStyleAllowedElements
SedmlStyleBaseStyleMustBeStyle = _libsedml.SedmlStyleBaseStyleMustBeStyle
SedmlLineAllowedCoreAttributes = _libsedml.SedmlLineAllowedCoreAttributes
SedmlLineAllowedCoreElements = _libsedml.SedmlLineAllowedCoreElements
SedmlLineAllowedAttributes = _libsedml.SedmlLineAllowedAttributes
SedmlLineStyleMustBeLineTypeEnum = _libsedml.SedmlLineStyleMustBeLineTypeEnum
SedmlLineColorMustBeString = _libsedml.SedmlLineColorMustBeString
SedmlLineThicknessMustBeDouble = _libsedml.SedmlLineThicknessMustBeDouble
SedmlMarkerAllowedCoreAttributes = _libsedml.SedmlMarkerAllowedCoreAttributes
SedmlMarkerAllowedCoreElements = _libsedml.SedmlMarkerAllowedCoreElements
SedmlMarkerAllowedAttributes = _libsedml.SedmlMarkerAllowedAttributes
SedmlMarkerSizeMustBeDouble = _libsedml.SedmlMarkerSizeMustBeDouble
SedmlMarkerStyleMustBeMarkerTypeEnum = _libsedml.SedmlMarkerStyleMustBeMarkerTypeEnum
SedmlMarkerFillMustBeString = _libsedml.SedmlMarkerFillMustBeString
SedmlMarkerLineColorMustBeString = _libsedml.SedmlMarkerLineColorMustBeString
SedmlMarkerLineThicknessMustBeDouble = _libsedml.SedmlMarkerLineThicknessMustBeDouble
SedmlFillAllowedCoreAttributes = _libsedml.SedmlFillAllowedCoreAttributes
SedmlFillAllowedCoreElements = _libsedml.SedmlFillAllowedCoreElements
SedmlFillAllowedAttributes = _libsedml.SedmlFillAllowedAttributes
SedmlFillColorMustBeString = _libsedml.SedmlFillColorMustBeString
SedmlFillSecondColorMustBeString = _libsedml.SedmlFillSecondColorMustBeString
SedmlDependentVariableAllowedCoreAttributes = _libsedml.SedmlDependentVariableAllowedCoreAttributes
SedmlDependentVariableAllowedCoreElements = _libsedml.SedmlDependentVariableAllowedCoreElements
SedmlDependentVariableAllowedAttributes = _libsedml.SedmlDependentVariableAllowedAttributes
SedmlDependentVariableTermMustBeString = _libsedml.SedmlDependentVariableTermMustBeString
SedmlDependentVariableTarget2MustBeString = _libsedml.SedmlDependentVariableTarget2MustBeString
SedmlDependentVariableSymbol2MustBeString = _libsedml.SedmlDependentVariableSymbol2MustBeString
SedmlRemainingDimensionAllowedCoreAttributes = _libsedml.SedmlRemainingDimensionAllowedCoreAttributes
SedmlRemainingDimensionAllowedCoreElements = _libsedml.SedmlRemainingDimensionAllowedCoreElements
SedmlRemainingDimensionAllowedAttributes = _libsedml.SedmlRemainingDimensionAllowedAttributes
SedmlRemainingDimensionTargetMustBeSId = _libsedml.SedmlRemainingDimensionTargetMustBeSId
SedmlRemainingDimensionDimensionTargetMustBeSId = _libsedml.SedmlRemainingDimensionDimensionTargetMustBeSId
SedmlDataRangeAllowedCoreAttributes = _libsedml.SedmlDataRangeAllowedCoreAttributes
SedmlDataRangeAllowedCoreElements = _libsedml.SedmlDataRangeAllowedCoreElements
SedmlDataRangeAllowedAttributes = _libsedml.SedmlDataRangeAllowedAttributes
SedmlDataRangeSourceRefMustBeSId = _libsedml.SedmlDataRangeSourceRefMustBeSId
SedmlSimpleRepeatedTaskAllowedCoreAttributes = _libsedml.SedmlSimpleRepeatedTaskAllowedCoreAttributes
SedmlSimpleRepeatedTaskAllowedCoreElements = _libsedml.SedmlSimpleRepeatedTaskAllowedCoreElements
SedmlSimpleRepeatedTaskAllowedAttributes = _libsedml.SedmlSimpleRepeatedTaskAllowedAttributes
SedmlSimpleRepeatedTaskResetModelMustBeBoolean = _libsedml.SedmlSimpleRepeatedTaskResetModelMustBeBoolean
SedmlSimpleRepeatedTaskNumRepeatsMustBeInteger = _libsedml.SedmlSimpleRepeatedTaskNumRepeatsMustBeInteger
SedmlShadedAreaAllowedCoreAttributes = _libsedml.SedmlShadedAreaAllowedCoreAttributes
SedmlShadedAreaAllowedCoreElements = _libsedml.SedmlShadedAreaAllowedCoreElements
SedmlShadedAreaAllowedAttributes = _libsedml.SedmlShadedAreaAllowedAttributes
SedmlShadedAreaYDataReferenceFromMustBeDataGenerator = _libsedml.SedmlShadedAreaYDataReferenceFromMustBeDataGenerator
SedmlShadedAreaYDataReferenceToMustBeDataGenerator = _libsedml.SedmlShadedAreaYDataReferenceToMustBeDataGenerator
SedmlParameterEstimationResultPlotAllowedCoreAttributes = _libsedml.SedmlParameterEstimationResultPlotAllowedCoreAttributes
SedmlParameterEstimationResultPlotAllowedCoreElements = _libsedml.SedmlParameterEstimationResultPlotAllowedCoreElements
SedmlParameterEstimationResultPlotAllowedAttributes = _libsedml.SedmlParameterEstimationResultPlotAllowedAttributes
SedmlParameterEstimationResultPlotTaskRefMustBeTask = _libsedml.SedmlParameterEstimationResultPlotTaskRefMustBeTask
SedmlWaterfallPlotAllowedCoreAttributes = _libsedml.SedmlWaterfallPlotAllowedCoreAttributes
SedmlWaterfallPlotAllowedCoreElements = _libsedml.SedmlWaterfallPlotAllowedCoreElements
SedmlWaterfallPlotAllowedAttributes = _libsedml.SedmlWaterfallPlotAllowedAttributes
SedmlWaterfallPlotTaskRefMustBeTask = _libsedml.SedmlWaterfallPlotTaskRefMustBeTask
SedmlParameterEstimationReportAllowedCoreAttributes = _libsedml.SedmlParameterEstimationReportAllowedCoreAttributes
SedmlParameterEstimationReportAllowedCoreElements = _libsedml.SedmlParameterEstimationReportAllowedCoreElements
SedmlParameterEstimationReportAllowedAttributes = _libsedml.SedmlParameterEstimationReportAllowedAttributes
SedmlParameterEstimationReportTaskRefMustBeTask = _libsedml.SedmlParameterEstimationReportTaskRefMustBeTask
SedUnknownCoreAttribute = _libsedml.SedUnknownCoreAttribute
SedCodesUpperBound = _libsedml.SedCodesUpperBound
LIBSEDML_CAT_INTERNAL = _libsedml.LIBSEDML_CAT_INTERNAL
LIBSEDML_CAT_SYSTEM = _libsedml.LIBSEDML_CAT_SYSTEM
LIBSEDML_CAT_XML = _libsedml.LIBSEDML_CAT_XML
LIBSEDML_CAT_SEDML = _libsedml.LIBSEDML_CAT_SEDML
LIBSEDML_CAT_GENERAL_CONSISTENCY = _libsedml.LIBSEDML_CAT_GENERAL_CONSISTENCY
LIBSEDML_CAT_IDENTIFIER_CONSISTENCY = _libsedml.LIBSEDML_CAT_IDENTIFIER_CONSISTENCY
LIBSEDML_CAT_MATHML_CONSISTENCY = _libsedml.LIBSEDML_CAT_MATHML_CONSISTENCY
LIBSEDML_CAT_INTERNAL_CONSISTENCY = _libsedml.LIBSEDML_CAT_INTERNAL_CONSISTENCY
LIBSEDML_SEV_WARNING = _libsedml.LIBSEDML_SEV_WARNING
LIBSEDML_SEV_ERROR = _libsedml.LIBSEDML_SEV_ERROR
LIBSEDML_SEV_FATAL = _libsedml.LIBSEDML_SEV_FATAL
LIBSEDML_SEV_SCHEMA_ERROR = _libsedml.LIBSEDML_SEV_SCHEMA_ERROR
LIBSEDML_SEV_GENERAL_WARNING = _libsedml.LIBSEDML_SEV_GENERAL_WARNING
LIBSEDML_SEV_NOT_APPLICABLE = _libsedml.LIBSEDML_SEV_NOT_APPLICABLE

class SedError(XMLError):
    """Proxy of C++ SedError class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedError self, unsigned int const errorId=0, unsigned int const level=SEDML_DEFAULT_LEVEL, unsigned int const version=SEDML_DEFAULT_VERSION, string details="", unsigned int const line=0, unsigned int const column=0, unsigned int const severity=LIBSEDML_SEV_ERROR, unsigned int const category=LIBSEDML_CAT_SEDML) -> SedError
        __init__(SedError self, SedError orig) -> SedError
        """
        _libsedml.SedError_swiginit(self, _libsedml.new_SedError(*args))

    __swig_destroy__ = _libsedml.delete_SedError


_libsedml.SedError_swigregister(SedError)

class SedNamespaces(object):
    """Proxy of C++ SedNamespaces class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_SedNamespaces

    def __init__(self, *args):
        """
        __init__(SedNamespaces self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedNamespaces
        __init__(SedNamespaces self, SedNamespaces orig) -> SedNamespaces
        """
        _libsedml.SedNamespaces_swiginit(self, _libsedml.new_SedNamespaces(*args))

    def clone(self):
        """clone(SedNamespaces self) -> SedNamespaces"""
        return _libsedml.SedNamespaces_clone(self)

    @staticmethod
    def getSedNamespaceURI(level, version):
        """getSedNamespaceURI(unsigned int level, unsigned int version) -> string"""
        return _libsedml.SedNamespaces_getSedNamespaceURI(level, version)

    @staticmethod
    def getSupportedNamespaces():
        """getSupportedNamespaces() -> List const *"""
        return _libsedml.SedNamespaces_getSupportedNamespaces()

    @staticmethod
    def freeSedNamespaces(supportedNS):
        """freeSedNamespaces(List * supportedNS)"""
        return _libsedml.SedNamespaces_freeSedNamespaces(supportedNS)

    def getURI(self):
        """getURI(SedNamespaces self) -> string"""
        return _libsedml.SedNamespaces_getURI(self)

    def getLevel(self, *args):
        """
        getLevel(SedNamespaces self) -> unsigned int
        getLevel(SedNamespaces self) -> unsigned int
        """
        return _libsedml.SedNamespaces_getLevel(self, *args)

    def getVersion(self, *args):
        """
        getVersion(SedNamespaces self) -> unsigned int
        getVersion(SedNamespaces self) -> unsigned int
        """
        return _libsedml.SedNamespaces_getVersion(self, *args)

    def getNamespaces(self, *args):
        """
        getNamespaces(SedNamespaces self) -> XMLNamespaces
        getNamespaces(SedNamespaces self) -> XMLNamespaces
        """
        return _libsedml.SedNamespaces_getNamespaces(self, *args)

    def addNamespaces(self, xmlns):
        """addNamespaces(SedNamespaces self, XMLNamespaces xmlns) -> int"""
        return _libsedml.SedNamespaces_addNamespaces(self, xmlns)

    def addNamespace(self, uri, prefix):
        """addNamespace(SedNamespaces self, string uri, string prefix) -> int"""
        return _libsedml.SedNamespaces_addNamespace(self, uri, prefix)

    def removeNamespace(self, uri):
        """removeNamespace(SedNamespaces self, string uri) -> int"""
        return _libsedml.SedNamespaces_removeNamespace(self, uri)

    @staticmethod
    def isSedNamespace(uri):
        """isSedNamespace(string uri) -> bool"""
        return _libsedml.SedNamespaces_isSedNamespace(uri)

    def isValidCombination(self):
        """isValidCombination(SedNamespaces self) -> bool"""
        return _libsedml.SedNamespaces_isValidCombination(self)

    def setLevel(self, level):
        """setLevel(SedNamespaces self, unsigned int level)"""
        return _libsedml.SedNamespaces_setLevel(self, level)

    def setVersion(self, version):
        """setVersion(SedNamespaces self, unsigned int version)"""
        return _libsedml.SedNamespaces_setVersion(self, version)

    def setNamespaces(self, xmlns):
        """setNamespaces(SedNamespaces self, XMLNamespaces xmlns)"""
        return _libsedml.SedNamespaces_setNamespaces(self, xmlns)

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True


_libsedml.SedNamespaces_swigregister(SedNamespaces)

def SedNamespaces_getSedNamespaceURI(level, version):
    """SedNamespaces_getSedNamespaceURI(unsigned int level, unsigned int version) -> string"""
    return _libsedml.SedNamespaces_getSedNamespaceURI(level, version)


def SedNamespaces_getSupportedNamespaces():
    """SedNamespaces_getSupportedNamespaces() -> List const *"""
    return _libsedml.SedNamespaces_getSupportedNamespaces()


def SedNamespaces_freeSedNamespaces(supportedNS):
    """SedNamespaces_freeSedNamespaces(List * supportedNS)"""
    return _libsedml.SedNamespaces_freeSedNamespaces(supportedNS)


def SedNamespaces_isSedNamespace(uri):
    """SedNamespaces_isSedNamespace(string uri) -> bool"""
    return _libsedml.SedNamespaces_isSedNamespace(uri)


class SedModel(SedBase):
    """Proxy of C++ SedModel class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedModel self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedModel
        __init__(SedModel self, SedNamespaces sedmlns) -> SedModel
        __init__(SedModel self, SedModel orig) -> SedModel
        """
        _libsedml.SedModel_swiginit(self, _libsedml.new_SedModel(*args))

    def clone(self):
        """clone(SedModel self) -> SedModel"""
        return _libsedml.SedModel_clone(self)

    __swig_destroy__ = _libsedml.delete_SedModel

    def getId(self):
        """getId(SedModel self) -> string"""
        return _libsedml.SedModel_getId(self)

    def getName(self):
        """getName(SedModel self) -> string"""
        return _libsedml.SedModel_getName(self)

    def getLanguage(self):
        """getLanguage(SedModel self) -> string"""
        return _libsedml.SedModel_getLanguage(self)

    def getSource(self):
        """getSource(SedModel self) -> string"""
        return _libsedml.SedModel_getSource(self)

    def isSetId(self):
        """isSetId(SedModel self) -> bool"""
        return _libsedml.SedModel_isSetId(self)

    def isSetName(self):
        """isSetName(SedModel self) -> bool"""
        return _libsedml.SedModel_isSetName(self)

    def isSetLanguage(self):
        """isSetLanguage(SedModel self) -> bool"""
        return _libsedml.SedModel_isSetLanguage(self)

    def isSetSource(self):
        """isSetSource(SedModel self) -> bool"""
        return _libsedml.SedModel_isSetSource(self)

    def setId(self, id):
        """setId(SedModel self, string id) -> int"""
        return _libsedml.SedModel_setId(self, id)

    def setName(self, name):
        """setName(SedModel self, string name) -> int"""
        return _libsedml.SedModel_setName(self, name)

    def setLanguage(self, language):
        """setLanguage(SedModel self, string language) -> int"""
        return _libsedml.SedModel_setLanguage(self, language)

    def setSource(self, source):
        """setSource(SedModel self, string source) -> int"""
        return _libsedml.SedModel_setSource(self, source)

    def unsetId(self):
        """unsetId(SedModel self) -> int"""
        return _libsedml.SedModel_unsetId(self)

    def unsetName(self):
        """unsetName(SedModel self) -> int"""
        return _libsedml.SedModel_unsetName(self)

    def unsetLanguage(self):
        """unsetLanguage(SedModel self) -> int"""
        return _libsedml.SedModel_unsetLanguage(self)

    def unsetSource(self):
        """unsetSource(SedModel self) -> int"""
        return _libsedml.SedModel_unsetSource(self)

    def getListOfChanges(self, *args):
        """
        getListOfChanges(SedModel self) -> SedListOfChanges
        getListOfChanges(SedModel self) -> SedListOfChanges
        """
        return _libsedml.SedModel_getListOfChanges(self, *args)

    def getChange(self, *args):
        """
        getChange(SedModel self, unsigned int n) -> SedChange
        getChange(SedModel self, unsigned int n) -> SedChange
        """
        return _libsedml.SedModel_getChange(self, *args)

    def addChange(self, sc):
        """addChange(SedModel self, SedChange sc) -> int"""
        return _libsedml.SedModel_addChange(self, sc)

    def getNumChanges(self):
        """getNumChanges(SedModel self) -> unsigned int"""
        return _libsedml.SedModel_getNumChanges(self)

    def createAddXML(self):
        """createAddXML(SedModel self) -> SedAddXML"""
        return _libsedml.SedModel_createAddXML(self)

    def createChangeXML(self):
        """createChangeXML(SedModel self) -> SedChangeXML"""
        return _libsedml.SedModel_createChangeXML(self)

    def createRemoveXML(self):
        """createRemoveXML(SedModel self) -> SedRemoveXML"""
        return _libsedml.SedModel_createRemoveXML(self)

    def createChangeAttribute(self):
        """createChangeAttribute(SedModel self) -> SedChangeAttribute"""
        return _libsedml.SedModel_createChangeAttribute(self)

    def createComputeChange(self):
        """createComputeChange(SedModel self) -> SedComputeChange"""
        return _libsedml.SedModel_createComputeChange(self)

    def removeChange(self, n):
        """removeChange(SedModel self, unsigned int n) -> SedChange"""
        return _libsedml.SedModel_removeChange(self, n)

    def getElementName(self):
        """getElementName(SedModel self) -> string"""
        return _libsedml.SedModel_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedModel self) -> int"""
        return _libsedml.SedModel_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedModel self) -> bool"""
        return _libsedml.SedModel_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedModel self)"""
        return _libsedml.SedModel_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedModel self, string id) -> SedBase"""
        return _libsedml.SedModel_getElementBySId(self, id)


_libsedml.SedModel_swigregister(SedModel)

class SedListOfModels(SedListOf):
    """Proxy of C++ SedListOfModels class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfModels self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfModels
        __init__(SedListOfModels self, SedNamespaces sedmlns) -> SedListOfModels
        __init__(SedListOfModels self, SedListOfModels orig) -> SedListOfModels
        """
        _libsedml.SedListOfModels_swiginit(self, _libsedml.new_SedListOfModels(*args))

    def clone(self):
        """clone(SedListOfModels self) -> SedListOfModels"""
        return _libsedml.SedListOfModels_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfModels

    def get(self, *args):
        """
        get(SedListOfModels self, unsigned int n) -> SedModel
        get(SedListOfModels self, unsigned int n) -> SedModel
        get(SedListOfModels self, string sid) -> SedModel
        get(SedListOfModels self, string sid) -> SedModel
        """
        return _libsedml.SedListOfModels_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfModels self, unsigned int n) -> SedModel
        remove(SedListOfModels self, string sid) -> SedModel
        """
        return _libsedml.SedListOfModels_remove(self, *args)

    def addModel(self, sm):
        """addModel(SedListOfModels self, SedModel sm) -> int"""
        return _libsedml.SedListOfModels_addModel(self, sm)

    def getNumModels(self):
        """getNumModels(SedListOfModels self) -> unsigned int"""
        return _libsedml.SedListOfModels_getNumModels(self)

    def createModel(self):
        """createModel(SedListOfModels self) -> SedModel"""
        return _libsedml.SedListOfModels_createModel(self)

    def getElementName(self):
        """getElementName(SedListOfModels self) -> string"""
        return _libsedml.SedListOfModels_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfModels self) -> int"""
        return _libsedml.SedListOfModels_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfModels self) -> int"""
        return _libsedml.SedListOfModels_getItemTypeCode(self)


_libsedml.SedListOfModels_swigregister(SedListOfModels)

class SedChange(SedBase):
    """Proxy of C++ SedChange class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedChange self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedChange
        __init__(SedChange self, SedNamespaces sedmlns) -> SedChange
        __init__(SedChange self, SedChange orig) -> SedChange
        """
        _libsedml.SedChange_swiginit(self, _libsedml.new_SedChange(*args))

    def clone(self):
        """clone(SedChange self) -> SedChange"""
        return _libsedml.SedChange_clone(self)

    __swig_destroy__ = _libsedml.delete_SedChange

    def getTarget(self):
        """getTarget(SedChange self) -> string"""
        return _libsedml.SedChange_getTarget(self)

    def isSetTarget(self):
        """isSetTarget(SedChange self) -> bool"""
        return _libsedml.SedChange_isSetTarget(self)

    def setTarget(self, target):
        """setTarget(SedChange self, string target) -> int"""
        return _libsedml.SedChange_setTarget(self, target)

    def unsetTarget(self):
        """unsetTarget(SedChange self) -> int"""
        return _libsedml.SedChange_unsetTarget(self)

    def isSedAddXML(self):
        """isSedAddXML(SedChange self) -> bool"""
        return _libsedml.SedChange_isSedAddXML(self)

    def isSedChangeXML(self):
        """isSedChangeXML(SedChange self) -> bool"""
        return _libsedml.SedChange_isSedChangeXML(self)

    def isSedRemoveXML(self):
        """isSedRemoveXML(SedChange self) -> bool"""
        return _libsedml.SedChange_isSedRemoveXML(self)

    def isSedChangeAttribute(self):
        """isSedChangeAttribute(SedChange self) -> bool"""
        return _libsedml.SedChange_isSedChangeAttribute(self)

    def isSedComputeChange(self):
        """isSedComputeChange(SedChange self) -> bool"""
        return _libsedml.SedChange_isSedComputeChange(self)

    def getElementName(self):
        """getElementName(SedChange self) -> string"""
        return _libsedml.SedChange_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedChange self, string name)"""
        return _libsedml.SedChange_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedChange self) -> int"""
        return _libsedml.SedChange_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedChange self) -> bool"""
        return _libsedml.SedChange_hasRequiredAttributes(self)


_libsedml.SedChange_swigregister(SedChange)

class SedListOfChanges(SedListOf):
    """Proxy of C++ SedListOfChanges class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfChanges self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfChanges
        __init__(SedListOfChanges self, SedNamespaces sedmlns) -> SedListOfChanges
        __init__(SedListOfChanges self, SedListOfChanges orig) -> SedListOfChanges
        """
        _libsedml.SedListOfChanges_swiginit(self, _libsedml.new_SedListOfChanges(*args))

    def clone(self):
        """clone(SedListOfChanges self) -> SedListOfChanges"""
        return _libsedml.SedListOfChanges_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfChanges

    def get(self, *args):
        """
        get(SedListOfChanges self, unsigned int n) -> SedChange
        get(SedListOfChanges self, unsigned int n) -> SedChange
        get(SedListOfChanges self, string sid) -> SedChange
        get(SedListOfChanges self, string sid) -> SedChange
        """
        return _libsedml.SedListOfChanges_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfChanges self, unsigned int n) -> SedChange
        remove(SedListOfChanges self, string sid) -> SedChange
        """
        return _libsedml.SedListOfChanges_remove(self, *args)

    def addChange(self, sc):
        """addChange(SedListOfChanges self, SedChange sc) -> int"""
        return _libsedml.SedListOfChanges_addChange(self, sc)

    def getNumChanges(self):
        """getNumChanges(SedListOfChanges self) -> unsigned int"""
        return _libsedml.SedListOfChanges_getNumChanges(self)

    def createAddXML(self):
        """createAddXML(SedListOfChanges self) -> SedAddXML"""
        return _libsedml.SedListOfChanges_createAddXML(self)

    def createChangeXML(self):
        """createChangeXML(SedListOfChanges self) -> SedChangeXML"""
        return _libsedml.SedListOfChanges_createChangeXML(self)

    def createRemoveXML(self):
        """createRemoveXML(SedListOfChanges self) -> SedRemoveXML"""
        return _libsedml.SedListOfChanges_createRemoveXML(self)

    def createChangeAttribute(self):
        """createChangeAttribute(SedListOfChanges self) -> SedChangeAttribute"""
        return _libsedml.SedListOfChanges_createChangeAttribute(self)

    def createComputeChange(self):
        """createComputeChange(SedListOfChanges self) -> SedComputeChange"""
        return _libsedml.SedListOfChanges_createComputeChange(self)

    def getElementName(self):
        """getElementName(SedListOfChanges self) -> string"""
        return _libsedml.SedListOfChanges_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfChanges self) -> int"""
        return _libsedml.SedListOfChanges_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfChanges self) -> int"""
        return _libsedml.SedListOfChanges_getItemTypeCode(self)


_libsedml.SedListOfChanges_swigregister(SedListOfChanges)

class SedAddXML(SedChange):
    """Proxy of C++ SedAddXML class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedAddXML self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedAddXML
        __init__(SedAddXML self, SedNamespaces sedmlns) -> SedAddXML
        __init__(SedAddXML self, SedAddXML orig) -> SedAddXML
        """
        _libsedml.SedAddXML_swiginit(self, _libsedml.new_SedAddXML(*args))

    def clone(self):
        """clone(SedAddXML self) -> SedAddXML"""
        return _libsedml.SedAddXML_clone(self)

    __swig_destroy__ = _libsedml.delete_SedAddXML

    def getNewXML(self, *args):
        """
        getNewXML(SedAddXML self) -> XMLNode
        getNewXML(SedAddXML self) -> XMLNode
        """
        return _libsedml.SedAddXML_getNewXML(self, *args)

    def isSetNewXML(self):
        """isSetNewXML(SedAddXML self) -> bool"""
        return _libsedml.SedAddXML_isSetNewXML(self)

    def setNewXML(self, newXML):
        """setNewXML(SedAddXML self, XMLNode newXML) -> int"""
        return _libsedml.SedAddXML_setNewXML(self, newXML)

    def unsetNewXML(self):
        """unsetNewXML(SedAddXML self) -> int"""
        return _libsedml.SedAddXML_unsetNewXML(self)

    def getElementName(self):
        """getElementName(SedAddXML self) -> string"""
        return _libsedml.SedAddXML_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedAddXML self) -> int"""
        return _libsedml.SedAddXML_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedAddXML self) -> bool"""
        return _libsedml.SedAddXML_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedAddXML self) -> bool"""
        return _libsedml.SedAddXML_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedAddXML self)"""
        return _libsedml.SedAddXML_connectToChild(self)


_libsedml.SedAddXML_swigregister(SedAddXML)

class SedChangeAttribute(SedChange):
    """Proxy of C++ SedChangeAttribute class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedChangeAttribute self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedChangeAttribute
        __init__(SedChangeAttribute self, SedNamespaces sedmlns) -> SedChangeAttribute
        __init__(SedChangeAttribute self, SedChangeAttribute orig) -> SedChangeAttribute
        """
        _libsedml.SedChangeAttribute_swiginit(self, _libsedml.new_SedChangeAttribute(*args))

    def clone(self):
        """clone(SedChangeAttribute self) -> SedChangeAttribute"""
        return _libsedml.SedChangeAttribute_clone(self)

    __swig_destroy__ = _libsedml.delete_SedChangeAttribute

    def getNewValue(self):
        """getNewValue(SedChangeAttribute self) -> string"""
        return _libsedml.SedChangeAttribute_getNewValue(self)

    def isSetNewValue(self):
        """isSetNewValue(SedChangeAttribute self) -> bool"""
        return _libsedml.SedChangeAttribute_isSetNewValue(self)

    def setNewValue(self, newValue):
        """setNewValue(SedChangeAttribute self, string newValue) -> int"""
        return _libsedml.SedChangeAttribute_setNewValue(self, newValue)

    def unsetNewValue(self):
        """unsetNewValue(SedChangeAttribute self) -> int"""
        return _libsedml.SedChangeAttribute_unsetNewValue(self)

    def getElementName(self):
        """getElementName(SedChangeAttribute self) -> string"""
        return _libsedml.SedChangeAttribute_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedChangeAttribute self) -> int"""
        return _libsedml.SedChangeAttribute_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedChangeAttribute self) -> bool"""
        return _libsedml.SedChangeAttribute_hasRequiredAttributes(self)


_libsedml.SedChangeAttribute_swigregister(SedChangeAttribute)

class SedVariable(SedBase):
    """Proxy of C++ SedVariable class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedVariable self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedVariable
        __init__(SedVariable self, SedNamespaces sedmlns) -> SedVariable
        __init__(SedVariable self, SedVariable orig) -> SedVariable
        """
        _libsedml.SedVariable_swiginit(self, _libsedml.new_SedVariable(*args))

    def clone(self):
        """clone(SedVariable self) -> SedVariable"""
        return _libsedml.SedVariable_clone(self)

    __swig_destroy__ = _libsedml.delete_SedVariable

    def getId(self):
        """getId(SedVariable self) -> string"""
        return _libsedml.SedVariable_getId(self)

    def getName(self):
        """getName(SedVariable self) -> string"""
        return _libsedml.SedVariable_getName(self)

    def getSymbol(self):
        """getSymbol(SedVariable self) -> string"""
        return _libsedml.SedVariable_getSymbol(self)

    def getTarget(self):
        """getTarget(SedVariable self) -> string"""
        return _libsedml.SedVariable_getTarget(self)

    def getTaskReference(self):
        """getTaskReference(SedVariable self) -> string"""
        return _libsedml.SedVariable_getTaskReference(self)

    def getModelReference(self):
        """getModelReference(SedVariable self) -> string"""
        return _libsedml.SedVariable_getModelReference(self)

    def isSetId(self):
        """isSetId(SedVariable self) -> bool"""
        return _libsedml.SedVariable_isSetId(self)

    def isSetName(self):
        """isSetName(SedVariable self) -> bool"""
        return _libsedml.SedVariable_isSetName(self)

    def isSetSymbol(self):
        """isSetSymbol(SedVariable self) -> bool"""
        return _libsedml.SedVariable_isSetSymbol(self)

    def isSetTarget(self):
        """isSetTarget(SedVariable self) -> bool"""
        return _libsedml.SedVariable_isSetTarget(self)

    def isSetTaskReference(self):
        """isSetTaskReference(SedVariable self) -> bool"""
        return _libsedml.SedVariable_isSetTaskReference(self)

    def isSetModelReference(self):
        """isSetModelReference(SedVariable self) -> bool"""
        return _libsedml.SedVariable_isSetModelReference(self)

    def setId(self, id):
        """setId(SedVariable self, string id) -> int"""
        return _libsedml.SedVariable_setId(self, id)

    def setName(self, name):
        """setName(SedVariable self, string name) -> int"""
        return _libsedml.SedVariable_setName(self, name)

    def setSymbol(self, symbol):
        """setSymbol(SedVariable self, string symbol) -> int"""
        return _libsedml.SedVariable_setSymbol(self, symbol)

    def setTarget(self, target):
        """setTarget(SedVariable self, string target) -> int"""
        return _libsedml.SedVariable_setTarget(self, target)

    def setTaskReference(self, taskReference):
        """setTaskReference(SedVariable self, string taskReference) -> int"""
        return _libsedml.SedVariable_setTaskReference(self, taskReference)

    def setModelReference(self, modelReference):
        """setModelReference(SedVariable self, string modelReference) -> int"""
        return _libsedml.SedVariable_setModelReference(self, modelReference)

    def unsetId(self):
        """unsetId(SedVariable self) -> int"""
        return _libsedml.SedVariable_unsetId(self)

    def unsetName(self):
        """unsetName(SedVariable self) -> int"""
        return _libsedml.SedVariable_unsetName(self)

    def unsetSymbol(self):
        """unsetSymbol(SedVariable self) -> int"""
        return _libsedml.SedVariable_unsetSymbol(self)

    def unsetTarget(self):
        """unsetTarget(SedVariable self) -> int"""
        return _libsedml.SedVariable_unsetTarget(self)

    def unsetTaskReference(self):
        """unsetTaskReference(SedVariable self) -> int"""
        return _libsedml.SedVariable_unsetTaskReference(self)

    def unsetModelReference(self):
        """unsetModelReference(SedVariable self) -> int"""
        return _libsedml.SedVariable_unsetModelReference(self)

    def getListOfRemainingDimensions(self, *args):
        """
        getListOfRemainingDimensions(SedVariable self) -> SedListOfRemainingDimensions
        getListOfRemainingDimensions(SedVariable self) -> SedListOfRemainingDimensions
        """
        return _libsedml.SedVariable_getListOfRemainingDimensions(self, *args)

    def getRemainingDimension(self, *args):
        """
        getRemainingDimension(SedVariable self, unsigned int n) -> SedRemainingDimension
        getRemainingDimension(SedVariable self, unsigned int n) -> SedRemainingDimension
        """
        return _libsedml.SedVariable_getRemainingDimension(self, *args)

    def getRemainingDimensionByTarget(self, *args):
        """
        getRemainingDimensionByTarget(SedVariable self, string sid) -> SedRemainingDimension
        getRemainingDimensionByTarget(SedVariable self, string sid) -> SedRemainingDimension
        """
        return _libsedml.SedVariable_getRemainingDimensionByTarget(self, *args)

    def getRemainingDimensionByDimensionTarget(self, *args):
        """
        getRemainingDimensionByDimensionTarget(SedVariable self, string sid) -> SedRemainingDimension
        getRemainingDimensionByDimensionTarget(SedVariable self, string sid) -> SedRemainingDimension
        """
        return _libsedml.SedVariable_getRemainingDimensionByDimensionTarget(self, *args)

    def addRemainingDimension(self, srd):
        """addRemainingDimension(SedVariable self, SedRemainingDimension srd) -> int"""
        return _libsedml.SedVariable_addRemainingDimension(self, srd)

    def getNumRemainingDimensions(self):
        """getNumRemainingDimensions(SedVariable self) -> unsigned int"""
        return _libsedml.SedVariable_getNumRemainingDimensions(self)

    def createRemainingDimension(self):
        """createRemainingDimension(SedVariable self) -> SedRemainingDimension"""
        return _libsedml.SedVariable_createRemainingDimension(self)

    def removeRemainingDimension(self, n):
        """removeRemainingDimension(SedVariable self, unsigned int n) -> SedRemainingDimension"""
        return _libsedml.SedVariable_removeRemainingDimension(self, n)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedVariable self, string oldid, string newid)"""
        return _libsedml.SedVariable_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedVariable self) -> string"""
        return _libsedml.SedVariable_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedVariable self) -> int"""
        return _libsedml.SedVariable_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedVariable self) -> bool"""
        return _libsedml.SedVariable_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedVariable self)"""
        return _libsedml.SedVariable_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedVariable self, string id) -> SedBase"""
        return _libsedml.SedVariable_getElementBySId(self, id)


_libsedml.SedVariable_swigregister(SedVariable)

class SedListOfVariables(SedListOf):
    """Proxy of C++ SedListOfVariables class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfVariables self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfVariables
        __init__(SedListOfVariables self, SedNamespaces sedmlns) -> SedListOfVariables
        __init__(SedListOfVariables self, SedListOfVariables orig) -> SedListOfVariables
        """
        _libsedml.SedListOfVariables_swiginit(self, _libsedml.new_SedListOfVariables(*args))

    def clone(self):
        """clone(SedListOfVariables self) -> SedListOfVariables"""
        return _libsedml.SedListOfVariables_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfVariables

    def get(self, *args):
        """
        get(SedListOfVariables self, unsigned int n) -> SedVariable
        get(SedListOfVariables self, unsigned int n) -> SedVariable
        get(SedListOfVariables self, string sid) -> SedVariable
        get(SedListOfVariables self, string sid) -> SedVariable
        """
        return _libsedml.SedListOfVariables_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfVariables self, unsigned int n) -> SedVariable
        remove(SedListOfVariables self, string sid) -> SedVariable
        """
        return _libsedml.SedListOfVariables_remove(self, *args)

    def addVariable(self, sv):
        """addVariable(SedListOfVariables self, SedVariable sv) -> int"""
        return _libsedml.SedListOfVariables_addVariable(self, sv)

    def getNumVariables(self):
        """getNumVariables(SedListOfVariables self) -> unsigned int"""
        return _libsedml.SedListOfVariables_getNumVariables(self)

    def createVariable(self):
        """createVariable(SedListOfVariables self) -> SedVariable"""
        return _libsedml.SedListOfVariables_createVariable(self)

    def createDependentVariable(self):
        """createDependentVariable(SedListOfVariables self) -> SedDependentVariable"""
        return _libsedml.SedListOfVariables_createDependentVariable(self)

    def getByTaskReference(self, *args):
        """
        getByTaskReference(SedListOfVariables self, string sid) -> SedVariable
        getByTaskReference(SedListOfVariables self, string sid) -> SedVariable
        """
        return _libsedml.SedListOfVariables_getByTaskReference(self, *args)

    def getByModelReference(self, *args):
        """
        getByModelReference(SedListOfVariables self, string sid) -> SedVariable
        getByModelReference(SedListOfVariables self, string sid) -> SedVariable
        """
        return _libsedml.SedListOfVariables_getByModelReference(self, *args)

    def getElementName(self):
        """getElementName(SedListOfVariables self) -> string"""
        return _libsedml.SedListOfVariables_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfVariables self) -> int"""
        return _libsedml.SedListOfVariables_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfVariables self) -> int"""
        return _libsedml.SedListOfVariables_getItemTypeCode(self)


_libsedml.SedListOfVariables_swigregister(SedListOfVariables)

class SedParameter(SedBase):
    """Proxy of C++ SedParameter class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedParameter self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedParameter
        __init__(SedParameter self, SedNamespaces sedmlns) -> SedParameter
        __init__(SedParameter self, SedParameter orig) -> SedParameter
        """
        _libsedml.SedParameter_swiginit(self, _libsedml.new_SedParameter(*args))

    def clone(self):
        """clone(SedParameter self) -> SedParameter"""
        return _libsedml.SedParameter_clone(self)

    __swig_destroy__ = _libsedml.delete_SedParameter

    def getId(self):
        """getId(SedParameter self) -> string"""
        return _libsedml.SedParameter_getId(self)

    def getName(self):
        """getName(SedParameter self) -> string"""
        return _libsedml.SedParameter_getName(self)

    def getValue(self):
        """getValue(SedParameter self) -> double"""
        return _libsedml.SedParameter_getValue(self)

    def isSetId(self):
        """isSetId(SedParameter self) -> bool"""
        return _libsedml.SedParameter_isSetId(self)

    def isSetName(self):
        """isSetName(SedParameter self) -> bool"""
        return _libsedml.SedParameter_isSetName(self)

    def isSetValue(self):
        """isSetValue(SedParameter self) -> bool"""
        return _libsedml.SedParameter_isSetValue(self)

    def setId(self, id):
        """setId(SedParameter self, string id) -> int"""
        return _libsedml.SedParameter_setId(self, id)

    def setName(self, name):
        """setName(SedParameter self, string name) -> int"""
        return _libsedml.SedParameter_setName(self, name)

    def setValue(self, value):
        """setValue(SedParameter self, double value) -> int"""
        return _libsedml.SedParameter_setValue(self, value)

    def unsetId(self):
        """unsetId(SedParameter self) -> int"""
        return _libsedml.SedParameter_unsetId(self)

    def unsetName(self):
        """unsetName(SedParameter self) -> int"""
        return _libsedml.SedParameter_unsetName(self)

    def unsetValue(self):
        """unsetValue(SedParameter self) -> int"""
        return _libsedml.SedParameter_unsetValue(self)

    def getElementName(self):
        """getElementName(SedParameter self) -> string"""
        return _libsedml.SedParameter_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedParameter self) -> int"""
        return _libsedml.SedParameter_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedParameter self) -> bool"""
        return _libsedml.SedParameter_hasRequiredAttributes(self)


_libsedml.SedParameter_swigregister(SedParameter)

class SedListOfParameters(SedListOf):
    """Proxy of C++ SedListOfParameters class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfParameters self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfParameters
        __init__(SedListOfParameters self, SedNamespaces sedmlns) -> SedListOfParameters
        __init__(SedListOfParameters self, SedListOfParameters orig) -> SedListOfParameters
        """
        _libsedml.SedListOfParameters_swiginit(self, _libsedml.new_SedListOfParameters(*args))

    def clone(self):
        """clone(SedListOfParameters self) -> SedListOfParameters"""
        return _libsedml.SedListOfParameters_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfParameters

    def get(self, *args):
        """
        get(SedListOfParameters self, unsigned int n) -> SedParameter
        get(SedListOfParameters self, unsigned int n) -> SedParameter
        get(SedListOfParameters self, string sid) -> SedParameter
        get(SedListOfParameters self, string sid) -> SedParameter
        """
        return _libsedml.SedListOfParameters_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfParameters self, unsigned int n) -> SedParameter
        remove(SedListOfParameters self, string sid) -> SedParameter
        """
        return _libsedml.SedListOfParameters_remove(self, *args)

    def addParameter(self, sp):
        """addParameter(SedListOfParameters self, SedParameter sp) -> int"""
        return _libsedml.SedListOfParameters_addParameter(self, sp)

    def getNumParameters(self):
        """getNumParameters(SedListOfParameters self) -> unsigned int"""
        return _libsedml.SedListOfParameters_getNumParameters(self)

    def createParameter(self):
        """createParameter(SedListOfParameters self) -> SedParameter"""
        return _libsedml.SedListOfParameters_createParameter(self)

    def getElementName(self):
        """getElementName(SedListOfParameters self) -> string"""
        return _libsedml.SedListOfParameters_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfParameters self) -> int"""
        return _libsedml.SedListOfParameters_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfParameters self) -> int"""
        return _libsedml.SedListOfParameters_getItemTypeCode(self)


_libsedml.SedListOfParameters_swigregister(SedListOfParameters)

class SedSimulation(SedBase):
    """Proxy of C++ SedSimulation class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedSimulation self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedSimulation
        __init__(SedSimulation self, SedNamespaces sedmlns) -> SedSimulation
        __init__(SedSimulation self, SedSimulation orig) -> SedSimulation
        """
        _libsedml.SedSimulation_swiginit(self, _libsedml.new_SedSimulation(*args))

    def clone(self):
        """clone(SedSimulation self) -> SedSimulation"""
        return _libsedml.SedSimulation_clone(self)

    __swig_destroy__ = _libsedml.delete_SedSimulation

    def getId(self):
        """getId(SedSimulation self) -> string"""
        return _libsedml.SedSimulation_getId(self)

    def getName(self):
        """getName(SedSimulation self) -> string"""
        return _libsedml.SedSimulation_getName(self)

    def isSetId(self):
        """isSetId(SedSimulation self) -> bool"""
        return _libsedml.SedSimulation_isSetId(self)

    def isSetName(self):
        """isSetName(SedSimulation self) -> bool"""
        return _libsedml.SedSimulation_isSetName(self)

    def setId(self, id):
        """setId(SedSimulation self, string id) -> int"""
        return _libsedml.SedSimulation_setId(self, id)

    def setName(self, name):
        """setName(SedSimulation self, string name) -> int"""
        return _libsedml.SedSimulation_setName(self, name)

    def unsetId(self):
        """unsetId(SedSimulation self) -> int"""
        return _libsedml.SedSimulation_unsetId(self)

    def unsetName(self):
        """unsetName(SedSimulation self) -> int"""
        return _libsedml.SedSimulation_unsetName(self)

    def getAlgorithm(self, *args):
        """
        getAlgorithm(SedSimulation self) -> SedAlgorithm
        getAlgorithm(SedSimulation self) -> SedAlgorithm
        """
        return _libsedml.SedSimulation_getAlgorithm(self, *args)

    def isSetAlgorithm(self):
        """isSetAlgorithm(SedSimulation self) -> bool"""
        return _libsedml.SedSimulation_isSetAlgorithm(self)

    def setAlgorithm(self, algorithm):
        """setAlgorithm(SedSimulation self, SedAlgorithm algorithm) -> int"""
        return _libsedml.SedSimulation_setAlgorithm(self, algorithm)

    def createAlgorithm(self):
        """createAlgorithm(SedSimulation self) -> SedAlgorithm"""
        return _libsedml.SedSimulation_createAlgorithm(self)

    def unsetAlgorithm(self):
        """unsetAlgorithm(SedSimulation self) -> int"""
        return _libsedml.SedSimulation_unsetAlgorithm(self)

    def isSedUniformTimeCourse(self):
        """isSedUniformTimeCourse(SedSimulation self) -> bool"""
        return _libsedml.SedSimulation_isSedUniformTimeCourse(self)

    def isSedOneStep(self):
        """isSedOneStep(SedSimulation self) -> bool"""
        return _libsedml.SedSimulation_isSedOneStep(self)

    def isSedSteadyState(self):
        """isSedSteadyState(SedSimulation self) -> bool"""
        return _libsedml.SedSimulation_isSedSteadyState(self)

    def getElementName(self):
        """getElementName(SedSimulation self) -> string"""
        return _libsedml.SedSimulation_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedSimulation self, string name)"""
        return _libsedml.SedSimulation_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedSimulation self) -> int"""
        return _libsedml.SedSimulation_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedSimulation self) -> bool"""
        return _libsedml.SedSimulation_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedSimulation self) -> bool"""
        return _libsedml.SedSimulation_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedSimulation self)"""
        return _libsedml.SedSimulation_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedSimulation self, string id) -> SedBase"""
        return _libsedml.SedSimulation_getElementBySId(self, id)


_libsedml.SedSimulation_swigregister(SedSimulation)

class SedListOfSimulations(SedListOf):
    """Proxy of C++ SedListOfSimulations class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfSimulations self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfSimulations
        __init__(SedListOfSimulations self, SedNamespaces sedmlns) -> SedListOfSimulations
        __init__(SedListOfSimulations self, SedListOfSimulations orig) -> SedListOfSimulations
        """
        _libsedml.SedListOfSimulations_swiginit(self, _libsedml.new_SedListOfSimulations(*args))

    def clone(self):
        """clone(SedListOfSimulations self) -> SedListOfSimulations"""
        return _libsedml.SedListOfSimulations_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfSimulations

    def get(self, *args):
        """
        get(SedListOfSimulations self, unsigned int n) -> SedSimulation
        get(SedListOfSimulations self, unsigned int n) -> SedSimulation
        get(SedListOfSimulations self, string sid) -> SedSimulation
        get(SedListOfSimulations self, string sid) -> SedSimulation
        """
        return _libsedml.SedListOfSimulations_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfSimulations self, unsigned int n) -> SedSimulation
        remove(SedListOfSimulations self, string sid) -> SedSimulation
        """
        return _libsedml.SedListOfSimulations_remove(self, *args)

    def addSimulation(self, ss):
        """addSimulation(SedListOfSimulations self, SedSimulation ss) -> int"""
        return _libsedml.SedListOfSimulations_addSimulation(self, ss)

    def getNumSimulations(self):
        """getNumSimulations(SedListOfSimulations self) -> unsigned int"""
        return _libsedml.SedListOfSimulations_getNumSimulations(self)

    def createUniformTimeCourse(self):
        """createUniformTimeCourse(SedListOfSimulations self) -> SedUniformTimeCourse"""
        return _libsedml.SedListOfSimulations_createUniformTimeCourse(self)

    def createOneStep(self):
        """createOneStep(SedListOfSimulations self) -> SedOneStep"""
        return _libsedml.SedListOfSimulations_createOneStep(self)

    def createSteadyState(self):
        """createSteadyState(SedListOfSimulations self) -> SedSteadyState"""
        return _libsedml.SedListOfSimulations_createSteadyState(self)

    def getElementName(self):
        """getElementName(SedListOfSimulations self) -> string"""
        return _libsedml.SedListOfSimulations_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfSimulations self) -> int"""
        return _libsedml.SedListOfSimulations_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfSimulations self) -> int"""
        return _libsedml.SedListOfSimulations_getItemTypeCode(self)


_libsedml.SedListOfSimulations_swigregister(SedListOfSimulations)

class SedUniformTimeCourse(SedSimulation):
    """Proxy of C++ SedUniformTimeCourse class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedUniformTimeCourse self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedUniformTimeCourse
        __init__(SedUniformTimeCourse self, SedNamespaces sedmlns) -> SedUniformTimeCourse
        __init__(SedUniformTimeCourse self, SedUniformTimeCourse orig) -> SedUniformTimeCourse
        """
        _libsedml.SedUniformTimeCourse_swiginit(self, _libsedml.new_SedUniformTimeCourse(*args))

    def clone(self):
        """clone(SedUniformTimeCourse self) -> SedUniformTimeCourse"""
        return _libsedml.SedUniformTimeCourse_clone(self)

    __swig_destroy__ = _libsedml.delete_SedUniformTimeCourse

    def getInitialTime(self):
        """getInitialTime(SedUniformTimeCourse self) -> double"""
        return _libsedml.SedUniformTimeCourse_getInitialTime(self)

    def getOutputStartTime(self):
        """getOutputStartTime(SedUniformTimeCourse self) -> double"""
        return _libsedml.SedUniformTimeCourse_getOutputStartTime(self)

    def getOutputEndTime(self):
        """getOutputEndTime(SedUniformTimeCourse self) -> double"""
        return _libsedml.SedUniformTimeCourse_getOutputEndTime(self)

    def getNumberOfPoints(self):
        """getNumberOfPoints(SedUniformTimeCourse self) -> int"""
        return _libsedml.SedUniformTimeCourse_getNumberOfPoints(self)

    def getNumberOfSteps(self):
        """getNumberOfSteps(SedUniformTimeCourse self) -> int"""
        return _libsedml.SedUniformTimeCourse_getNumberOfSteps(self)

    def isSetInitialTime(self):
        """isSetInitialTime(SedUniformTimeCourse self) -> bool"""
        return _libsedml.SedUniformTimeCourse_isSetInitialTime(self)

    def isSetOutputStartTime(self):
        """isSetOutputStartTime(SedUniformTimeCourse self) -> bool"""
        return _libsedml.SedUniformTimeCourse_isSetOutputStartTime(self)

    def isSetOutputEndTime(self):
        """isSetOutputEndTime(SedUniformTimeCourse self) -> bool"""
        return _libsedml.SedUniformTimeCourse_isSetOutputEndTime(self)

    def isSetNumberOfPoints(self):
        """isSetNumberOfPoints(SedUniformTimeCourse self) -> bool"""
        return _libsedml.SedUniformTimeCourse_isSetNumberOfPoints(self)

    def isSetNumberOfSteps(self):
        """isSetNumberOfSteps(SedUniformTimeCourse self) -> bool"""
        return _libsedml.SedUniformTimeCourse_isSetNumberOfSteps(self)

    def setInitialTime(self, initialTime):
        """setInitialTime(SedUniformTimeCourse self, double initialTime) -> int"""
        return _libsedml.SedUniformTimeCourse_setInitialTime(self, initialTime)

    def setOutputStartTime(self, outputStartTime):
        """setOutputStartTime(SedUniformTimeCourse self, double outputStartTime) -> int"""
        return _libsedml.SedUniformTimeCourse_setOutputStartTime(self, outputStartTime)

    def setOutputEndTime(self, outputEndTime):
        """setOutputEndTime(SedUniformTimeCourse self, double outputEndTime) -> int"""
        return _libsedml.SedUniformTimeCourse_setOutputEndTime(self, outputEndTime)

    def setNumberOfPoints(self, numberOfPoints):
        """setNumberOfPoints(SedUniformTimeCourse self, int numberOfPoints) -> int"""
        return _libsedml.SedUniformTimeCourse_setNumberOfPoints(self, numberOfPoints)

    def setNumberOfSteps(self, numberOfSteps):
        """setNumberOfSteps(SedUniformTimeCourse self, int numberOfSteps) -> int"""
        return _libsedml.SedUniformTimeCourse_setNumberOfSteps(self, numberOfSteps)

    def unsetInitialTime(self):
        """unsetInitialTime(SedUniformTimeCourse self) -> int"""
        return _libsedml.SedUniformTimeCourse_unsetInitialTime(self)

    def unsetOutputStartTime(self):
        """unsetOutputStartTime(SedUniformTimeCourse self) -> int"""
        return _libsedml.SedUniformTimeCourse_unsetOutputStartTime(self)

    def unsetOutputEndTime(self):
        """unsetOutputEndTime(SedUniformTimeCourse self) -> int"""
        return _libsedml.SedUniformTimeCourse_unsetOutputEndTime(self)

    def unsetNumberOfPoints(self):
        """unsetNumberOfPoints(SedUniformTimeCourse self) -> int"""
        return _libsedml.SedUniformTimeCourse_unsetNumberOfPoints(self)

    def unsetNumberOfSteps(self):
        """unsetNumberOfSteps(SedUniformTimeCourse self) -> int"""
        return _libsedml.SedUniformTimeCourse_unsetNumberOfSteps(self)

    def getElementName(self):
        """getElementName(SedUniformTimeCourse self) -> string"""
        return _libsedml.SedUniformTimeCourse_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedUniformTimeCourse self) -> int"""
        return _libsedml.SedUniformTimeCourse_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedUniformTimeCourse self) -> bool"""
        return _libsedml.SedUniformTimeCourse_hasRequiredAttributes(self)


_libsedml.SedUniformTimeCourse_swigregister(SedUniformTimeCourse)

class SedAlgorithm(SedBase):
    """Proxy of C++ SedAlgorithm class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedAlgorithm self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedAlgorithm
        __init__(SedAlgorithm self, SedNamespaces sedmlns) -> SedAlgorithm
        __init__(SedAlgorithm self, SedAlgorithm orig) -> SedAlgorithm
        """
        _libsedml.SedAlgorithm_swiginit(self, _libsedml.new_SedAlgorithm(*args))

    def clone(self):
        """clone(SedAlgorithm self) -> SedAlgorithm"""
        return _libsedml.SedAlgorithm_clone(self)

    __swig_destroy__ = _libsedml.delete_SedAlgorithm

    def getKisaoID(self):
        """getKisaoID(SedAlgorithm self) -> string"""
        return _libsedml.SedAlgorithm_getKisaoID(self)

    def isSetKisaoID(self):
        """isSetKisaoID(SedAlgorithm self) -> bool"""
        return _libsedml.SedAlgorithm_isSetKisaoID(self)

    def unsetKisaoID(self):
        """unsetKisaoID(SedAlgorithm self) -> int"""
        return _libsedml.SedAlgorithm_unsetKisaoID(self)

    def getListOfAlgorithmParameters(self, *args):
        """
        getListOfAlgorithmParameters(SedAlgorithm self) -> SedListOfAlgorithmParameters
        getListOfAlgorithmParameters(SedAlgorithm self) -> SedListOfAlgorithmParameters
        """
        return _libsedml.SedAlgorithm_getListOfAlgorithmParameters(self, *args)

    def getAlgorithmParameter(self, *args):
        """
        getAlgorithmParameter(SedAlgorithm self, unsigned int n) -> SedAlgorithmParameter
        getAlgorithmParameter(SedAlgorithm self, unsigned int n) -> SedAlgorithmParameter
        """
        return _libsedml.SedAlgorithm_getAlgorithmParameter(self, *args)

    def addAlgorithmParameter(self, sap):
        """addAlgorithmParameter(SedAlgorithm self, SedAlgorithmParameter sap) -> int"""
        return _libsedml.SedAlgorithm_addAlgorithmParameter(self, sap)

    def getNumAlgorithmParameters(self):
        """getNumAlgorithmParameters(SedAlgorithm self) -> unsigned int"""
        return _libsedml.SedAlgorithm_getNumAlgorithmParameters(self)

    def createAlgorithmParameter(self):
        """createAlgorithmParameter(SedAlgorithm self) -> SedAlgorithmParameter"""
        return _libsedml.SedAlgorithm_createAlgorithmParameter(self)

    def removeAlgorithmParameter(self, n):
        """removeAlgorithmParameter(SedAlgorithm self, unsigned int n) -> SedAlgorithmParameter"""
        return _libsedml.SedAlgorithm_removeAlgorithmParameter(self, n)

    def getElementName(self):
        """getElementName(SedAlgorithm self) -> string"""
        return _libsedml.SedAlgorithm_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedAlgorithm self) -> int"""
        return _libsedml.SedAlgorithm_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedAlgorithm self) -> bool"""
        return _libsedml.SedAlgorithm_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedAlgorithm self)"""
        return _libsedml.SedAlgorithm_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedAlgorithm self, string id) -> SedBase"""
        return _libsedml.SedAlgorithm_getElementBySId(self, id)

    def getKisaoIDasInt(self):
        """getKisaoIDasInt(SedAlgorithm self) -> int"""
        return _libsedml.SedAlgorithm_getKisaoIDasInt(self)

    def setKisaoID(self, *args):
        """
        setKisaoID(SedAlgorithm self, string kisaoID) -> int
        setKisaoID(SedAlgorithm self, int kisaoID) -> int
        """
        return _libsedml.SedAlgorithm_setKisaoID(self, *args)


_libsedml.SedAlgorithm_swigregister(SedAlgorithm)

class SedAbstractTask(SedBase):
    """Proxy of C++ SedAbstractTask class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedAbstractTask self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedAbstractTask
        __init__(SedAbstractTask self, SedNamespaces sedmlns) -> SedAbstractTask
        __init__(SedAbstractTask self, SedAbstractTask orig) -> SedAbstractTask
        """
        _libsedml.SedAbstractTask_swiginit(self, _libsedml.new_SedAbstractTask(*args))

    def clone(self):
        """clone(SedAbstractTask self) -> SedAbstractTask"""
        return _libsedml.SedAbstractTask_clone(self)

    __swig_destroy__ = _libsedml.delete_SedAbstractTask

    def getId(self):
        """getId(SedAbstractTask self) -> string"""
        return _libsedml.SedAbstractTask_getId(self)

    def getName(self):
        """getName(SedAbstractTask self) -> string"""
        return _libsedml.SedAbstractTask_getName(self)

    def isSetId(self):
        """isSetId(SedAbstractTask self) -> bool"""
        return _libsedml.SedAbstractTask_isSetId(self)

    def isSetName(self):
        """isSetName(SedAbstractTask self) -> bool"""
        return _libsedml.SedAbstractTask_isSetName(self)

    def setId(self, id):
        """setId(SedAbstractTask self, string id) -> int"""
        return _libsedml.SedAbstractTask_setId(self, id)

    def setName(self, name):
        """setName(SedAbstractTask self, string name) -> int"""
        return _libsedml.SedAbstractTask_setName(self, name)

    def unsetId(self):
        """unsetId(SedAbstractTask self) -> int"""
        return _libsedml.SedAbstractTask_unsetId(self)

    def unsetName(self):
        """unsetName(SedAbstractTask self) -> int"""
        return _libsedml.SedAbstractTask_unsetName(self)

    def isSedTask(self):
        """isSedTask(SedAbstractTask self) -> bool"""
        return _libsedml.SedAbstractTask_isSedTask(self)

    def isSedRepeatedTask(self):
        """isSedRepeatedTask(SedAbstractTask self) -> bool"""
        return _libsedml.SedAbstractTask_isSedRepeatedTask(self)

    def isSedParameterEstimationTask(self):
        """isSedParameterEstimationTask(SedAbstractTask self) -> bool"""
        return _libsedml.SedAbstractTask_isSedParameterEstimationTask(self)

    def isSedSimpleRepeatedTask(self):
        """isSedSimpleRepeatedTask(SedAbstractTask self) -> bool"""
        return _libsedml.SedAbstractTask_isSedSimpleRepeatedTask(self)

    def getElementName(self):
        """getElementName(SedAbstractTask self) -> string"""
        return _libsedml.SedAbstractTask_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedAbstractTask self, string name)"""
        return _libsedml.SedAbstractTask_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedAbstractTask self) -> int"""
        return _libsedml.SedAbstractTask_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedAbstractTask self) -> bool"""
        return _libsedml.SedAbstractTask_hasRequiredAttributes(self)


_libsedml.SedAbstractTask_swigregister(SedAbstractTask)

class SedListOfTasks(SedListOf):
    """Proxy of C++ SedListOfTasks class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfTasks self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfTasks
        __init__(SedListOfTasks self, SedNamespaces sedmlns) -> SedListOfTasks
        __init__(SedListOfTasks self, SedListOfTasks orig) -> SedListOfTasks
        """
        _libsedml.SedListOfTasks_swiginit(self, _libsedml.new_SedListOfTasks(*args))

    def clone(self):
        """clone(SedListOfTasks self) -> SedListOfTasks"""
        return _libsedml.SedListOfTasks_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfTasks

    def get(self, *args):
        """
        get(SedListOfTasks self, unsigned int n) -> SedAbstractTask
        get(SedListOfTasks self, unsigned int n) -> SedAbstractTask
        get(SedListOfTasks self, string sid) -> SedAbstractTask
        get(SedListOfTasks self, string sid) -> SedAbstractTask
        """
        return _libsedml.SedListOfTasks_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfTasks self, unsigned int n) -> SedAbstractTask
        remove(SedListOfTasks self, string sid) -> SedAbstractTask
        """
        return _libsedml.SedListOfTasks_remove(self, *args)

    def addAbstractTask(self, sat):
        """addAbstractTask(SedListOfTasks self, SedAbstractTask sat) -> int"""
        return _libsedml.SedListOfTasks_addAbstractTask(self, sat)

    def getNumAbstractTasks(self):
        """getNumAbstractTasks(SedListOfTasks self) -> unsigned int"""
        return _libsedml.SedListOfTasks_getNumAbstractTasks(self)

    def createTask(self):
        """createTask(SedListOfTasks self) -> SedTask"""
        return _libsedml.SedListOfTasks_createTask(self)

    def createRepeatedTask(self):
        """createRepeatedTask(SedListOfTasks self) -> SedRepeatedTask"""
        return _libsedml.SedListOfTasks_createRepeatedTask(self)

    def createParameterEstimationTask(self):
        """createParameterEstimationTask(SedListOfTasks self) -> SedParameterEstimationTask"""
        return _libsedml.SedListOfTasks_createParameterEstimationTask(self)

    def createSimpleRepeatedTask(self):
        """createSimpleRepeatedTask(SedListOfTasks self) -> SedSimpleRepeatedTask"""
        return _libsedml.SedListOfTasks_createSimpleRepeatedTask(self)

    def getElementName(self):
        """getElementName(SedListOfTasks self) -> string"""
        return _libsedml.SedListOfTasks_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedListOfTasks self, string name)"""
        return _libsedml.SedListOfTasks_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedListOfTasks self) -> int"""
        return _libsedml.SedListOfTasks_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfTasks self) -> int"""
        return _libsedml.SedListOfTasks_getItemTypeCode(self)


_libsedml.SedListOfTasks_swigregister(SedListOfTasks)

class SedTask(SedAbstractTask):
    """Proxy of C++ SedTask class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedTask self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedTask
        __init__(SedTask self, SedNamespaces sedmlns) -> SedTask
        __init__(SedTask self, SedTask orig) -> SedTask
        """
        _libsedml.SedTask_swiginit(self, _libsedml.new_SedTask(*args))

    def clone(self):
        """clone(SedTask self) -> SedTask"""
        return _libsedml.SedTask_clone(self)

    __swig_destroy__ = _libsedml.delete_SedTask

    def getModelReference(self):
        """getModelReference(SedTask self) -> string"""
        return _libsedml.SedTask_getModelReference(self)

    def getSimulationReference(self):
        """getSimulationReference(SedTask self) -> string"""
        return _libsedml.SedTask_getSimulationReference(self)

    def isSetModelReference(self):
        """isSetModelReference(SedTask self) -> bool"""
        return _libsedml.SedTask_isSetModelReference(self)

    def isSetSimulationReference(self):
        """isSetSimulationReference(SedTask self) -> bool"""
        return _libsedml.SedTask_isSetSimulationReference(self)

    def setModelReference(self, modelReference):
        """setModelReference(SedTask self, string modelReference) -> int"""
        return _libsedml.SedTask_setModelReference(self, modelReference)

    def setSimulationReference(self, simulationReference):
        """setSimulationReference(SedTask self, string simulationReference) -> int"""
        return _libsedml.SedTask_setSimulationReference(self, simulationReference)

    def unsetModelReference(self):
        """unsetModelReference(SedTask self) -> int"""
        return _libsedml.SedTask_unsetModelReference(self)

    def unsetSimulationReference(self):
        """unsetSimulationReference(SedTask self) -> int"""
        return _libsedml.SedTask_unsetSimulationReference(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedTask self, string oldid, string newid)"""
        return _libsedml.SedTask_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedTask self) -> string"""
        return _libsedml.SedTask_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedTask self) -> int"""
        return _libsedml.SedTask_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedTask self) -> bool"""
        return _libsedml.SedTask_hasRequiredAttributes(self)


_libsedml.SedTask_swigregister(SedTask)

class SedDataGenerator(SedBase):
    """Proxy of C++ SedDataGenerator class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedDataGenerator self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedDataGenerator
        __init__(SedDataGenerator self, SedNamespaces sedmlns) -> SedDataGenerator
        __init__(SedDataGenerator self, SedDataGenerator orig) -> SedDataGenerator
        """
        _libsedml.SedDataGenerator_swiginit(self, _libsedml.new_SedDataGenerator(*args))

    def clone(self):
        """clone(SedDataGenerator self) -> SedDataGenerator"""
        return _libsedml.SedDataGenerator_clone(self)

    __swig_destroy__ = _libsedml.delete_SedDataGenerator

    def getId(self):
        """getId(SedDataGenerator self) -> string"""
        return _libsedml.SedDataGenerator_getId(self)

    def getName(self):
        """getName(SedDataGenerator self) -> string"""
        return _libsedml.SedDataGenerator_getName(self)

    def isSetId(self):
        """isSetId(SedDataGenerator self) -> bool"""
        return _libsedml.SedDataGenerator_isSetId(self)

    def isSetName(self):
        """isSetName(SedDataGenerator self) -> bool"""
        return _libsedml.SedDataGenerator_isSetName(self)

    def setId(self, id):
        """setId(SedDataGenerator self, string id) -> int"""
        return _libsedml.SedDataGenerator_setId(self, id)

    def setName(self, name):
        """setName(SedDataGenerator self, string name) -> int"""
        return _libsedml.SedDataGenerator_setName(self, name)

    def unsetId(self):
        """unsetId(SedDataGenerator self) -> int"""
        return _libsedml.SedDataGenerator_unsetId(self)

    def unsetName(self):
        """unsetName(SedDataGenerator self) -> int"""
        return _libsedml.SedDataGenerator_unsetName(self)

    def getMath(self, *args):
        """
        getMath(SedDataGenerator self) -> ASTNode
        getMath(SedDataGenerator self) -> ASTNode
        """
        return _libsedml.SedDataGenerator_getMath(self, *args)

    def isSetMath(self):
        """isSetMath(SedDataGenerator self) -> bool"""
        return _libsedml.SedDataGenerator_isSetMath(self)

    def setMath(self, math):
        """setMath(SedDataGenerator self, ASTNode math) -> int"""
        return _libsedml.SedDataGenerator_setMath(self, math)

    def unsetMath(self):
        """unsetMath(SedDataGenerator self) -> int"""
        return _libsedml.SedDataGenerator_unsetMath(self)

    def getListOfVariables(self, *args):
        """
        getListOfVariables(SedDataGenerator self) -> SedListOfVariables
        getListOfVariables(SedDataGenerator self) -> SedListOfVariables
        """
        return _libsedml.SedDataGenerator_getListOfVariables(self, *args)

    def getVariable(self, *args):
        """
        getVariable(SedDataGenerator self, unsigned int n) -> SedVariable
        getVariable(SedDataGenerator self, unsigned int n) -> SedVariable
        getVariable(SedDataGenerator self, string sid) -> SedVariable
        getVariable(SedDataGenerator self, string sid) -> SedVariable
        """
        return _libsedml.SedDataGenerator_getVariable(self, *args)

    def getVariableByTaskReference(self, *args):
        """
        getVariableByTaskReference(SedDataGenerator self, string sid) -> SedVariable
        getVariableByTaskReference(SedDataGenerator self, string sid) -> SedVariable
        """
        return _libsedml.SedDataGenerator_getVariableByTaskReference(self, *args)

    def getVariableByModelReference(self, *args):
        """
        getVariableByModelReference(SedDataGenerator self, string sid) -> SedVariable
        getVariableByModelReference(SedDataGenerator self, string sid) -> SedVariable
        """
        return _libsedml.SedDataGenerator_getVariableByModelReference(self, *args)

    def addVariable(self, sv):
        """addVariable(SedDataGenerator self, SedVariable sv) -> int"""
        return _libsedml.SedDataGenerator_addVariable(self, sv)

    def getNumVariables(self):
        """getNumVariables(SedDataGenerator self) -> unsigned int"""
        return _libsedml.SedDataGenerator_getNumVariables(self)

    def createVariable(self):
        """createVariable(SedDataGenerator self) -> SedVariable"""
        return _libsedml.SedDataGenerator_createVariable(self)

    def createDependentVariable(self):
        """createDependentVariable(SedDataGenerator self) -> SedDependentVariable"""
        return _libsedml.SedDataGenerator_createDependentVariable(self)

    def removeVariable(self, *args):
        """
        removeVariable(SedDataGenerator self, unsigned int n) -> SedVariable
        removeVariable(SedDataGenerator self, string sid) -> SedVariable
        """
        return _libsedml.SedDataGenerator_removeVariable(self, *args)

    def getListOfParameters(self, *args):
        """
        getListOfParameters(SedDataGenerator self) -> SedListOfParameters
        getListOfParameters(SedDataGenerator self) -> SedListOfParameters
        """
        return _libsedml.SedDataGenerator_getListOfParameters(self, *args)

    def getParameter(self, *args):
        """
        getParameter(SedDataGenerator self, unsigned int n) -> SedParameter
        getParameter(SedDataGenerator self, unsigned int n) -> SedParameter
        getParameter(SedDataGenerator self, string sid) -> SedParameter
        getParameter(SedDataGenerator self, string sid) -> SedParameter
        """
        return _libsedml.SedDataGenerator_getParameter(self, *args)

    def addParameter(self, sp):
        """addParameter(SedDataGenerator self, SedParameter sp) -> int"""
        return _libsedml.SedDataGenerator_addParameter(self, sp)

    def getNumParameters(self):
        """getNumParameters(SedDataGenerator self) -> unsigned int"""
        return _libsedml.SedDataGenerator_getNumParameters(self)

    def createParameter(self):
        """createParameter(SedDataGenerator self) -> SedParameter"""
        return _libsedml.SedDataGenerator_createParameter(self)

    def removeParameter(self, *args):
        """
        removeParameter(SedDataGenerator self, unsigned int n) -> SedParameter
        removeParameter(SedDataGenerator self, string sid) -> SedParameter
        """
        return _libsedml.SedDataGenerator_removeParameter(self, *args)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedDataGenerator self, string oldid, string newid)"""
        return _libsedml.SedDataGenerator_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedDataGenerator self) -> string"""
        return _libsedml.SedDataGenerator_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedDataGenerator self) -> int"""
        return _libsedml.SedDataGenerator_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedDataGenerator self) -> bool"""
        return _libsedml.SedDataGenerator_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedDataGenerator self)"""
        return _libsedml.SedDataGenerator_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedDataGenerator self, string id) -> SedBase"""
        return _libsedml.SedDataGenerator_getElementBySId(self, id)


_libsedml.SedDataGenerator_swigregister(SedDataGenerator)

class SedListOfDataGenerators(SedListOf):
    """Proxy of C++ SedListOfDataGenerators class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfDataGenerators self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfDataGenerators
        __init__(SedListOfDataGenerators self, SedNamespaces sedmlns) -> SedListOfDataGenerators
        __init__(SedListOfDataGenerators self, SedListOfDataGenerators orig) -> SedListOfDataGenerators
        """
        _libsedml.SedListOfDataGenerators_swiginit(self, _libsedml.new_SedListOfDataGenerators(*args))

    def clone(self):
        """clone(SedListOfDataGenerators self) -> SedListOfDataGenerators"""
        return _libsedml.SedListOfDataGenerators_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfDataGenerators

    def get(self, *args):
        """
        get(SedListOfDataGenerators self, unsigned int n) -> SedDataGenerator
        get(SedListOfDataGenerators self, unsigned int n) -> SedDataGenerator
        get(SedListOfDataGenerators self, string sid) -> SedDataGenerator
        get(SedListOfDataGenerators self, string sid) -> SedDataGenerator
        """
        return _libsedml.SedListOfDataGenerators_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfDataGenerators self, unsigned int n) -> SedDataGenerator
        remove(SedListOfDataGenerators self, string sid) -> SedDataGenerator
        """
        return _libsedml.SedListOfDataGenerators_remove(self, *args)

    def addDataGenerator(self, sdg):
        """addDataGenerator(SedListOfDataGenerators self, SedDataGenerator sdg) -> int"""
        return _libsedml.SedListOfDataGenerators_addDataGenerator(self, sdg)

    def getNumDataGenerators(self):
        """getNumDataGenerators(SedListOfDataGenerators self) -> unsigned int"""
        return _libsedml.SedListOfDataGenerators_getNumDataGenerators(self)

    def createDataGenerator(self):
        """createDataGenerator(SedListOfDataGenerators self) -> SedDataGenerator"""
        return _libsedml.SedListOfDataGenerators_createDataGenerator(self)

    def getElementName(self):
        """getElementName(SedListOfDataGenerators self) -> string"""
        return _libsedml.SedListOfDataGenerators_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfDataGenerators self) -> int"""
        return _libsedml.SedListOfDataGenerators_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfDataGenerators self) -> int"""
        return _libsedml.SedListOfDataGenerators_getItemTypeCode(self)


_libsedml.SedListOfDataGenerators_swigregister(SedListOfDataGenerators)

class SedOutput(SedBase):
    """Proxy of C++ SedOutput class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedOutput self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedOutput
        __init__(SedOutput self, SedNamespaces sedmlns) -> SedOutput
        __init__(SedOutput self, SedOutput orig) -> SedOutput
        """
        _libsedml.SedOutput_swiginit(self, _libsedml.new_SedOutput(*args))

    def clone(self):
        """clone(SedOutput self) -> SedOutput"""
        return _libsedml.SedOutput_clone(self)

    __swig_destroy__ = _libsedml.delete_SedOutput

    def getId(self):
        """getId(SedOutput self) -> string"""
        return _libsedml.SedOutput_getId(self)

    def getName(self):
        """getName(SedOutput self) -> string"""
        return _libsedml.SedOutput_getName(self)

    def isSetId(self):
        """isSetId(SedOutput self) -> bool"""
        return _libsedml.SedOutput_isSetId(self)

    def isSetName(self):
        """isSetName(SedOutput self) -> bool"""
        return _libsedml.SedOutput_isSetName(self)

    def setId(self, id):
        """setId(SedOutput self, string id) -> int"""
        return _libsedml.SedOutput_setId(self, id)

    def setName(self, name):
        """setName(SedOutput self, string name) -> int"""
        return _libsedml.SedOutput_setName(self, name)

    def unsetId(self):
        """unsetId(SedOutput self) -> int"""
        return _libsedml.SedOutput_unsetId(self)

    def unsetName(self):
        """unsetName(SedOutput self) -> int"""
        return _libsedml.SedOutput_unsetName(self)

    def isSedReport(self):
        """isSedReport(SedOutput self) -> bool"""
        return _libsedml.SedOutput_isSedReport(self)

    def isSedPlot2D(self):
        """isSedPlot2D(SedOutput self) -> bool"""
        return _libsedml.SedOutput_isSedPlot2D(self)

    def isSedPlot3D(self):
        """isSedPlot3D(SedOutput self) -> bool"""
        return _libsedml.SedOutput_isSedPlot3D(self)

    def isSedFigure(self):
        """isSedFigure(SedOutput self) -> bool"""
        return _libsedml.SedOutput_isSedFigure(self)

    def isSedParameterEstimationResultPlot(self):
        """isSedParameterEstimationResultPlot(SedOutput self) -> bool"""
        return _libsedml.SedOutput_isSedParameterEstimationResultPlot(self)

    def getElementName(self):
        """getElementName(SedOutput self) -> string"""
        return _libsedml.SedOutput_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedOutput self, string name)"""
        return _libsedml.SedOutput_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedOutput self) -> int"""
        return _libsedml.SedOutput_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedOutput self) -> bool"""
        return _libsedml.SedOutput_hasRequiredAttributes(self)


_libsedml.SedOutput_swigregister(SedOutput)

class SedListOfOutputs(SedListOf):
    """Proxy of C++ SedListOfOutputs class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfOutputs self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfOutputs
        __init__(SedListOfOutputs self, SedNamespaces sedmlns) -> SedListOfOutputs
        __init__(SedListOfOutputs self, SedListOfOutputs orig) -> SedListOfOutputs
        """
        _libsedml.SedListOfOutputs_swiginit(self, _libsedml.new_SedListOfOutputs(*args))

    def clone(self):
        """clone(SedListOfOutputs self) -> SedListOfOutputs"""
        return _libsedml.SedListOfOutputs_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfOutputs

    def get(self, *args):
        """
        get(SedListOfOutputs self, unsigned int n) -> SedOutput
        get(SedListOfOutputs self, unsigned int n) -> SedOutput
        get(SedListOfOutputs self, string sid) -> SedOutput
        get(SedListOfOutputs self, string sid) -> SedOutput
        """
        return _libsedml.SedListOfOutputs_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfOutputs self, unsigned int n) -> SedOutput
        remove(SedListOfOutputs self, string sid) -> SedOutput
        """
        return _libsedml.SedListOfOutputs_remove(self, *args)

    def addOutput(self, so):
        """addOutput(SedListOfOutputs self, SedOutput so) -> int"""
        return _libsedml.SedListOfOutputs_addOutput(self, so)

    def getNumOutputs(self):
        """getNumOutputs(SedListOfOutputs self) -> unsigned int"""
        return _libsedml.SedListOfOutputs_getNumOutputs(self)

    def createReport(self):
        """createReport(SedListOfOutputs self) -> SedReport"""
        return _libsedml.SedListOfOutputs_createReport(self)

    def createPlot2D(self):
        """createPlot2D(SedListOfOutputs self) -> SedPlot2D"""
        return _libsedml.SedListOfOutputs_createPlot2D(self)

    def createPlot3D(self):
        """createPlot3D(SedListOfOutputs self) -> SedPlot3D"""
        return _libsedml.SedListOfOutputs_createPlot3D(self)

    def createFigure(self):
        """createFigure(SedListOfOutputs self) -> SedFigure"""
        return _libsedml.SedListOfOutputs_createFigure(self)

    def createParameterEstimationResultPlot(self):
        """createParameterEstimationResultPlot(SedListOfOutputs self) -> SedParameterEstimationResultPlot"""
        return _libsedml.SedListOfOutputs_createParameterEstimationResultPlot(self)

    def getElementName(self):
        """getElementName(SedListOfOutputs self) -> string"""
        return _libsedml.SedListOfOutputs_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedListOfOutputs self, string name)"""
        return _libsedml.SedListOfOutputs_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedListOfOutputs self) -> int"""
        return _libsedml.SedListOfOutputs_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfOutputs self) -> int"""
        return _libsedml.SedListOfOutputs_getItemTypeCode(self)


_libsedml.SedListOfOutputs_swigregister(SedListOfOutputs)

class SedPlot(SedOutput):
    """Proxy of C++ SedPlot class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedPlot self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedPlot
        __init__(SedPlot self, SedNamespaces sedmlns) -> SedPlot
        __init__(SedPlot self, SedPlot orig) -> SedPlot
        """
        _libsedml.SedPlot_swiginit(self, _libsedml.new_SedPlot(*args))

    def clone(self):
        """clone(SedPlot self) -> SedPlot"""
        return _libsedml.SedPlot_clone(self)

    __swig_destroy__ = _libsedml.delete_SedPlot

    def getLegend(self):
        """getLegend(SedPlot self) -> bool"""
        return _libsedml.SedPlot_getLegend(self)

    def getHeight(self):
        """getHeight(SedPlot self) -> double"""
        return _libsedml.SedPlot_getHeight(self)

    def getWidth(self):
        """getWidth(SedPlot self) -> double"""
        return _libsedml.SedPlot_getWidth(self)

    def isSetLegend(self):
        """isSetLegend(SedPlot self) -> bool"""
        return _libsedml.SedPlot_isSetLegend(self)

    def isSetHeight(self):
        """isSetHeight(SedPlot self) -> bool"""
        return _libsedml.SedPlot_isSetHeight(self)

    def isSetWidth(self):
        """isSetWidth(SedPlot self) -> bool"""
        return _libsedml.SedPlot_isSetWidth(self)

    def setLegend(self, legend):
        """setLegend(SedPlot self, bool legend) -> int"""
        return _libsedml.SedPlot_setLegend(self, legend)

    def setHeight(self, height):
        """setHeight(SedPlot self, double height) -> int"""
        return _libsedml.SedPlot_setHeight(self, height)

    def setWidth(self, width):
        """setWidth(SedPlot self, double width) -> int"""
        return _libsedml.SedPlot_setWidth(self, width)

    def unsetLegend(self):
        """unsetLegend(SedPlot self) -> int"""
        return _libsedml.SedPlot_unsetLegend(self)

    def unsetHeight(self):
        """unsetHeight(SedPlot self) -> int"""
        return _libsedml.SedPlot_unsetHeight(self)

    def unsetWidth(self):
        """unsetWidth(SedPlot self) -> int"""
        return _libsedml.SedPlot_unsetWidth(self)

    def getXAxis(self, *args):
        """
        getXAxis(SedPlot self) -> SedAxis
        getXAxis(SedPlot self) -> SedAxis
        """
        return _libsedml.SedPlot_getXAxis(self, *args)

    def getYAxis(self, *args):
        """
        getYAxis(SedPlot self) -> SedAxis
        getYAxis(SedPlot self) -> SedAxis
        """
        return _libsedml.SedPlot_getYAxis(self, *args)

    def isSetXAxis(self):
        """isSetXAxis(SedPlot self) -> bool"""
        return _libsedml.SedPlot_isSetXAxis(self)

    def isSetYAxis(self):
        """isSetYAxis(SedPlot self) -> bool"""
        return _libsedml.SedPlot_isSetYAxis(self)

    def setXAxis(self, xAxis):
        """setXAxis(SedPlot self, SedAxis xAxis) -> int"""
        return _libsedml.SedPlot_setXAxis(self, xAxis)

    def setYAxis(self, yAxis):
        """setYAxis(SedPlot self, SedAxis yAxis) -> int"""
        return _libsedml.SedPlot_setYAxis(self, yAxis)

    def createXAxis(self):
        """createXAxis(SedPlot self) -> SedAxis"""
        return _libsedml.SedPlot_createXAxis(self)

    def createYAxis(self):
        """createYAxis(SedPlot self) -> SedAxis"""
        return _libsedml.SedPlot_createYAxis(self)

    def unsetXAxis(self):
        """unsetXAxis(SedPlot self) -> int"""
        return _libsedml.SedPlot_unsetXAxis(self)

    def unsetYAxis(self):
        """unsetYAxis(SedPlot self) -> int"""
        return _libsedml.SedPlot_unsetYAxis(self)

    def getElementName(self):
        """getElementName(SedPlot self) -> string"""
        return _libsedml.SedPlot_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedPlot self) -> int"""
        return _libsedml.SedPlot_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedPlot self) -> bool"""
        return _libsedml.SedPlot_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedPlot self) -> bool"""
        return _libsedml.SedPlot_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedPlot self)"""
        return _libsedml.SedPlot_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedPlot self, string id) -> SedBase"""
        return _libsedml.SedPlot_getElementBySId(self, id)


_libsedml.SedPlot_swigregister(SedPlot)

class SedPlot2D(SedPlot):
    """Proxy of C++ SedPlot2D class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedPlot2D self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedPlot2D
        __init__(SedPlot2D self, SedNamespaces sedmlns) -> SedPlot2D
        __init__(SedPlot2D self, SedPlot2D orig) -> SedPlot2D
        """
        _libsedml.SedPlot2D_swiginit(self, _libsedml.new_SedPlot2D(*args))

    def clone(self):
        """clone(SedPlot2D self) -> SedPlot2D"""
        return _libsedml.SedPlot2D_clone(self)

    __swig_destroy__ = _libsedml.delete_SedPlot2D

    def getRightYAxis(self, *args):
        """
        getRightYAxis(SedPlot2D self) -> SedAxis
        getRightYAxis(SedPlot2D self) -> SedAxis
        """
        return _libsedml.SedPlot2D_getRightYAxis(self, *args)

    def isSetRightYAxis(self):
        """isSetRightYAxis(SedPlot2D self) -> bool"""
        return _libsedml.SedPlot2D_isSetRightYAxis(self)

    def setRightYAxis(self, rightYAxis):
        """setRightYAxis(SedPlot2D self, SedAxis rightYAxis) -> int"""
        return _libsedml.SedPlot2D_setRightYAxis(self, rightYAxis)

    def createRightYAxis(self):
        """createRightYAxis(SedPlot2D self) -> SedAxis"""
        return _libsedml.SedPlot2D_createRightYAxis(self)

    def unsetRightYAxis(self):
        """unsetRightYAxis(SedPlot2D self) -> int"""
        return _libsedml.SedPlot2D_unsetRightYAxis(self)

    def getListOfCurves(self, *args):
        """
        getListOfCurves(SedPlot2D self) -> SedListOfCurves
        getListOfCurves(SedPlot2D self) -> SedListOfCurves
        """
        return _libsedml.SedPlot2D_getListOfCurves(self, *args)

    def getCurve(self, *args):
        """
        getCurve(SedPlot2D self, unsigned int n) -> SedAbstractCurve
        getCurve(SedPlot2D self, unsigned int n) -> SedAbstractCurve
        getCurve(SedPlot2D self, string sid) -> SedAbstractCurve
        getCurve(SedPlot2D self, string sid) -> SedAbstractCurve
        """
        return _libsedml.SedPlot2D_getCurve(self, *args)

    def getCurveByStyle(self, *args):
        """
        getCurveByStyle(SedPlot2D self, string sid) -> SedAbstractCurve
        getCurveByStyle(SedPlot2D self, string sid) -> SedAbstractCurve
        """
        return _libsedml.SedPlot2D_getCurveByStyle(self, *args)

    def getCurveByXDataReference(self, *args):
        """
        getCurveByXDataReference(SedPlot2D self, string sid) -> SedAbstractCurve
        getCurveByXDataReference(SedPlot2D self, string sid) -> SedAbstractCurve
        """
        return _libsedml.SedPlot2D_getCurveByXDataReference(self, *args)

    def addCurve(self, sac):
        """addCurve(SedPlot2D self, SedAbstractCurve sac) -> int"""
        return _libsedml.SedPlot2D_addCurve(self, sac)

    def getNumCurves(self):
        """getNumCurves(SedPlot2D self) -> unsigned int"""
        return _libsedml.SedPlot2D_getNumCurves(self)

    def createCurve(self):
        """createCurve(SedPlot2D self) -> SedCurve"""
        return _libsedml.SedPlot2D_createCurve(self)

    def createShadedArea(self):
        """createShadedArea(SedPlot2D self) -> SedShadedArea"""
        return _libsedml.SedPlot2D_createShadedArea(self)

    def removeCurve(self, *args):
        """
        removeCurve(SedPlot2D self, unsigned int n) -> SedAbstractCurve
        removeCurve(SedPlot2D self, string sid) -> SedAbstractCurve
        """
        return _libsedml.SedPlot2D_removeCurve(self, *args)

    def getElementName(self):
        """getElementName(SedPlot2D self) -> string"""
        return _libsedml.SedPlot2D_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedPlot2D self) -> int"""
        return _libsedml.SedPlot2D_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedPlot2D self) -> bool"""
        return _libsedml.SedPlot2D_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedPlot2D self) -> bool"""
        return _libsedml.SedPlot2D_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedPlot2D self)"""
        return _libsedml.SedPlot2D_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedPlot2D self, string id) -> SedBase"""
        return _libsedml.SedPlot2D_getElementBySId(self, id)


_libsedml.SedPlot2D_swigregister(SedPlot2D)

class SedPlot3D(SedPlot):
    """Proxy of C++ SedPlot3D class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedPlot3D self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedPlot3D
        __init__(SedPlot3D self, SedNamespaces sedmlns) -> SedPlot3D
        __init__(SedPlot3D self, SedPlot3D orig) -> SedPlot3D
        """
        _libsedml.SedPlot3D_swiginit(self, _libsedml.new_SedPlot3D(*args))

    def clone(self):
        """clone(SedPlot3D self) -> SedPlot3D"""
        return _libsedml.SedPlot3D_clone(self)

    __swig_destroy__ = _libsedml.delete_SedPlot3D

    def getZAxis(self, *args):
        """
        getZAxis(SedPlot3D self) -> SedAxis
        getZAxis(SedPlot3D self) -> SedAxis
        """
        return _libsedml.SedPlot3D_getZAxis(self, *args)

    def isSetZAxis(self):
        """isSetZAxis(SedPlot3D self) -> bool"""
        return _libsedml.SedPlot3D_isSetZAxis(self)

    def setZAxis(self, zAxis):
        """setZAxis(SedPlot3D self, SedAxis zAxis) -> int"""
        return _libsedml.SedPlot3D_setZAxis(self, zAxis)

    def createZAxis(self):
        """createZAxis(SedPlot3D self) -> SedAxis"""
        return _libsedml.SedPlot3D_createZAxis(self)

    def unsetZAxis(self):
        """unsetZAxis(SedPlot3D self) -> int"""
        return _libsedml.SedPlot3D_unsetZAxis(self)

    def getListOfSurfaces(self, *args):
        """
        getListOfSurfaces(SedPlot3D self) -> SedListOfSurfaces
        getListOfSurfaces(SedPlot3D self) -> SedListOfSurfaces
        """
        return _libsedml.SedPlot3D_getListOfSurfaces(self, *args)

    def getSurface(self, *args):
        """
        getSurface(SedPlot3D self, unsigned int n) -> SedSurface
        getSurface(SedPlot3D self, unsigned int n) -> SedSurface
        getSurface(SedPlot3D self, string sid) -> SedSurface
        getSurface(SedPlot3D self, string sid) -> SedSurface
        """
        return _libsedml.SedPlot3D_getSurface(self, *args)

    def getSurfaceByXDataReference(self, *args):
        """
        getSurfaceByXDataReference(SedPlot3D self, string sid) -> SedSurface
        getSurfaceByXDataReference(SedPlot3D self, string sid) -> SedSurface
        """
        return _libsedml.SedPlot3D_getSurfaceByXDataReference(self, *args)

    def getSurfaceByYDataReference(self, *args):
        """
        getSurfaceByYDataReference(SedPlot3D self, string sid) -> SedSurface
        getSurfaceByYDataReference(SedPlot3D self, string sid) -> SedSurface
        """
        return _libsedml.SedPlot3D_getSurfaceByYDataReference(self, *args)

    def getSurfaceByZDataReference(self, *args):
        """
        getSurfaceByZDataReference(SedPlot3D self, string sid) -> SedSurface
        getSurfaceByZDataReference(SedPlot3D self, string sid) -> SedSurface
        """
        return _libsedml.SedPlot3D_getSurfaceByZDataReference(self, *args)

    def getSurfaceByStyle(self, *args):
        """
        getSurfaceByStyle(SedPlot3D self, string sid) -> SedSurface
        getSurfaceByStyle(SedPlot3D self, string sid) -> SedSurface
        """
        return _libsedml.SedPlot3D_getSurfaceByStyle(self, *args)

    def addSurface(self, ss):
        """addSurface(SedPlot3D self, SedSurface ss) -> int"""
        return _libsedml.SedPlot3D_addSurface(self, ss)

    def getNumSurfaces(self):
        """getNumSurfaces(SedPlot3D self) -> unsigned int"""
        return _libsedml.SedPlot3D_getNumSurfaces(self)

    def createSurface(self):
        """createSurface(SedPlot3D self) -> SedSurface"""
        return _libsedml.SedPlot3D_createSurface(self)

    def removeSurface(self, *args):
        """
        removeSurface(SedPlot3D self, unsigned int n) -> SedSurface
        removeSurface(SedPlot3D self, string sid) -> SedSurface
        """
        return _libsedml.SedPlot3D_removeSurface(self, *args)

    def getElementName(self):
        """getElementName(SedPlot3D self) -> string"""
        return _libsedml.SedPlot3D_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedPlot3D self) -> int"""
        return _libsedml.SedPlot3D_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedPlot3D self) -> bool"""
        return _libsedml.SedPlot3D_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedPlot3D self) -> bool"""
        return _libsedml.SedPlot3D_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedPlot3D self)"""
        return _libsedml.SedPlot3D_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedPlot3D self, string id) -> SedBase"""
        return _libsedml.SedPlot3D_getElementBySId(self, id)


_libsedml.SedPlot3D_swigregister(SedPlot3D)

class SedAbstractCurve(SedBase):
    """Proxy of C++ SedAbstractCurve class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedAbstractCurve self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedAbstractCurve
        __init__(SedAbstractCurve self, SedNamespaces sedmlns) -> SedAbstractCurve
        __init__(SedAbstractCurve self, SedAbstractCurve orig) -> SedAbstractCurve
        """
        _libsedml.SedAbstractCurve_swiginit(self, _libsedml.new_SedAbstractCurve(*args))

    def clone(self):
        """clone(SedAbstractCurve self) -> SedAbstractCurve"""
        return _libsedml.SedAbstractCurve_clone(self)

    __swig_destroy__ = _libsedml.delete_SedAbstractCurve

    def getId(self):
        """getId(SedAbstractCurve self) -> string"""
        return _libsedml.SedAbstractCurve_getId(self)

    def getName(self):
        """getName(SedAbstractCurve self) -> string"""
        return _libsedml.SedAbstractCurve_getName(self)

    def getLogX(self):
        """getLogX(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_getLogX(self)

    def getOrder(self):
        """getOrder(SedAbstractCurve self) -> int"""
        return _libsedml.SedAbstractCurve_getOrder(self)

    def getStyle(self):
        """getStyle(SedAbstractCurve self) -> string"""
        return _libsedml.SedAbstractCurve_getStyle(self)

    def getYAxis(self):
        """getYAxis(SedAbstractCurve self) -> string"""
        return _libsedml.SedAbstractCurve_getYAxis(self)

    def getXDataReference(self):
        """getXDataReference(SedAbstractCurve self) -> string"""
        return _libsedml.SedAbstractCurve_getXDataReference(self)

    def isSetId(self):
        """isSetId(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_isSetId(self)

    def isSetName(self):
        """isSetName(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_isSetName(self)

    def isSetLogX(self):
        """isSetLogX(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_isSetLogX(self)

    def isSetOrder(self):
        """isSetOrder(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_isSetOrder(self)

    def isSetStyle(self):
        """isSetStyle(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_isSetStyle(self)

    def isSetYAxis(self):
        """isSetYAxis(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_isSetYAxis(self)

    def isSetXDataReference(self):
        """isSetXDataReference(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_isSetXDataReference(self)

    def setId(self, id):
        """setId(SedAbstractCurve self, string id) -> int"""
        return _libsedml.SedAbstractCurve_setId(self, id)

    def setName(self, name):
        """setName(SedAbstractCurve self, string name) -> int"""
        return _libsedml.SedAbstractCurve_setName(self, name)

    def setLogX(self, logX):
        """setLogX(SedAbstractCurve self, bool logX) -> int"""
        return _libsedml.SedAbstractCurve_setLogX(self, logX)

    def setOrder(self, order):
        """setOrder(SedAbstractCurve self, int order) -> int"""
        return _libsedml.SedAbstractCurve_setOrder(self, order)

    def setStyle(self, style):
        """setStyle(SedAbstractCurve self, string style) -> int"""
        return _libsedml.SedAbstractCurve_setStyle(self, style)

    def setYAxis(self, yAxis):
        """setYAxis(SedAbstractCurve self, string yAxis) -> int"""
        return _libsedml.SedAbstractCurve_setYAxis(self, yAxis)

    def setXDataReference(self, xDataReference):
        """setXDataReference(SedAbstractCurve self, string xDataReference) -> int"""
        return _libsedml.SedAbstractCurve_setXDataReference(self, xDataReference)

    def unsetId(self):
        """unsetId(SedAbstractCurve self) -> int"""
        return _libsedml.SedAbstractCurve_unsetId(self)

    def unsetName(self):
        """unsetName(SedAbstractCurve self) -> int"""
        return _libsedml.SedAbstractCurve_unsetName(self)

    def unsetLogX(self):
        """unsetLogX(SedAbstractCurve self) -> int"""
        return _libsedml.SedAbstractCurve_unsetLogX(self)

    def unsetOrder(self):
        """unsetOrder(SedAbstractCurve self) -> int"""
        return _libsedml.SedAbstractCurve_unsetOrder(self)

    def unsetStyle(self):
        """unsetStyle(SedAbstractCurve self) -> int"""
        return _libsedml.SedAbstractCurve_unsetStyle(self)

    def unsetYAxis(self):
        """unsetYAxis(SedAbstractCurve self) -> int"""
        return _libsedml.SedAbstractCurve_unsetYAxis(self)

    def unsetXDataReference(self):
        """unsetXDataReference(SedAbstractCurve self) -> int"""
        return _libsedml.SedAbstractCurve_unsetXDataReference(self)

    def isSedCurve(self):
        """isSedCurve(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_isSedCurve(self)

    def isSedShadedArea(self):
        """isSedShadedArea(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_isSedShadedArea(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedAbstractCurve self, string oldid, string newid)"""
        return _libsedml.SedAbstractCurve_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedAbstractCurve self) -> string"""
        return _libsedml.SedAbstractCurve_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedAbstractCurve self, string name)"""
        return _libsedml.SedAbstractCurve_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedAbstractCurve self) -> int"""
        return _libsedml.SedAbstractCurve_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedAbstractCurve self) -> bool"""
        return _libsedml.SedAbstractCurve_hasRequiredAttributes(self)


_libsedml.SedAbstractCurve_swigregister(SedAbstractCurve)

class SedListOfCurves(SedListOf):
    """Proxy of C++ SedListOfCurves class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfCurves self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfCurves
        __init__(SedListOfCurves self, SedNamespaces sedmlns) -> SedListOfCurves
        __init__(SedListOfCurves self, SedListOfCurves orig) -> SedListOfCurves
        """
        _libsedml.SedListOfCurves_swiginit(self, _libsedml.new_SedListOfCurves(*args))

    def clone(self):
        """clone(SedListOfCurves self) -> SedListOfCurves"""
        return _libsedml.SedListOfCurves_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfCurves

    def get(self, *args):
        """
        get(SedListOfCurves self, unsigned int n) -> SedAbstractCurve
        get(SedListOfCurves self, unsigned int n) -> SedAbstractCurve
        get(SedListOfCurves self, string sid) -> SedAbstractCurve
        get(SedListOfCurves self, string sid) -> SedAbstractCurve
        """
        return _libsedml.SedListOfCurves_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfCurves self, unsigned int n) -> SedAbstractCurve
        remove(SedListOfCurves self, string sid) -> SedAbstractCurve
        """
        return _libsedml.SedListOfCurves_remove(self, *args)

    def addCurve(self, sac):
        """addCurve(SedListOfCurves self, SedAbstractCurve sac) -> int"""
        return _libsedml.SedListOfCurves_addCurve(self, sac)

    def getNumCurves(self):
        """getNumCurves(SedListOfCurves self) -> unsigned int"""
        return _libsedml.SedListOfCurves_getNumCurves(self)

    def createCurve(self):
        """createCurve(SedListOfCurves self) -> SedCurve"""
        return _libsedml.SedListOfCurves_createCurve(self)

    def createShadedArea(self):
        """createShadedArea(SedListOfCurves self) -> SedShadedArea"""
        return _libsedml.SedListOfCurves_createShadedArea(self)

    def getByStyle(self, *args):
        """
        getByStyle(SedListOfCurves self, string sid) -> SedAbstractCurve
        getByStyle(SedListOfCurves self, string sid) -> SedAbstractCurve
        """
        return _libsedml.SedListOfCurves_getByStyle(self, *args)

    def getByXDataReference(self, *args):
        """
        getByXDataReference(SedListOfCurves self, string sid) -> SedAbstractCurve
        getByXDataReference(SedListOfCurves self, string sid) -> SedAbstractCurve
        """
        return _libsedml.SedListOfCurves_getByXDataReference(self, *args)

    def getElementName(self):
        """getElementName(SedListOfCurves self) -> string"""
        return _libsedml.SedListOfCurves_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfCurves self) -> int"""
        return _libsedml.SedListOfCurves_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfCurves self) -> int"""
        return _libsedml.SedListOfCurves_getItemTypeCode(self)


_libsedml.SedListOfCurves_swigregister(SedListOfCurves)

class SedCurve(SedAbstractCurve):
    """Proxy of C++ SedCurve class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedCurve self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedCurve
        __init__(SedCurve self, SedNamespaces sedmlns) -> SedCurve
        __init__(SedCurve self, SedCurve orig) -> SedCurve
        """
        _libsedml.SedCurve_swiginit(self, _libsedml.new_SedCurve(*args))

    def clone(self):
        """clone(SedCurve self) -> SedCurve"""
        return _libsedml.SedCurve_clone(self)

    __swig_destroy__ = _libsedml.delete_SedCurve

    def getLogY(self):
        """getLogY(SedCurve self) -> bool"""
        return _libsedml.SedCurve_getLogY(self)

    def getYDataReference(self):
        """getYDataReference(SedCurve self) -> string"""
        return _libsedml.SedCurve_getYDataReference(self)

    def getType(self):
        """getType(SedCurve self) -> CurveType_t"""
        return _libsedml.SedCurve_getType(self)

    def getTypeAsString(self):
        """getTypeAsString(SedCurve self) -> string"""
        return _libsedml.SedCurve_getTypeAsString(self)

    def getXErrorUpper(self):
        """getXErrorUpper(SedCurve self) -> string"""
        return _libsedml.SedCurve_getXErrorUpper(self)

    def getXErrorLower(self):
        """getXErrorLower(SedCurve self) -> string"""
        return _libsedml.SedCurve_getXErrorLower(self)

    def getYErrorUpper(self):
        """getYErrorUpper(SedCurve self) -> string"""
        return _libsedml.SedCurve_getYErrorUpper(self)

    def getYErrorLower(self):
        """getYErrorLower(SedCurve self) -> string"""
        return _libsedml.SedCurve_getYErrorLower(self)

    def isSetLogY(self):
        """isSetLogY(SedCurve self) -> bool"""
        return _libsedml.SedCurve_isSetLogY(self)

    def isSetYDataReference(self):
        """isSetYDataReference(SedCurve self) -> bool"""
        return _libsedml.SedCurve_isSetYDataReference(self)

    def isSetType(self):
        """isSetType(SedCurve self) -> bool"""
        return _libsedml.SedCurve_isSetType(self)

    def isSetXErrorUpper(self):
        """isSetXErrorUpper(SedCurve self) -> bool"""
        return _libsedml.SedCurve_isSetXErrorUpper(self)

    def isSetXErrorLower(self):
        """isSetXErrorLower(SedCurve self) -> bool"""
        return _libsedml.SedCurve_isSetXErrorLower(self)

    def isSetYErrorUpper(self):
        """isSetYErrorUpper(SedCurve self) -> bool"""
        return _libsedml.SedCurve_isSetYErrorUpper(self)

    def isSetYErrorLower(self):
        """isSetYErrorLower(SedCurve self) -> bool"""
        return _libsedml.SedCurve_isSetYErrorLower(self)

    def setLogY(self, logY):
        """setLogY(SedCurve self, bool logY) -> int"""
        return _libsedml.SedCurve_setLogY(self, logY)

    def setYDataReference(self, yDataReference):
        """setYDataReference(SedCurve self, string yDataReference) -> int"""
        return _libsedml.SedCurve_setYDataReference(self, yDataReference)

    def setType(self, *args):
        """
        setType(SedCurve self, CurveType_t const type) -> int
        setType(SedCurve self, string type) -> int
        """
        return _libsedml.SedCurve_setType(self, *args)

    def setXErrorUpper(self, xErrorUpper):
        """setXErrorUpper(SedCurve self, string xErrorUpper) -> int"""
        return _libsedml.SedCurve_setXErrorUpper(self, xErrorUpper)

    def setXErrorLower(self, xErrorLower):
        """setXErrorLower(SedCurve self, string xErrorLower) -> int"""
        return _libsedml.SedCurve_setXErrorLower(self, xErrorLower)

    def setYErrorUpper(self, yErrorUpper):
        """setYErrorUpper(SedCurve self, string yErrorUpper) -> int"""
        return _libsedml.SedCurve_setYErrorUpper(self, yErrorUpper)

    def setYErrorLower(self, yErrorLower):
        """setYErrorLower(SedCurve self, string yErrorLower) -> int"""
        return _libsedml.SedCurve_setYErrorLower(self, yErrorLower)

    def unsetLogY(self):
        """unsetLogY(SedCurve self) -> int"""
        return _libsedml.SedCurve_unsetLogY(self)

    def unsetYDataReference(self):
        """unsetYDataReference(SedCurve self) -> int"""
        return _libsedml.SedCurve_unsetYDataReference(self)

    def unsetType(self):
        """unsetType(SedCurve self) -> int"""
        return _libsedml.SedCurve_unsetType(self)

    def unsetXErrorUpper(self):
        """unsetXErrorUpper(SedCurve self) -> int"""
        return _libsedml.SedCurve_unsetXErrorUpper(self)

    def unsetXErrorLower(self):
        """unsetXErrorLower(SedCurve self) -> int"""
        return _libsedml.SedCurve_unsetXErrorLower(self)

    def unsetYErrorUpper(self):
        """unsetYErrorUpper(SedCurve self) -> int"""
        return _libsedml.SedCurve_unsetYErrorUpper(self)

    def unsetYErrorLower(self):
        """unsetYErrorLower(SedCurve self) -> int"""
        return _libsedml.SedCurve_unsetYErrorLower(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedCurve self, string oldid, string newid)"""
        return _libsedml.SedCurve_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedCurve self) -> string"""
        return _libsedml.SedCurve_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedCurve self) -> int"""
        return _libsedml.SedCurve_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedCurve self) -> bool"""
        return _libsedml.SedCurve_hasRequiredAttributes(self)


_libsedml.SedCurve_swigregister(SedCurve)

class SedSurface(SedBase):
    """Proxy of C++ SedSurface class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedSurface self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedSurface
        __init__(SedSurface self, SedNamespaces sedmlns) -> SedSurface
        __init__(SedSurface self, SedSurface orig) -> SedSurface
        """
        _libsedml.SedSurface_swiginit(self, _libsedml.new_SedSurface(*args))

    def clone(self):
        """clone(SedSurface self) -> SedSurface"""
        return _libsedml.SedSurface_clone(self)

    __swig_destroy__ = _libsedml.delete_SedSurface

    def getId(self):
        """getId(SedSurface self) -> string"""
        return _libsedml.SedSurface_getId(self)

    def getName(self):
        """getName(SedSurface self) -> string"""
        return _libsedml.SedSurface_getName(self)

    def getXDataReference(self):
        """getXDataReference(SedSurface self) -> string"""
        return _libsedml.SedSurface_getXDataReference(self)

    def getYDataReference(self):
        """getYDataReference(SedSurface self) -> string"""
        return _libsedml.SedSurface_getYDataReference(self)

    def getZDataReference(self):
        """getZDataReference(SedSurface self) -> string"""
        return _libsedml.SedSurface_getZDataReference(self)

    def getType(self):
        """getType(SedSurface self) -> SurfaceType_t"""
        return _libsedml.SedSurface_getType(self)

    def getTypeAsString(self):
        """getTypeAsString(SedSurface self) -> string"""
        return _libsedml.SedSurface_getTypeAsString(self)

    def getStyle(self):
        """getStyle(SedSurface self) -> string"""
        return _libsedml.SedSurface_getStyle(self)

    def getLogX(self):
        """getLogX(SedSurface self) -> bool"""
        return _libsedml.SedSurface_getLogX(self)

    def getLogY(self):
        """getLogY(SedSurface self) -> bool"""
        return _libsedml.SedSurface_getLogY(self)

    def getLogZ(self):
        """getLogZ(SedSurface self) -> bool"""
        return _libsedml.SedSurface_getLogZ(self)

    def getOrder(self):
        """getOrder(SedSurface self) -> int"""
        return _libsedml.SedSurface_getOrder(self)

    def isSetId(self):
        """isSetId(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetId(self)

    def isSetName(self):
        """isSetName(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetName(self)

    def isSetXDataReference(self):
        """isSetXDataReference(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetXDataReference(self)

    def isSetYDataReference(self):
        """isSetYDataReference(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetYDataReference(self)

    def isSetZDataReference(self):
        """isSetZDataReference(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetZDataReference(self)

    def isSetType(self):
        """isSetType(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetType(self)

    def isSetStyle(self):
        """isSetStyle(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetStyle(self)

    def isSetLogX(self):
        """isSetLogX(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetLogX(self)

    def isSetLogY(self):
        """isSetLogY(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetLogY(self)

    def isSetLogZ(self):
        """isSetLogZ(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetLogZ(self)

    def isSetOrder(self):
        """isSetOrder(SedSurface self) -> bool"""
        return _libsedml.SedSurface_isSetOrder(self)

    def setId(self, id):
        """setId(SedSurface self, string id) -> int"""
        return _libsedml.SedSurface_setId(self, id)

    def setName(self, name):
        """setName(SedSurface self, string name) -> int"""
        return _libsedml.SedSurface_setName(self, name)

    def setXDataReference(self, xDataReference):
        """setXDataReference(SedSurface self, string xDataReference) -> int"""
        return _libsedml.SedSurface_setXDataReference(self, xDataReference)

    def setYDataReference(self, yDataReference):
        """setYDataReference(SedSurface self, string yDataReference) -> int"""
        return _libsedml.SedSurface_setYDataReference(self, yDataReference)

    def setZDataReference(self, zDataReference):
        """setZDataReference(SedSurface self, string zDataReference) -> int"""
        return _libsedml.SedSurface_setZDataReference(self, zDataReference)

    def setType(self, *args):
        """
        setType(SedSurface self, SurfaceType_t const type) -> int
        setType(SedSurface self, string type) -> int
        """
        return _libsedml.SedSurface_setType(self, *args)

    def setStyle(self, style):
        """setStyle(SedSurface self, string style) -> int"""
        return _libsedml.SedSurface_setStyle(self, style)

    def setLogX(self, logX):
        """setLogX(SedSurface self, bool logX) -> int"""
        return _libsedml.SedSurface_setLogX(self, logX)

    def setLogY(self, logY):
        """setLogY(SedSurface self, bool logY) -> int"""
        return _libsedml.SedSurface_setLogY(self, logY)

    def setLogZ(self, logZ):
        """setLogZ(SedSurface self, bool logZ) -> int"""
        return _libsedml.SedSurface_setLogZ(self, logZ)

    def setOrder(self, order):
        """setOrder(SedSurface self, int order) -> int"""
        return _libsedml.SedSurface_setOrder(self, order)

    def unsetId(self):
        """unsetId(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetId(self)

    def unsetName(self):
        """unsetName(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetName(self)

    def unsetXDataReference(self):
        """unsetXDataReference(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetXDataReference(self)

    def unsetYDataReference(self):
        """unsetYDataReference(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetYDataReference(self)

    def unsetZDataReference(self):
        """unsetZDataReference(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetZDataReference(self)

    def unsetType(self):
        """unsetType(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetType(self)

    def unsetStyle(self):
        """unsetStyle(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetStyle(self)

    def unsetLogX(self):
        """unsetLogX(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetLogX(self)

    def unsetLogY(self):
        """unsetLogY(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetLogY(self)

    def unsetLogZ(self):
        """unsetLogZ(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetLogZ(self)

    def unsetOrder(self):
        """unsetOrder(SedSurface self) -> int"""
        return _libsedml.SedSurface_unsetOrder(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedSurface self, string oldid, string newid)"""
        return _libsedml.SedSurface_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedSurface self) -> string"""
        return _libsedml.SedSurface_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedSurface self) -> int"""
        return _libsedml.SedSurface_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedSurface self) -> bool"""
        return _libsedml.SedSurface_hasRequiredAttributes(self)


_libsedml.SedSurface_swigregister(SedSurface)

class SedListOfSurfaces(SedListOf):
    """Proxy of C++ SedListOfSurfaces class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfSurfaces self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfSurfaces
        __init__(SedListOfSurfaces self, SedNamespaces sedmlns) -> SedListOfSurfaces
        __init__(SedListOfSurfaces self, SedListOfSurfaces orig) -> SedListOfSurfaces
        """
        _libsedml.SedListOfSurfaces_swiginit(self, _libsedml.new_SedListOfSurfaces(*args))

    def clone(self):
        """clone(SedListOfSurfaces self) -> SedListOfSurfaces"""
        return _libsedml.SedListOfSurfaces_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfSurfaces

    def get(self, *args):
        """
        get(SedListOfSurfaces self, unsigned int n) -> SedSurface
        get(SedListOfSurfaces self, unsigned int n) -> SedSurface
        get(SedListOfSurfaces self, string sid) -> SedSurface
        get(SedListOfSurfaces self, string sid) -> SedSurface
        """
        return _libsedml.SedListOfSurfaces_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfSurfaces self, unsigned int n) -> SedSurface
        remove(SedListOfSurfaces self, string sid) -> SedSurface
        """
        return _libsedml.SedListOfSurfaces_remove(self, *args)

    def addSurface(self, ss):
        """addSurface(SedListOfSurfaces self, SedSurface ss) -> int"""
        return _libsedml.SedListOfSurfaces_addSurface(self, ss)

    def getNumSurfaces(self):
        """getNumSurfaces(SedListOfSurfaces self) -> unsigned int"""
        return _libsedml.SedListOfSurfaces_getNumSurfaces(self)

    def createSurface(self):
        """createSurface(SedListOfSurfaces self) -> SedSurface"""
        return _libsedml.SedListOfSurfaces_createSurface(self)

    def getByXDataReference(self, *args):
        """
        getByXDataReference(SedListOfSurfaces self, string sid) -> SedSurface
        getByXDataReference(SedListOfSurfaces self, string sid) -> SedSurface
        """
        return _libsedml.SedListOfSurfaces_getByXDataReference(self, *args)

    def getByYDataReference(self, *args):
        """
        getByYDataReference(SedListOfSurfaces self, string sid) -> SedSurface
        getByYDataReference(SedListOfSurfaces self, string sid) -> SedSurface
        """
        return _libsedml.SedListOfSurfaces_getByYDataReference(self, *args)

    def getByZDataReference(self, *args):
        """
        getByZDataReference(SedListOfSurfaces self, string sid) -> SedSurface
        getByZDataReference(SedListOfSurfaces self, string sid) -> SedSurface
        """
        return _libsedml.SedListOfSurfaces_getByZDataReference(self, *args)

    def getByStyle(self, *args):
        """
        getByStyle(SedListOfSurfaces self, string sid) -> SedSurface
        getByStyle(SedListOfSurfaces self, string sid) -> SedSurface
        """
        return _libsedml.SedListOfSurfaces_getByStyle(self, *args)

    def getElementName(self):
        """getElementName(SedListOfSurfaces self) -> string"""
        return _libsedml.SedListOfSurfaces_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfSurfaces self) -> int"""
        return _libsedml.SedListOfSurfaces_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfSurfaces self) -> int"""
        return _libsedml.SedListOfSurfaces_getItemTypeCode(self)


_libsedml.SedListOfSurfaces_swigregister(SedListOfSurfaces)

class SedDataSet(SedBase):
    """Proxy of C++ SedDataSet class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedDataSet self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedDataSet
        __init__(SedDataSet self, SedNamespaces sedmlns) -> SedDataSet
        __init__(SedDataSet self, SedDataSet orig) -> SedDataSet
        """
        _libsedml.SedDataSet_swiginit(self, _libsedml.new_SedDataSet(*args))

    def clone(self):
        """clone(SedDataSet self) -> SedDataSet"""
        return _libsedml.SedDataSet_clone(self)

    __swig_destroy__ = _libsedml.delete_SedDataSet

    def getId(self):
        """getId(SedDataSet self) -> string"""
        return _libsedml.SedDataSet_getId(self)

    def getLabel(self):
        """getLabel(SedDataSet self) -> string"""
        return _libsedml.SedDataSet_getLabel(self)

    def getName(self):
        """getName(SedDataSet self) -> string"""
        return _libsedml.SedDataSet_getName(self)

    def getDataReference(self):
        """getDataReference(SedDataSet self) -> string"""
        return _libsedml.SedDataSet_getDataReference(self)

    def isSetId(self):
        """isSetId(SedDataSet self) -> bool"""
        return _libsedml.SedDataSet_isSetId(self)

    def isSetLabel(self):
        """isSetLabel(SedDataSet self) -> bool"""
        return _libsedml.SedDataSet_isSetLabel(self)

    def isSetName(self):
        """isSetName(SedDataSet self) -> bool"""
        return _libsedml.SedDataSet_isSetName(self)

    def isSetDataReference(self):
        """isSetDataReference(SedDataSet self) -> bool"""
        return _libsedml.SedDataSet_isSetDataReference(self)

    def setId(self, id):
        """setId(SedDataSet self, string id) -> int"""
        return _libsedml.SedDataSet_setId(self, id)

    def setLabel(self, label):
        """setLabel(SedDataSet self, string label) -> int"""
        return _libsedml.SedDataSet_setLabel(self, label)

    def setName(self, name):
        """setName(SedDataSet self, string name) -> int"""
        return _libsedml.SedDataSet_setName(self, name)

    def setDataReference(self, dataReference):
        """setDataReference(SedDataSet self, string dataReference) -> int"""
        return _libsedml.SedDataSet_setDataReference(self, dataReference)

    def unsetId(self):
        """unsetId(SedDataSet self) -> int"""
        return _libsedml.SedDataSet_unsetId(self)

    def unsetLabel(self):
        """unsetLabel(SedDataSet self) -> int"""
        return _libsedml.SedDataSet_unsetLabel(self)

    def unsetName(self):
        """unsetName(SedDataSet self) -> int"""
        return _libsedml.SedDataSet_unsetName(self)

    def unsetDataReference(self):
        """unsetDataReference(SedDataSet self) -> int"""
        return _libsedml.SedDataSet_unsetDataReference(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedDataSet self, string oldid, string newid)"""
        return _libsedml.SedDataSet_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedDataSet self) -> string"""
        return _libsedml.SedDataSet_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedDataSet self) -> int"""
        return _libsedml.SedDataSet_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedDataSet self) -> bool"""
        return _libsedml.SedDataSet_hasRequiredAttributes(self)


_libsedml.SedDataSet_swigregister(SedDataSet)

class SedListOfDataSets(SedListOf):
    """Proxy of C++ SedListOfDataSets class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfDataSets self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfDataSets
        __init__(SedListOfDataSets self, SedNamespaces sedmlns) -> SedListOfDataSets
        __init__(SedListOfDataSets self, SedListOfDataSets orig) -> SedListOfDataSets
        """
        _libsedml.SedListOfDataSets_swiginit(self, _libsedml.new_SedListOfDataSets(*args))

    def clone(self):
        """clone(SedListOfDataSets self) -> SedListOfDataSets"""
        return _libsedml.SedListOfDataSets_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfDataSets

    def get(self, *args):
        """
        get(SedListOfDataSets self, unsigned int n) -> SedDataSet
        get(SedListOfDataSets self, unsigned int n) -> SedDataSet
        get(SedListOfDataSets self, string sid) -> SedDataSet
        get(SedListOfDataSets self, string sid) -> SedDataSet
        """
        return _libsedml.SedListOfDataSets_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfDataSets self, unsigned int n) -> SedDataSet
        remove(SedListOfDataSets self, string sid) -> SedDataSet
        """
        return _libsedml.SedListOfDataSets_remove(self, *args)

    def addDataSet(self, sds):
        """addDataSet(SedListOfDataSets self, SedDataSet sds) -> int"""
        return _libsedml.SedListOfDataSets_addDataSet(self, sds)

    def getNumDataSets(self):
        """getNumDataSets(SedListOfDataSets self) -> unsigned int"""
        return _libsedml.SedListOfDataSets_getNumDataSets(self)

    def createDataSet(self):
        """createDataSet(SedListOfDataSets self) -> SedDataSet"""
        return _libsedml.SedListOfDataSets_createDataSet(self)

    def getByDataReference(self, *args):
        """
        getByDataReference(SedListOfDataSets self, string sid) -> SedDataSet
        getByDataReference(SedListOfDataSets self, string sid) -> SedDataSet
        """
        return _libsedml.SedListOfDataSets_getByDataReference(self, *args)

    def getElementName(self):
        """getElementName(SedListOfDataSets self) -> string"""
        return _libsedml.SedListOfDataSets_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfDataSets self) -> int"""
        return _libsedml.SedListOfDataSets_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfDataSets self) -> int"""
        return _libsedml.SedListOfDataSets_getItemTypeCode(self)


_libsedml.SedListOfDataSets_swigregister(SedListOfDataSets)

class SedReport(SedOutput):
    """Proxy of C++ SedReport class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedReport self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedReport
        __init__(SedReport self, SedNamespaces sedmlns) -> SedReport
        __init__(SedReport self, SedReport orig) -> SedReport
        """
        _libsedml.SedReport_swiginit(self, _libsedml.new_SedReport(*args))

    def clone(self):
        """clone(SedReport self) -> SedReport"""
        return _libsedml.SedReport_clone(self)

    __swig_destroy__ = _libsedml.delete_SedReport

    def getListOfDataSets(self, *args):
        """
        getListOfDataSets(SedReport self) -> SedListOfDataSets
        getListOfDataSets(SedReport self) -> SedListOfDataSets
        """
        return _libsedml.SedReport_getListOfDataSets(self, *args)

    def getDataSet(self, *args):
        """
        getDataSet(SedReport self, unsigned int n) -> SedDataSet
        getDataSet(SedReport self, unsigned int n) -> SedDataSet
        getDataSet(SedReport self, string sid) -> SedDataSet
        getDataSet(SedReport self, string sid) -> SedDataSet
        """
        return _libsedml.SedReport_getDataSet(self, *args)

    def getDataSetByDataReference(self, *args):
        """
        getDataSetByDataReference(SedReport self, string sid) -> SedDataSet
        getDataSetByDataReference(SedReport self, string sid) -> SedDataSet
        """
        return _libsedml.SedReport_getDataSetByDataReference(self, *args)

    def addDataSet(self, sds):
        """addDataSet(SedReport self, SedDataSet sds) -> int"""
        return _libsedml.SedReport_addDataSet(self, sds)

    def getNumDataSets(self):
        """getNumDataSets(SedReport self) -> unsigned int"""
        return _libsedml.SedReport_getNumDataSets(self)

    def createDataSet(self):
        """createDataSet(SedReport self) -> SedDataSet"""
        return _libsedml.SedReport_createDataSet(self)

    def removeDataSet(self, *args):
        """
        removeDataSet(SedReport self, unsigned int n) -> SedDataSet
        removeDataSet(SedReport self, string sid) -> SedDataSet
        """
        return _libsedml.SedReport_removeDataSet(self, *args)

    def getElementName(self):
        """getElementName(SedReport self) -> string"""
        return _libsedml.SedReport_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedReport self) -> int"""
        return _libsedml.SedReport_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedReport self) -> bool"""
        return _libsedml.SedReport_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedReport self) -> bool"""
        return _libsedml.SedReport_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedReport self)"""
        return _libsedml.SedReport_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedReport self, string id) -> SedBase"""
        return _libsedml.SedReport_getElementBySId(self, id)


_libsedml.SedReport_swigregister(SedReport)

class SedAlgorithmParameter(SedBase):
    """Proxy of C++ SedAlgorithmParameter class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedAlgorithmParameter self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedAlgorithmParameter
        __init__(SedAlgorithmParameter self, SedNamespaces sedmlns) -> SedAlgorithmParameter
        __init__(SedAlgorithmParameter self, SedAlgorithmParameter orig) -> SedAlgorithmParameter
        """
        _libsedml.SedAlgorithmParameter_swiginit(self, _libsedml.new_SedAlgorithmParameter(*args))

    def clone(self):
        """clone(SedAlgorithmParameter self) -> SedAlgorithmParameter"""
        return _libsedml.SedAlgorithmParameter_clone(self)

    __swig_destroy__ = _libsedml.delete_SedAlgorithmParameter

    def getKisaoID(self):
        """getKisaoID(SedAlgorithmParameter self) -> string"""
        return _libsedml.SedAlgorithmParameter_getKisaoID(self)

    def getValue(self):
        """getValue(SedAlgorithmParameter self) -> string"""
        return _libsedml.SedAlgorithmParameter_getValue(self)

    def isSetKisaoID(self):
        """isSetKisaoID(SedAlgorithmParameter self) -> bool"""
        return _libsedml.SedAlgorithmParameter_isSetKisaoID(self)

    def isSetValue(self):
        """isSetValue(SedAlgorithmParameter self) -> bool"""
        return _libsedml.SedAlgorithmParameter_isSetValue(self)

    def setValue(self, value):
        """setValue(SedAlgorithmParameter self, string value) -> int"""
        return _libsedml.SedAlgorithmParameter_setValue(self, value)

    def unsetKisaoID(self):
        """unsetKisaoID(SedAlgorithmParameter self) -> int"""
        return _libsedml.SedAlgorithmParameter_unsetKisaoID(self)

    def unsetValue(self):
        """unsetValue(SedAlgorithmParameter self) -> int"""
        return _libsedml.SedAlgorithmParameter_unsetValue(self)

    def getListOfAlgorithmParameters(self, *args):
        """
        getListOfAlgorithmParameters(SedAlgorithmParameter self) -> SedListOfAlgorithmParameters
        getListOfAlgorithmParameters(SedAlgorithmParameter self) -> SedListOfAlgorithmParameters
        """
        return _libsedml.SedAlgorithmParameter_getListOfAlgorithmParameters(self, *args)

    def getAlgorithmParameter(self, *args):
        """
        getAlgorithmParameter(SedAlgorithmParameter self, unsigned int n) -> SedAlgorithmParameter
        getAlgorithmParameter(SedAlgorithmParameter self, unsigned int n) -> SedAlgorithmParameter
        """
        return _libsedml.SedAlgorithmParameter_getAlgorithmParameter(self, *args)

    def addAlgorithmParameter(self, sap1):
        """addAlgorithmParameter(SedAlgorithmParameter self, SedAlgorithmParameter sap1) -> int"""
        return _libsedml.SedAlgorithmParameter_addAlgorithmParameter(self, sap1)

    def getNumAlgorithmParameters(self):
        """getNumAlgorithmParameters(SedAlgorithmParameter self) -> unsigned int"""
        return _libsedml.SedAlgorithmParameter_getNumAlgorithmParameters(self)

    def createAlgorithmParameter(self):
        """createAlgorithmParameter(SedAlgorithmParameter self) -> SedAlgorithmParameter"""
        return _libsedml.SedAlgorithmParameter_createAlgorithmParameter(self)

    def removeAlgorithmParameter(self, n):
        """removeAlgorithmParameter(SedAlgorithmParameter self, unsigned int n) -> SedAlgorithmParameter"""
        return _libsedml.SedAlgorithmParameter_removeAlgorithmParameter(self, n)

    def getElementName(self):
        """getElementName(SedAlgorithmParameter self) -> string"""
        return _libsedml.SedAlgorithmParameter_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedAlgorithmParameter self) -> int"""
        return _libsedml.SedAlgorithmParameter_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedAlgorithmParameter self) -> bool"""
        return _libsedml.SedAlgorithmParameter_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedAlgorithmParameter self)"""
        return _libsedml.SedAlgorithmParameter_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedAlgorithmParameter self, string id) -> SedBase"""
        return _libsedml.SedAlgorithmParameter_getElementBySId(self, id)

    def getKisaoIDasInt(self):
        """getKisaoIDasInt(SedAlgorithmParameter self) -> int"""
        return _libsedml.SedAlgorithmParameter_getKisaoIDasInt(self)

    def setKisaoID(self, *args):
        """
        setKisaoID(SedAlgorithmParameter self, string kisaoID) -> int
        setKisaoID(SedAlgorithmParameter self, int kisaoID) -> int
        """
        return _libsedml.SedAlgorithmParameter_setKisaoID(self, *args)


_libsedml.SedAlgorithmParameter_swigregister(SedAlgorithmParameter)

class SedListOfAlgorithmParameters(SedListOf):
    """Proxy of C++ SedListOfAlgorithmParameters class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfAlgorithmParameters self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfAlgorithmParameters
        __init__(SedListOfAlgorithmParameters self, SedNamespaces sedmlns) -> SedListOfAlgorithmParameters
        __init__(SedListOfAlgorithmParameters self, SedListOfAlgorithmParameters orig) -> SedListOfAlgorithmParameters
        """
        _libsedml.SedListOfAlgorithmParameters_swiginit(self, _libsedml.new_SedListOfAlgorithmParameters(*args))

    def clone(self):
        """clone(SedListOfAlgorithmParameters self) -> SedListOfAlgorithmParameters"""
        return _libsedml.SedListOfAlgorithmParameters_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfAlgorithmParameters

    def get(self, *args):
        """
        get(SedListOfAlgorithmParameters self, unsigned int n) -> SedAlgorithmParameter
        get(SedListOfAlgorithmParameters self, unsigned int n) -> SedAlgorithmParameter
        get(SedListOfAlgorithmParameters self, string sid) -> SedAlgorithmParameter
        get(SedListOfAlgorithmParameters self, string sid) -> SedAlgorithmParameter
        """
        return _libsedml.SedListOfAlgorithmParameters_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfAlgorithmParameters self, unsigned int n) -> SedAlgorithmParameter
        remove(SedListOfAlgorithmParameters self, string sid) -> SedAlgorithmParameter
        """
        return _libsedml.SedListOfAlgorithmParameters_remove(self, *args)

    def addAlgorithmParameter(self, sap):
        """addAlgorithmParameter(SedListOfAlgorithmParameters self, SedAlgorithmParameter sap) -> int"""
        return _libsedml.SedListOfAlgorithmParameters_addAlgorithmParameter(self, sap)

    def getNumAlgorithmParameters(self):
        """getNumAlgorithmParameters(SedListOfAlgorithmParameters self) -> unsigned int"""
        return _libsedml.SedListOfAlgorithmParameters_getNumAlgorithmParameters(self)

    def createAlgorithmParameter(self):
        """createAlgorithmParameter(SedListOfAlgorithmParameters self) -> SedAlgorithmParameter"""
        return _libsedml.SedListOfAlgorithmParameters_createAlgorithmParameter(self)

    def getElementName(self):
        """getElementName(SedListOfAlgorithmParameters self) -> string"""
        return _libsedml.SedListOfAlgorithmParameters_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfAlgorithmParameters self) -> int"""
        return _libsedml.SedListOfAlgorithmParameters_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfAlgorithmParameters self) -> int"""
        return _libsedml.SedListOfAlgorithmParameters_getItemTypeCode(self)


_libsedml.SedListOfAlgorithmParameters_swigregister(SedListOfAlgorithmParameters)

class SedRange(SedBase):
    """Proxy of C++ SedRange class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedRange self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedRange
        __init__(SedRange self, SedNamespaces sedmlns) -> SedRange
        __init__(SedRange self, SedRange orig) -> SedRange
        """
        _libsedml.SedRange_swiginit(self, _libsedml.new_SedRange(*args))

    def clone(self):
        """clone(SedRange self) -> SedRange"""
        return _libsedml.SedRange_clone(self)

    __swig_destroy__ = _libsedml.delete_SedRange

    def getId(self):
        """getId(SedRange self) -> string"""
        return _libsedml.SedRange_getId(self)

    def isSetId(self):
        """isSetId(SedRange self) -> bool"""
        return _libsedml.SedRange_isSetId(self)

    def setId(self, id):
        """setId(SedRange self, string id) -> int"""
        return _libsedml.SedRange_setId(self, id)

    def unsetId(self):
        """unsetId(SedRange self) -> int"""
        return _libsedml.SedRange_unsetId(self)

    def isSedUniformRange(self):
        """isSedUniformRange(SedRange self) -> bool"""
        return _libsedml.SedRange_isSedUniformRange(self)

    def isSedVectorRange(self):
        """isSedVectorRange(SedRange self) -> bool"""
        return _libsedml.SedRange_isSedVectorRange(self)

    def isSedFunctionalRange(self):
        """isSedFunctionalRange(SedRange self) -> bool"""
        return _libsedml.SedRange_isSedFunctionalRange(self)

    def isSedDataRange(self):
        """isSedDataRange(SedRange self) -> bool"""
        return _libsedml.SedRange_isSedDataRange(self)

    def getElementName(self):
        """getElementName(SedRange self) -> string"""
        return _libsedml.SedRange_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedRange self, string name)"""
        return _libsedml.SedRange_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedRange self) -> int"""
        return _libsedml.SedRange_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedRange self) -> bool"""
        return _libsedml.SedRange_hasRequiredAttributes(self)


_libsedml.SedRange_swigregister(SedRange)

class SedListOfRanges(SedListOf):
    """Proxy of C++ SedListOfRanges class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfRanges self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfRanges
        __init__(SedListOfRanges self, SedNamespaces sedmlns) -> SedListOfRanges
        __init__(SedListOfRanges self, SedListOfRanges orig) -> SedListOfRanges
        """
        _libsedml.SedListOfRanges_swiginit(self, _libsedml.new_SedListOfRanges(*args))

    def clone(self):
        """clone(SedListOfRanges self) -> SedListOfRanges"""
        return _libsedml.SedListOfRanges_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfRanges

    def get(self, *args):
        """
        get(SedListOfRanges self, unsigned int n) -> SedRange
        get(SedListOfRanges self, unsigned int n) -> SedRange
        get(SedListOfRanges self, string sid) -> SedRange
        get(SedListOfRanges self, string sid) -> SedRange
        """
        return _libsedml.SedListOfRanges_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfRanges self, unsigned int n) -> SedRange
        remove(SedListOfRanges self, string sid) -> SedRange
        """
        return _libsedml.SedListOfRanges_remove(self, *args)

    def addRange(self, sr):
        """addRange(SedListOfRanges self, SedRange sr) -> int"""
        return _libsedml.SedListOfRanges_addRange(self, sr)

    def getNumRanges(self):
        """getNumRanges(SedListOfRanges self) -> unsigned int"""
        return _libsedml.SedListOfRanges_getNumRanges(self)

    def createUniformRange(self):
        """createUniformRange(SedListOfRanges self) -> SedUniformRange"""
        return _libsedml.SedListOfRanges_createUniformRange(self)

    def createVectorRange(self):
        """createVectorRange(SedListOfRanges self) -> SedVectorRange"""
        return _libsedml.SedListOfRanges_createVectorRange(self)

    def createFunctionalRange(self):
        """createFunctionalRange(SedListOfRanges self) -> SedFunctionalRange"""
        return _libsedml.SedListOfRanges_createFunctionalRange(self)

    def createDataRange(self):
        """createDataRange(SedListOfRanges self) -> SedDataRange"""
        return _libsedml.SedListOfRanges_createDataRange(self)

    def getElementName(self):
        """getElementName(SedListOfRanges self) -> string"""
        return _libsedml.SedListOfRanges_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedListOfRanges self, string name)"""
        return _libsedml.SedListOfRanges_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedListOfRanges self) -> int"""
        return _libsedml.SedListOfRanges_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfRanges self) -> int"""
        return _libsedml.SedListOfRanges_getItemTypeCode(self)


_libsedml.SedListOfRanges_swigregister(SedListOfRanges)

class SedChangeXML(SedChange):
    """Proxy of C++ SedChangeXML class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedChangeXML self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedChangeXML
        __init__(SedChangeXML self, SedNamespaces sedmlns) -> SedChangeXML
        __init__(SedChangeXML self, SedChangeXML orig) -> SedChangeXML
        """
        _libsedml.SedChangeXML_swiginit(self, _libsedml.new_SedChangeXML(*args))

    def clone(self):
        """clone(SedChangeXML self) -> SedChangeXML"""
        return _libsedml.SedChangeXML_clone(self)

    __swig_destroy__ = _libsedml.delete_SedChangeXML

    def getNewXML(self, *args):
        """
        getNewXML(SedChangeXML self) -> XMLNode
        getNewXML(SedChangeXML self) -> XMLNode
        """
        return _libsedml.SedChangeXML_getNewXML(self, *args)

    def isSetNewXML(self):
        """isSetNewXML(SedChangeXML self) -> bool"""
        return _libsedml.SedChangeXML_isSetNewXML(self)

    def setNewXML(self, newXML):
        """setNewXML(SedChangeXML self, XMLNode newXML) -> int"""
        return _libsedml.SedChangeXML_setNewXML(self, newXML)

    def unsetNewXML(self):
        """unsetNewXML(SedChangeXML self) -> int"""
        return _libsedml.SedChangeXML_unsetNewXML(self)

    def getElementName(self):
        """getElementName(SedChangeXML self) -> string"""
        return _libsedml.SedChangeXML_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedChangeXML self) -> int"""
        return _libsedml.SedChangeXML_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedChangeXML self) -> bool"""
        return _libsedml.SedChangeXML_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedChangeXML self) -> bool"""
        return _libsedml.SedChangeXML_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedChangeXML self)"""
        return _libsedml.SedChangeXML_connectToChild(self)


_libsedml.SedChangeXML_swigregister(SedChangeXML)

class SedRemoveXML(SedChange):
    """Proxy of C++ SedRemoveXML class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedRemoveXML self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedRemoveXML
        __init__(SedRemoveXML self, SedNamespaces sedmlns) -> SedRemoveXML
        __init__(SedRemoveXML self, SedRemoveXML orig) -> SedRemoveXML
        """
        _libsedml.SedRemoveXML_swiginit(self, _libsedml.new_SedRemoveXML(*args))

    def clone(self):
        """clone(SedRemoveXML self) -> SedRemoveXML"""
        return _libsedml.SedRemoveXML_clone(self)

    __swig_destroy__ = _libsedml.delete_SedRemoveXML

    def getElementName(self):
        """getElementName(SedRemoveXML self) -> string"""
        return _libsedml.SedRemoveXML_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedRemoveXML self) -> int"""
        return _libsedml.SedRemoveXML_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedRemoveXML self) -> bool"""
        return _libsedml.SedRemoveXML_hasRequiredAttributes(self)


_libsedml.SedRemoveXML_swigregister(SedRemoveXML)

class SedSetValue(SedBase):
    """Proxy of C++ SedSetValue class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedSetValue self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedSetValue
        __init__(SedSetValue self, SedNamespaces sedmlns) -> SedSetValue
        __init__(SedSetValue self, SedSetValue orig) -> SedSetValue
        """
        _libsedml.SedSetValue_swiginit(self, _libsedml.new_SedSetValue(*args))

    def clone(self):
        """clone(SedSetValue self) -> SedSetValue"""
        return _libsedml.SedSetValue_clone(self)

    __swig_destroy__ = _libsedml.delete_SedSetValue

    def getModelReference(self):
        """getModelReference(SedSetValue self) -> string"""
        return _libsedml.SedSetValue_getModelReference(self)

    def getSymbol(self):
        """getSymbol(SedSetValue self) -> string"""
        return _libsedml.SedSetValue_getSymbol(self)

    def getTarget(self):
        """getTarget(SedSetValue self) -> string"""
        return _libsedml.SedSetValue_getTarget(self)

    def getRange(self):
        """getRange(SedSetValue self) -> string"""
        return _libsedml.SedSetValue_getRange(self)

    def isSetModelReference(self):
        """isSetModelReference(SedSetValue self) -> bool"""
        return _libsedml.SedSetValue_isSetModelReference(self)

    def isSetSymbol(self):
        """isSetSymbol(SedSetValue self) -> bool"""
        return _libsedml.SedSetValue_isSetSymbol(self)

    def isSetTarget(self):
        """isSetTarget(SedSetValue self) -> bool"""
        return _libsedml.SedSetValue_isSetTarget(self)

    def isSetRange(self):
        """isSetRange(SedSetValue self) -> bool"""
        return _libsedml.SedSetValue_isSetRange(self)

    def setModelReference(self, modelReference):
        """setModelReference(SedSetValue self, string modelReference) -> int"""
        return _libsedml.SedSetValue_setModelReference(self, modelReference)

    def setSymbol(self, symbol):
        """setSymbol(SedSetValue self, string symbol) -> int"""
        return _libsedml.SedSetValue_setSymbol(self, symbol)

    def setTarget(self, target):
        """setTarget(SedSetValue self, string target) -> int"""
        return _libsedml.SedSetValue_setTarget(self, target)

    def setRange(self, range):
        """setRange(SedSetValue self, string range) -> int"""
        return _libsedml.SedSetValue_setRange(self, range)

    def unsetModelReference(self):
        """unsetModelReference(SedSetValue self) -> int"""
        return _libsedml.SedSetValue_unsetModelReference(self)

    def unsetSymbol(self):
        """unsetSymbol(SedSetValue self) -> int"""
        return _libsedml.SedSetValue_unsetSymbol(self)

    def unsetTarget(self):
        """unsetTarget(SedSetValue self) -> int"""
        return _libsedml.SedSetValue_unsetTarget(self)

    def unsetRange(self):
        """unsetRange(SedSetValue self) -> int"""
        return _libsedml.SedSetValue_unsetRange(self)

    def getMath(self, *args):
        """
        getMath(SedSetValue self) -> ASTNode
        getMath(SedSetValue self) -> ASTNode
        """
        return _libsedml.SedSetValue_getMath(self, *args)

    def isSetMath(self):
        """isSetMath(SedSetValue self) -> bool"""
        return _libsedml.SedSetValue_isSetMath(self)

    def setMath(self, math):
        """setMath(SedSetValue self, ASTNode math) -> int"""
        return _libsedml.SedSetValue_setMath(self, math)

    def unsetMath(self):
        """unsetMath(SedSetValue self) -> int"""
        return _libsedml.SedSetValue_unsetMath(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedSetValue self, string oldid, string newid)"""
        return _libsedml.SedSetValue_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedSetValue self) -> string"""
        return _libsedml.SedSetValue_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedSetValue self) -> int"""
        return _libsedml.SedSetValue_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedSetValue self) -> bool"""
        return _libsedml.SedSetValue_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedSetValue self)"""
        return _libsedml.SedSetValue_connectToChild(self)


_libsedml.SedSetValue_swigregister(SedSetValue)

class SedListOfSetValues(SedListOf):
    """Proxy of C++ SedListOfSetValues class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfSetValues self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfSetValues
        __init__(SedListOfSetValues self, SedNamespaces sedmlns) -> SedListOfSetValues
        __init__(SedListOfSetValues self, SedListOfSetValues orig) -> SedListOfSetValues
        """
        _libsedml.SedListOfSetValues_swiginit(self, _libsedml.new_SedListOfSetValues(*args))

    def clone(self):
        """clone(SedListOfSetValues self) -> SedListOfSetValues"""
        return _libsedml.SedListOfSetValues_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfSetValues

    def get(self, *args):
        """
        get(SedListOfSetValues self, unsigned int n) -> SedSetValue
        get(SedListOfSetValues self, unsigned int n) -> SedSetValue
        get(SedListOfSetValues self, string sid) -> SedSetValue
        get(SedListOfSetValues self, string sid) -> SedSetValue
        """
        return _libsedml.SedListOfSetValues_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfSetValues self, unsigned int n) -> SedSetValue
        remove(SedListOfSetValues self, string sid) -> SedSetValue
        """
        return _libsedml.SedListOfSetValues_remove(self, *args)

    def addTaskChange(self, ssv):
        """addTaskChange(SedListOfSetValues self, SedSetValue ssv) -> int"""
        return _libsedml.SedListOfSetValues_addTaskChange(self, ssv)

    def getNumTaskChanges(self):
        """getNumTaskChanges(SedListOfSetValues self) -> unsigned int"""
        return _libsedml.SedListOfSetValues_getNumTaskChanges(self)

    def createSetValue(self):
        """createSetValue(SedListOfSetValues self) -> SedSetValue"""
        return _libsedml.SedListOfSetValues_createSetValue(self)

    def getByModelReference(self, *args):
        """
        getByModelReference(SedListOfSetValues self, string sid) -> SedSetValue
        getByModelReference(SedListOfSetValues self, string sid) -> SedSetValue
        """
        return _libsedml.SedListOfSetValues_getByModelReference(self, *args)

    def getByRange(self, *args):
        """
        getByRange(SedListOfSetValues self, string sid) -> SedSetValue
        getByRange(SedListOfSetValues self, string sid) -> SedSetValue
        """
        return _libsedml.SedListOfSetValues_getByRange(self, *args)

    def getElementName(self):
        """getElementName(SedListOfSetValues self) -> string"""
        return _libsedml.SedListOfSetValues_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfSetValues self) -> int"""
        return _libsedml.SedListOfSetValues_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfSetValues self) -> int"""
        return _libsedml.SedListOfSetValues_getItemTypeCode(self)


_libsedml.SedListOfSetValues_swigregister(SedListOfSetValues)

class SedUniformRange(SedRange):
    """Proxy of C++ SedUniformRange class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedUniformRange self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedUniformRange
        __init__(SedUniformRange self, SedNamespaces sedmlns) -> SedUniformRange
        __init__(SedUniformRange self, SedUniformRange orig) -> SedUniformRange
        """
        _libsedml.SedUniformRange_swiginit(self, _libsedml.new_SedUniformRange(*args))

    def clone(self):
        """clone(SedUniformRange self) -> SedUniformRange"""
        return _libsedml.SedUniformRange_clone(self)

    __swig_destroy__ = _libsedml.delete_SedUniformRange

    def getStart(self):
        """getStart(SedUniformRange self) -> double"""
        return _libsedml.SedUniformRange_getStart(self)

    def getEnd(self):
        """getEnd(SedUniformRange self) -> double"""
        return _libsedml.SedUniformRange_getEnd(self)

    def getNumberOfPoints(self):
        """getNumberOfPoints(SedUniformRange self) -> int"""
        return _libsedml.SedUniformRange_getNumberOfPoints(self)

    def getType(self):
        """getType(SedUniformRange self) -> string"""
        return _libsedml.SedUniformRange_getType(self)

    def isSetStart(self):
        """isSetStart(SedUniformRange self) -> bool"""
        return _libsedml.SedUniformRange_isSetStart(self)

    def isSetEnd(self):
        """isSetEnd(SedUniformRange self) -> bool"""
        return _libsedml.SedUniformRange_isSetEnd(self)

    def isSetNumberOfPoints(self):
        """isSetNumberOfPoints(SedUniformRange self) -> bool"""
        return _libsedml.SedUniformRange_isSetNumberOfPoints(self)

    def isSetType(self):
        """isSetType(SedUniformRange self) -> bool"""
        return _libsedml.SedUniformRange_isSetType(self)

    def setStart(self, start):
        """setStart(SedUniformRange self, double start) -> int"""
        return _libsedml.SedUniformRange_setStart(self, start)

    def setEnd(self, end):
        """setEnd(SedUniformRange self, double end) -> int"""
        return _libsedml.SedUniformRange_setEnd(self, end)

    def setNumberOfPoints(self, numberOfPoints):
        """setNumberOfPoints(SedUniformRange self, int numberOfPoints) -> int"""
        return _libsedml.SedUniformRange_setNumberOfPoints(self, numberOfPoints)

    def setType(self, type):
        """setType(SedUniformRange self, string type) -> int"""
        return _libsedml.SedUniformRange_setType(self, type)

    def unsetStart(self):
        """unsetStart(SedUniformRange self) -> int"""
        return _libsedml.SedUniformRange_unsetStart(self)

    def unsetEnd(self):
        """unsetEnd(SedUniformRange self) -> int"""
        return _libsedml.SedUniformRange_unsetEnd(self)

    def unsetNumberOfPoints(self):
        """unsetNumberOfPoints(SedUniformRange self) -> int"""
        return _libsedml.SedUniformRange_unsetNumberOfPoints(self)

    def unsetType(self):
        """unsetType(SedUniformRange self) -> int"""
        return _libsedml.SedUniformRange_unsetType(self)

    def getElementName(self):
        """getElementName(SedUniformRange self) -> string"""
        return _libsedml.SedUniformRange_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedUniformRange self) -> int"""
        return _libsedml.SedUniformRange_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedUniformRange self) -> bool"""
        return _libsedml.SedUniformRange_hasRequiredAttributes(self)


_libsedml.SedUniformRange_swigregister(SedUniformRange)

class SedVectorRange(SedRange):
    """Proxy of C++ SedVectorRange class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedVectorRange self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedVectorRange
        __init__(SedVectorRange self, SedNamespaces sedmlns) -> SedVectorRange
        __init__(SedVectorRange self, SedVectorRange orig) -> SedVectorRange
        """
        _libsedml.SedVectorRange_swiginit(self, _libsedml.new_SedVectorRange(*args))

    def clone(self):
        """clone(SedVectorRange self) -> SedVectorRange"""
        return _libsedml.SedVectorRange_clone(self)

    __swig_destroy__ = _libsedml.delete_SedVectorRange

    def getValues(self):
        """getValues(SedVectorRange self) -> DoubleStdVector"""
        return _libsedml.SedVectorRange_getValues(self)

    def hasValues(self):
        """hasValues(SedVectorRange self) -> bool"""
        return _libsedml.SedVectorRange_hasValues(self)

    def getNumValues(self):
        """getNumValues(SedVectorRange self) -> unsigned int"""
        return _libsedml.SedVectorRange_getNumValues(self)

    def setValues(self, value):
        """setValues(SedVectorRange self, DoubleStdVector value) -> int"""
        return _libsedml.SedVectorRange_setValues(self, value)

    def addValue(self, value):
        """addValue(SedVectorRange self, double value) -> int"""
        return _libsedml.SedVectorRange_addValue(self, value)

    def clearValues(self):
        """clearValues(SedVectorRange self) -> int"""
        return _libsedml.SedVectorRange_clearValues(self)

    def getElementName(self):
        """getElementName(SedVectorRange self) -> string"""
        return _libsedml.SedVectorRange_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedVectorRange self) -> int"""
        return _libsedml.SedVectorRange_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedVectorRange self) -> bool"""
        return _libsedml.SedVectorRange_hasRequiredAttributes(self)


_libsedml.SedVectorRange_swigregister(SedVectorRange)

class SedFunctionalRange(SedRange):
    """Proxy of C++ SedFunctionalRange class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedFunctionalRange self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedFunctionalRange
        __init__(SedFunctionalRange self, SedNamespaces sedmlns) -> SedFunctionalRange
        __init__(SedFunctionalRange self, SedFunctionalRange orig) -> SedFunctionalRange
        """
        _libsedml.SedFunctionalRange_swiginit(self, _libsedml.new_SedFunctionalRange(*args))

    def clone(self):
        """clone(SedFunctionalRange self) -> SedFunctionalRange"""
        return _libsedml.SedFunctionalRange_clone(self)

    __swig_destroy__ = _libsedml.delete_SedFunctionalRange

    def getRange(self):
        """getRange(SedFunctionalRange self) -> string"""
        return _libsedml.SedFunctionalRange_getRange(self)

    def isSetRange(self):
        """isSetRange(SedFunctionalRange self) -> bool"""
        return _libsedml.SedFunctionalRange_isSetRange(self)

    def setRange(self, range):
        """setRange(SedFunctionalRange self, string range) -> int"""
        return _libsedml.SedFunctionalRange_setRange(self, range)

    def unsetRange(self):
        """unsetRange(SedFunctionalRange self) -> int"""
        return _libsedml.SedFunctionalRange_unsetRange(self)

    def getMath(self, *args):
        """
        getMath(SedFunctionalRange self) -> ASTNode
        getMath(SedFunctionalRange self) -> ASTNode
        """
        return _libsedml.SedFunctionalRange_getMath(self, *args)

    def isSetMath(self):
        """isSetMath(SedFunctionalRange self) -> bool"""
        return _libsedml.SedFunctionalRange_isSetMath(self)

    def setMath(self, math):
        """setMath(SedFunctionalRange self, ASTNode math) -> int"""
        return _libsedml.SedFunctionalRange_setMath(self, math)

    def unsetMath(self):
        """unsetMath(SedFunctionalRange self) -> int"""
        return _libsedml.SedFunctionalRange_unsetMath(self)

    def getListOfVariables(self, *args):
        """
        getListOfVariables(SedFunctionalRange self) -> SedListOfVariables
        getListOfVariables(SedFunctionalRange self) -> SedListOfVariables
        """
        return _libsedml.SedFunctionalRange_getListOfVariables(self, *args)

    def getVariable(self, *args):
        """
        getVariable(SedFunctionalRange self, unsigned int n) -> SedVariable
        getVariable(SedFunctionalRange self, unsigned int n) -> SedVariable
        getVariable(SedFunctionalRange self, string sid) -> SedVariable
        getVariable(SedFunctionalRange self, string sid) -> SedVariable
        """
        return _libsedml.SedFunctionalRange_getVariable(self, *args)

    def getVariableByTaskReference(self, *args):
        """
        getVariableByTaskReference(SedFunctionalRange self, string sid) -> SedVariable
        getVariableByTaskReference(SedFunctionalRange self, string sid) -> SedVariable
        """
        return _libsedml.SedFunctionalRange_getVariableByTaskReference(self, *args)

    def getVariableByModelReference(self, *args):
        """
        getVariableByModelReference(SedFunctionalRange self, string sid) -> SedVariable
        getVariableByModelReference(SedFunctionalRange self, string sid) -> SedVariable
        """
        return _libsedml.SedFunctionalRange_getVariableByModelReference(self, *args)

    def addVariable(self, sv):
        """addVariable(SedFunctionalRange self, SedVariable sv) -> int"""
        return _libsedml.SedFunctionalRange_addVariable(self, sv)

    def getNumVariables(self):
        """getNumVariables(SedFunctionalRange self) -> unsigned int"""
        return _libsedml.SedFunctionalRange_getNumVariables(self)

    def createVariable(self):
        """createVariable(SedFunctionalRange self) -> SedVariable"""
        return _libsedml.SedFunctionalRange_createVariable(self)

    def createDependentVariable(self):
        """createDependentVariable(SedFunctionalRange self) -> SedDependentVariable"""
        return _libsedml.SedFunctionalRange_createDependentVariable(self)

    def removeVariable(self, *args):
        """
        removeVariable(SedFunctionalRange self, unsigned int n) -> SedVariable
        removeVariable(SedFunctionalRange self, string sid) -> SedVariable
        """
        return _libsedml.SedFunctionalRange_removeVariable(self, *args)

    def getListOfParameters(self, *args):
        """
        getListOfParameters(SedFunctionalRange self) -> SedListOfParameters
        getListOfParameters(SedFunctionalRange self) -> SedListOfParameters
        """
        return _libsedml.SedFunctionalRange_getListOfParameters(self, *args)

    def getParameter(self, *args):
        """
        getParameter(SedFunctionalRange self, unsigned int n) -> SedParameter
        getParameter(SedFunctionalRange self, unsigned int n) -> SedParameter
        getParameter(SedFunctionalRange self, string sid) -> SedParameter
        getParameter(SedFunctionalRange self, string sid) -> SedParameter
        """
        return _libsedml.SedFunctionalRange_getParameter(self, *args)

    def addParameter(self, sp):
        """addParameter(SedFunctionalRange self, SedParameter sp) -> int"""
        return _libsedml.SedFunctionalRange_addParameter(self, sp)

    def getNumParameters(self):
        """getNumParameters(SedFunctionalRange self) -> unsigned int"""
        return _libsedml.SedFunctionalRange_getNumParameters(self)

    def createParameter(self):
        """createParameter(SedFunctionalRange self) -> SedParameter"""
        return _libsedml.SedFunctionalRange_createParameter(self)

    def removeParameter(self, *args):
        """
        removeParameter(SedFunctionalRange self, unsigned int n) -> SedParameter
        removeParameter(SedFunctionalRange self, string sid) -> SedParameter
        """
        return _libsedml.SedFunctionalRange_removeParameter(self, *args)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedFunctionalRange self, string oldid, string newid)"""
        return _libsedml.SedFunctionalRange_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedFunctionalRange self) -> string"""
        return _libsedml.SedFunctionalRange_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedFunctionalRange self) -> int"""
        return _libsedml.SedFunctionalRange_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedFunctionalRange self) -> bool"""
        return _libsedml.SedFunctionalRange_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedFunctionalRange self) -> bool"""
        return _libsedml.SedFunctionalRange_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedFunctionalRange self)"""
        return _libsedml.SedFunctionalRange_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedFunctionalRange self, string id) -> SedBase"""
        return _libsedml.SedFunctionalRange_getElementBySId(self, id)


_libsedml.SedFunctionalRange_swigregister(SedFunctionalRange)

class SedSubTask(SedBase):
    """Proxy of C++ SedSubTask class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedSubTask self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedSubTask
        __init__(SedSubTask self, SedNamespaces sedmlns) -> SedSubTask
        __init__(SedSubTask self, SedSubTask orig) -> SedSubTask
        """
        _libsedml.SedSubTask_swiginit(self, _libsedml.new_SedSubTask(*args))

    def clone(self):
        """clone(SedSubTask self) -> SedSubTask"""
        return _libsedml.SedSubTask_clone(self)

    __swig_destroy__ = _libsedml.delete_SedSubTask

    def getOrder(self):
        """getOrder(SedSubTask self) -> int"""
        return _libsedml.SedSubTask_getOrder(self)

    def getTask(self):
        """getTask(SedSubTask self) -> string"""
        return _libsedml.SedSubTask_getTask(self)

    def isSetOrder(self):
        """isSetOrder(SedSubTask self) -> bool"""
        return _libsedml.SedSubTask_isSetOrder(self)

    def isSetTask(self):
        """isSetTask(SedSubTask self) -> bool"""
        return _libsedml.SedSubTask_isSetTask(self)

    def setOrder(self, order):
        """setOrder(SedSubTask self, int order) -> int"""
        return _libsedml.SedSubTask_setOrder(self, order)

    def setTask(self, task):
        """setTask(SedSubTask self, string task) -> int"""
        return _libsedml.SedSubTask_setTask(self, task)

    def unsetOrder(self):
        """unsetOrder(SedSubTask self) -> int"""
        return _libsedml.SedSubTask_unsetOrder(self)

    def unsetTask(self):
        """unsetTask(SedSubTask self) -> int"""
        return _libsedml.SedSubTask_unsetTask(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedSubTask self, string oldid, string newid)"""
        return _libsedml.SedSubTask_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedSubTask self) -> string"""
        return _libsedml.SedSubTask_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedSubTask self) -> int"""
        return _libsedml.SedSubTask_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedSubTask self) -> bool"""
        return _libsedml.SedSubTask_hasRequiredAttributes(self)


_libsedml.SedSubTask_swigregister(SedSubTask)

class SedListOfSubTasks(SedListOf):
    """Proxy of C++ SedListOfSubTasks class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfSubTasks self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfSubTasks
        __init__(SedListOfSubTasks self, SedNamespaces sedmlns) -> SedListOfSubTasks
        __init__(SedListOfSubTasks self, SedListOfSubTasks orig) -> SedListOfSubTasks
        """
        _libsedml.SedListOfSubTasks_swiginit(self, _libsedml.new_SedListOfSubTasks(*args))

    def clone(self):
        """clone(SedListOfSubTasks self) -> SedListOfSubTasks"""
        return _libsedml.SedListOfSubTasks_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfSubTasks

    def get(self, *args):
        """
        get(SedListOfSubTasks self, unsigned int n) -> SedSubTask
        get(SedListOfSubTasks self, unsigned int n) -> SedSubTask
        get(SedListOfSubTasks self, string sid) -> SedSubTask
        get(SedListOfSubTasks self, string sid) -> SedSubTask
        """
        return _libsedml.SedListOfSubTasks_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfSubTasks self, unsigned int n) -> SedSubTask
        remove(SedListOfSubTasks self, string sid) -> SedSubTask
        """
        return _libsedml.SedListOfSubTasks_remove(self, *args)

    def addSubTask(self, sst):
        """addSubTask(SedListOfSubTasks self, SedSubTask sst) -> int"""
        return _libsedml.SedListOfSubTasks_addSubTask(self, sst)

    def getNumSubTasks(self):
        """getNumSubTasks(SedListOfSubTasks self) -> unsigned int"""
        return _libsedml.SedListOfSubTasks_getNumSubTasks(self)

    def createSubTask(self):
        """createSubTask(SedListOfSubTasks self) -> SedSubTask"""
        return _libsedml.SedListOfSubTasks_createSubTask(self)

    def getByTask(self, *args):
        """
        getByTask(SedListOfSubTasks self, string sid) -> SedSubTask
        getByTask(SedListOfSubTasks self, string sid) -> SedSubTask
        """
        return _libsedml.SedListOfSubTasks_getByTask(self, *args)

    def getElementName(self):
        """getElementName(SedListOfSubTasks self) -> string"""
        return _libsedml.SedListOfSubTasks_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfSubTasks self) -> int"""
        return _libsedml.SedListOfSubTasks_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfSubTasks self) -> int"""
        return _libsedml.SedListOfSubTasks_getItemTypeCode(self)


_libsedml.SedListOfSubTasks_swigregister(SedListOfSubTasks)

class SedOneStep(SedSimulation):
    """Proxy of C++ SedOneStep class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedOneStep self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedOneStep
        __init__(SedOneStep self, SedNamespaces sedmlns) -> SedOneStep
        __init__(SedOneStep self, SedOneStep orig) -> SedOneStep
        """
        _libsedml.SedOneStep_swiginit(self, _libsedml.new_SedOneStep(*args))

    def clone(self):
        """clone(SedOneStep self) -> SedOneStep"""
        return _libsedml.SedOneStep_clone(self)

    __swig_destroy__ = _libsedml.delete_SedOneStep

    def getStep(self):
        """getStep(SedOneStep self) -> double"""
        return _libsedml.SedOneStep_getStep(self)

    def isSetStep(self):
        """isSetStep(SedOneStep self) -> bool"""
        return _libsedml.SedOneStep_isSetStep(self)

    def setStep(self, step):
        """setStep(SedOneStep self, double step) -> int"""
        return _libsedml.SedOneStep_setStep(self, step)

    def unsetStep(self):
        """unsetStep(SedOneStep self) -> int"""
        return _libsedml.SedOneStep_unsetStep(self)

    def getElementName(self):
        """getElementName(SedOneStep self) -> string"""
        return _libsedml.SedOneStep_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedOneStep self) -> int"""
        return _libsedml.SedOneStep_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedOneStep self) -> bool"""
        return _libsedml.SedOneStep_hasRequiredAttributes(self)


_libsedml.SedOneStep_swigregister(SedOneStep)

class SedSteadyState(SedSimulation):
    """Proxy of C++ SedSteadyState class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedSteadyState self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedSteadyState
        __init__(SedSteadyState self, SedNamespaces sedmlns) -> SedSteadyState
        __init__(SedSteadyState self, SedSteadyState orig) -> SedSteadyState
        """
        _libsedml.SedSteadyState_swiginit(self, _libsedml.new_SedSteadyState(*args))

    def clone(self):
        """clone(SedSteadyState self) -> SedSteadyState"""
        return _libsedml.SedSteadyState_clone(self)

    __swig_destroy__ = _libsedml.delete_SedSteadyState

    def getElementName(self):
        """getElementName(SedSteadyState self) -> string"""
        return _libsedml.SedSteadyState_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedSteadyState self) -> int"""
        return _libsedml.SedSteadyState_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedSteadyState self) -> bool"""
        return _libsedml.SedSteadyState_hasRequiredAttributes(self)


_libsedml.SedSteadyState_swigregister(SedSteadyState)

class SedRepeatedTask(SedAbstractTask):
    """Proxy of C++ SedRepeatedTask class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedRepeatedTask self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedRepeatedTask
        __init__(SedRepeatedTask self, SedNamespaces sedmlns) -> SedRepeatedTask
        __init__(SedRepeatedTask self, SedRepeatedTask orig) -> SedRepeatedTask
        """
        _libsedml.SedRepeatedTask_swiginit(self, _libsedml.new_SedRepeatedTask(*args))

    def clone(self):
        """clone(SedRepeatedTask self) -> SedRepeatedTask"""
        return _libsedml.SedRepeatedTask_clone(self)

    __swig_destroy__ = _libsedml.delete_SedRepeatedTask

    def getRangeId(self):
        """getRangeId(SedRepeatedTask self) -> string"""
        return _libsedml.SedRepeatedTask_getRangeId(self)

    def getResetModel(self):
        """getResetModel(SedRepeatedTask self) -> bool"""
        return _libsedml.SedRepeatedTask_getResetModel(self)

    def isSetRangeId(self):
        """isSetRangeId(SedRepeatedTask self) -> bool"""
        return _libsedml.SedRepeatedTask_isSetRangeId(self)

    def isSetResetModel(self):
        """isSetResetModel(SedRepeatedTask self) -> bool"""
        return _libsedml.SedRepeatedTask_isSetResetModel(self)

    def setRangeId(self, rangeId):
        """setRangeId(SedRepeatedTask self, string rangeId) -> int"""
        return _libsedml.SedRepeatedTask_setRangeId(self, rangeId)

    def setResetModel(self, resetModel):
        """setResetModel(SedRepeatedTask self, bool resetModel) -> int"""
        return _libsedml.SedRepeatedTask_setResetModel(self, resetModel)

    def unsetRangeId(self):
        """unsetRangeId(SedRepeatedTask self) -> int"""
        return _libsedml.SedRepeatedTask_unsetRangeId(self)

    def unsetResetModel(self):
        """unsetResetModel(SedRepeatedTask self) -> int"""
        return _libsedml.SedRepeatedTask_unsetResetModel(self)

    def getListOfRanges(self, *args):
        """
        getListOfRanges(SedRepeatedTask self) -> SedListOfRanges
        getListOfRanges(SedRepeatedTask self) -> SedListOfRanges
        """
        return _libsedml.SedRepeatedTask_getListOfRanges(self, *args)

    def getRange(self, *args):
        """
        getRange(SedRepeatedTask self, unsigned int n) -> SedRange
        getRange(SedRepeatedTask self, unsigned int n) -> SedRange
        getRange(SedRepeatedTask self, string sid) -> SedRange
        getRange(SedRepeatedTask self, string sid) -> SedRange
        """
        return _libsedml.SedRepeatedTask_getRange(self, *args)

    def addRange(self, sr):
        """addRange(SedRepeatedTask self, SedRange sr) -> int"""
        return _libsedml.SedRepeatedTask_addRange(self, sr)

    def getNumRanges(self):
        """getNumRanges(SedRepeatedTask self) -> unsigned int"""
        return _libsedml.SedRepeatedTask_getNumRanges(self)

    def createUniformRange(self):
        """createUniformRange(SedRepeatedTask self) -> SedUniformRange"""
        return _libsedml.SedRepeatedTask_createUniformRange(self)

    def createVectorRange(self):
        """createVectorRange(SedRepeatedTask self) -> SedVectorRange"""
        return _libsedml.SedRepeatedTask_createVectorRange(self)

    def createFunctionalRange(self):
        """createFunctionalRange(SedRepeatedTask self) -> SedFunctionalRange"""
        return _libsedml.SedRepeatedTask_createFunctionalRange(self)

    def createDataRange(self):
        """createDataRange(SedRepeatedTask self) -> SedDataRange"""
        return _libsedml.SedRepeatedTask_createDataRange(self)

    def removeRange(self, *args):
        """
        removeRange(SedRepeatedTask self, unsigned int n) -> SedRange
        removeRange(SedRepeatedTask self, string sid) -> SedRange
        """
        return _libsedml.SedRepeatedTask_removeRange(self, *args)

    def getListOfTaskChanges(self, *args):
        """
        getListOfTaskChanges(SedRepeatedTask self) -> SedListOfSetValues
        getListOfTaskChanges(SedRepeatedTask self) -> SedListOfSetValues
        """
        return _libsedml.SedRepeatedTask_getListOfTaskChanges(self, *args)

    def getTaskChange(self, *args):
        """
        getTaskChange(SedRepeatedTask self, unsigned int n) -> SedSetValue
        getTaskChange(SedRepeatedTask self, unsigned int n) -> SedSetValue
        """
        return _libsedml.SedRepeatedTask_getTaskChange(self, *args)

    def getTaskChangeByModelReference(self, *args):
        """
        getTaskChangeByModelReference(SedRepeatedTask self, string sid) -> SedSetValue
        getTaskChangeByModelReference(SedRepeatedTask self, string sid) -> SedSetValue
        """
        return _libsedml.SedRepeatedTask_getTaskChangeByModelReference(self, *args)

    def getTaskChangeByRange(self, *args):
        """
        getTaskChangeByRange(SedRepeatedTask self, string sid) -> SedSetValue
        getTaskChangeByRange(SedRepeatedTask self, string sid) -> SedSetValue
        """
        return _libsedml.SedRepeatedTask_getTaskChangeByRange(self, *args)

    def addTaskChange(self, ssv):
        """addTaskChange(SedRepeatedTask self, SedSetValue ssv) -> int"""
        return _libsedml.SedRepeatedTask_addTaskChange(self, ssv)

    def getNumTaskChanges(self):
        """getNumTaskChanges(SedRepeatedTask self) -> unsigned int"""
        return _libsedml.SedRepeatedTask_getNumTaskChanges(self)

    def createTaskChange(self):
        """createTaskChange(SedRepeatedTask self) -> SedSetValue"""
        return _libsedml.SedRepeatedTask_createTaskChange(self)

    def removeTaskChange(self, n):
        """removeTaskChange(SedRepeatedTask self, unsigned int n) -> SedSetValue"""
        return _libsedml.SedRepeatedTask_removeTaskChange(self, n)

    def getListOfSubTasks(self, *args):
        """
        getListOfSubTasks(SedRepeatedTask self) -> SedListOfSubTasks
        getListOfSubTasks(SedRepeatedTask self) -> SedListOfSubTasks
        """
        return _libsedml.SedRepeatedTask_getListOfSubTasks(self, *args)

    def getSubTask(self, *args):
        """
        getSubTask(SedRepeatedTask self, unsigned int n) -> SedSubTask
        getSubTask(SedRepeatedTask self, unsigned int n) -> SedSubTask
        """
        return _libsedml.SedRepeatedTask_getSubTask(self, *args)

    def getSubTaskByTask(self, *args):
        """
        getSubTaskByTask(SedRepeatedTask self, string sid) -> SedSubTask
        getSubTaskByTask(SedRepeatedTask self, string sid) -> SedSubTask
        """
        return _libsedml.SedRepeatedTask_getSubTaskByTask(self, *args)

    def addSubTask(self, sst):
        """addSubTask(SedRepeatedTask self, SedSubTask sst) -> int"""
        return _libsedml.SedRepeatedTask_addSubTask(self, sst)

    def getNumSubTasks(self):
        """getNumSubTasks(SedRepeatedTask self) -> unsigned int"""
        return _libsedml.SedRepeatedTask_getNumSubTasks(self)

    def createSubTask(self):
        """createSubTask(SedRepeatedTask self) -> SedSubTask"""
        return _libsedml.SedRepeatedTask_createSubTask(self)

    def removeSubTask(self, n):
        """removeSubTask(SedRepeatedTask self, unsigned int n) -> SedSubTask"""
        return _libsedml.SedRepeatedTask_removeSubTask(self, n)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedRepeatedTask self, string oldid, string newid)"""
        return _libsedml.SedRepeatedTask_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedRepeatedTask self) -> string"""
        return _libsedml.SedRepeatedTask_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedRepeatedTask self) -> int"""
        return _libsedml.SedRepeatedTask_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedRepeatedTask self) -> bool"""
        return _libsedml.SedRepeatedTask_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedRepeatedTask self) -> bool"""
        return _libsedml.SedRepeatedTask_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedRepeatedTask self)"""
        return _libsedml.SedRepeatedTask_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedRepeatedTask self, string id) -> SedBase"""
        return _libsedml.SedRepeatedTask_getElementBySId(self, id)


_libsedml.SedRepeatedTask_swigregister(SedRepeatedTask)

class SedComputeChange(SedChange):
    """Proxy of C++ SedComputeChange class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedComputeChange self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedComputeChange
        __init__(SedComputeChange self, SedNamespaces sedmlns) -> SedComputeChange
        __init__(SedComputeChange self, SedComputeChange orig) -> SedComputeChange
        """
        _libsedml.SedComputeChange_swiginit(self, _libsedml.new_SedComputeChange(*args))

    def clone(self):
        """clone(SedComputeChange self) -> SedComputeChange"""
        return _libsedml.SedComputeChange_clone(self)

    __swig_destroy__ = _libsedml.delete_SedComputeChange

    def getMath(self, *args):
        """
        getMath(SedComputeChange self) -> ASTNode
        getMath(SedComputeChange self) -> ASTNode
        """
        return _libsedml.SedComputeChange_getMath(self, *args)

    def isSetMath(self):
        """isSetMath(SedComputeChange self) -> bool"""
        return _libsedml.SedComputeChange_isSetMath(self)

    def setMath(self, math):
        """setMath(SedComputeChange self, ASTNode math) -> int"""
        return _libsedml.SedComputeChange_setMath(self, math)

    def unsetMath(self):
        """unsetMath(SedComputeChange self) -> int"""
        return _libsedml.SedComputeChange_unsetMath(self)

    def getListOfVariables(self, *args):
        """
        getListOfVariables(SedComputeChange self) -> SedListOfVariables
        getListOfVariables(SedComputeChange self) -> SedListOfVariables
        """
        return _libsedml.SedComputeChange_getListOfVariables(self, *args)

    def getVariable(self, *args):
        """
        getVariable(SedComputeChange self, unsigned int n) -> SedVariable
        getVariable(SedComputeChange self, unsigned int n) -> SedVariable
        getVariable(SedComputeChange self, string sid) -> SedVariable
        getVariable(SedComputeChange self, string sid) -> SedVariable
        """
        return _libsedml.SedComputeChange_getVariable(self, *args)

    def getVariableByTaskReference(self, *args):
        """
        getVariableByTaskReference(SedComputeChange self, string sid) -> SedVariable
        getVariableByTaskReference(SedComputeChange self, string sid) -> SedVariable
        """
        return _libsedml.SedComputeChange_getVariableByTaskReference(self, *args)

    def getVariableByModelReference(self, *args):
        """
        getVariableByModelReference(SedComputeChange self, string sid) -> SedVariable
        getVariableByModelReference(SedComputeChange self, string sid) -> SedVariable
        """
        return _libsedml.SedComputeChange_getVariableByModelReference(self, *args)

    def addVariable(self, sv):
        """addVariable(SedComputeChange self, SedVariable sv) -> int"""
        return _libsedml.SedComputeChange_addVariable(self, sv)

    def getNumVariables(self):
        """getNumVariables(SedComputeChange self) -> unsigned int"""
        return _libsedml.SedComputeChange_getNumVariables(self)

    def createVariable(self):
        """createVariable(SedComputeChange self) -> SedVariable"""
        return _libsedml.SedComputeChange_createVariable(self)

    def createDependentVariable(self):
        """createDependentVariable(SedComputeChange self) -> SedDependentVariable"""
        return _libsedml.SedComputeChange_createDependentVariable(self)

    def removeVariable(self, *args):
        """
        removeVariable(SedComputeChange self, unsigned int n) -> SedVariable
        removeVariable(SedComputeChange self, string sid) -> SedVariable
        """
        return _libsedml.SedComputeChange_removeVariable(self, *args)

    def getListOfParameters(self, *args):
        """
        getListOfParameters(SedComputeChange self) -> SedListOfParameters
        getListOfParameters(SedComputeChange self) -> SedListOfParameters
        """
        return _libsedml.SedComputeChange_getListOfParameters(self, *args)

    def getParameter(self, *args):
        """
        getParameter(SedComputeChange self, unsigned int n) -> SedParameter
        getParameter(SedComputeChange self, unsigned int n) -> SedParameter
        getParameter(SedComputeChange self, string sid) -> SedParameter
        getParameter(SedComputeChange self, string sid) -> SedParameter
        """
        return _libsedml.SedComputeChange_getParameter(self, *args)

    def addParameter(self, sp):
        """addParameter(SedComputeChange self, SedParameter sp) -> int"""
        return _libsedml.SedComputeChange_addParameter(self, sp)

    def getNumParameters(self):
        """getNumParameters(SedComputeChange self) -> unsigned int"""
        return _libsedml.SedComputeChange_getNumParameters(self)

    def createParameter(self):
        """createParameter(SedComputeChange self) -> SedParameter"""
        return _libsedml.SedComputeChange_createParameter(self)

    def removeParameter(self, *args):
        """
        removeParameter(SedComputeChange self, unsigned int n) -> SedParameter
        removeParameter(SedComputeChange self, string sid) -> SedParameter
        """
        return _libsedml.SedComputeChange_removeParameter(self, *args)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedComputeChange self, string oldid, string newid)"""
        return _libsedml.SedComputeChange_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedComputeChange self) -> string"""
        return _libsedml.SedComputeChange_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedComputeChange self) -> int"""
        return _libsedml.SedComputeChange_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedComputeChange self) -> bool"""
        return _libsedml.SedComputeChange_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedComputeChange self) -> bool"""
        return _libsedml.SedComputeChange_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedComputeChange self)"""
        return _libsedml.SedComputeChange_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedComputeChange self, string id) -> SedBase"""
        return _libsedml.SedComputeChange_getElementBySId(self, id)


_libsedml.SedComputeChange_swigregister(SedComputeChange)

class SedDataDescription(SedBase):
    """Proxy of C++ SedDataDescription class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedDataDescription self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedDataDescription
        __init__(SedDataDescription self, SedNamespaces sedmlns) -> SedDataDescription
        __init__(SedDataDescription self, SedDataDescription orig) -> SedDataDescription
        """
        _libsedml.SedDataDescription_swiginit(self, _libsedml.new_SedDataDescription(*args))

    def clone(self):
        """clone(SedDataDescription self) -> SedDataDescription"""
        return _libsedml.SedDataDescription_clone(self)

    __swig_destroy__ = _libsedml.delete_SedDataDescription

    def getId(self):
        """getId(SedDataDescription self) -> string"""
        return _libsedml.SedDataDescription_getId(self)

    def getName(self):
        """getName(SedDataDescription self) -> string"""
        return _libsedml.SedDataDescription_getName(self)

    def getFormat(self):
        """getFormat(SedDataDescription self) -> string"""
        return _libsedml.SedDataDescription_getFormat(self)

    def getSource(self):
        """getSource(SedDataDescription self) -> string"""
        return _libsedml.SedDataDescription_getSource(self)

    def isSetId(self):
        """isSetId(SedDataDescription self) -> bool"""
        return _libsedml.SedDataDescription_isSetId(self)

    def isSetName(self):
        """isSetName(SedDataDescription self) -> bool"""
        return _libsedml.SedDataDescription_isSetName(self)

    def isSetFormat(self):
        """isSetFormat(SedDataDescription self) -> bool"""
        return _libsedml.SedDataDescription_isSetFormat(self)

    def isSetSource(self):
        """isSetSource(SedDataDescription self) -> bool"""
        return _libsedml.SedDataDescription_isSetSource(self)

    def setId(self, id):
        """setId(SedDataDescription self, string id) -> int"""
        return _libsedml.SedDataDescription_setId(self, id)

    def setName(self, name):
        """setName(SedDataDescription self, string name) -> int"""
        return _libsedml.SedDataDescription_setName(self, name)

    def setFormat(self, format):
        """setFormat(SedDataDescription self, string format) -> int"""
        return _libsedml.SedDataDescription_setFormat(self, format)

    def setSource(self, source):
        """setSource(SedDataDescription self, string source) -> int"""
        return _libsedml.SedDataDescription_setSource(self, source)

    def unsetId(self):
        """unsetId(SedDataDescription self) -> int"""
        return _libsedml.SedDataDescription_unsetId(self)

    def unsetName(self):
        """unsetName(SedDataDescription self) -> int"""
        return _libsedml.SedDataDescription_unsetName(self)

    def unsetFormat(self):
        """unsetFormat(SedDataDescription self) -> int"""
        return _libsedml.SedDataDescription_unsetFormat(self)

    def unsetSource(self):
        """unsetSource(SedDataDescription self) -> int"""
        return _libsedml.SedDataDescription_unsetSource(self)

    def getDimensionDescription(self, *args):
        """
        getDimensionDescription(SedDataDescription self) -> DimensionDescription
        getDimensionDescription(SedDataDescription self) -> DimensionDescription
        """
        return _libsedml.SedDataDescription_getDimensionDescription(self, *args)

    def isSetDimensionDescription(self):
        """isSetDimensionDescription(SedDataDescription self) -> bool"""
        return _libsedml.SedDataDescription_isSetDimensionDescription(self)

    def setDimensionDescription(self, dimensionDescription):
        """setDimensionDescription(SedDataDescription self, DimensionDescription dimensionDescription) -> int"""
        return _libsedml.SedDataDescription_setDimensionDescription(self, dimensionDescription)

    def createDimensionDescription(self):
        """createDimensionDescription(SedDataDescription self) -> DimensionDescription"""
        return _libsedml.SedDataDescription_createDimensionDescription(self)

    def unsetDimensionDescription(self):
        """unsetDimensionDescription(SedDataDescription self) -> int"""
        return _libsedml.SedDataDescription_unsetDimensionDescription(self)

    def getListOfDataSources(self, *args):
        """
        getListOfDataSources(SedDataDescription self) -> SedListOfDataSources
        getListOfDataSources(SedDataDescription self) -> SedListOfDataSources
        """
        return _libsedml.SedDataDescription_getListOfDataSources(self, *args)

    def getDataSource(self, *args):
        """
        getDataSource(SedDataDescription self, unsigned int n) -> SedDataSource
        getDataSource(SedDataDescription self, unsigned int n) -> SedDataSource
        getDataSource(SedDataDescription self, string sid) -> SedDataSource
        getDataSource(SedDataDescription self, string sid) -> SedDataSource
        """
        return _libsedml.SedDataDescription_getDataSource(self, *args)

    def getDataSourceByIndexSet(self, *args):
        """
        getDataSourceByIndexSet(SedDataDescription self, string sid) -> SedDataSource
        getDataSourceByIndexSet(SedDataDescription self, string sid) -> SedDataSource
        """
        return _libsedml.SedDataDescription_getDataSourceByIndexSet(self, *args)

    def addDataSource(self, sds):
        """addDataSource(SedDataDescription self, SedDataSource sds) -> int"""
        return _libsedml.SedDataDescription_addDataSource(self, sds)

    def getNumDataSources(self):
        """getNumDataSources(SedDataDescription self) -> unsigned int"""
        return _libsedml.SedDataDescription_getNumDataSources(self)

    def createDataSource(self):
        """createDataSource(SedDataDescription self) -> SedDataSource"""
        return _libsedml.SedDataDescription_createDataSource(self)

    def removeDataSource(self, *args):
        """
        removeDataSource(SedDataDescription self, unsigned int n) -> SedDataSource
        removeDataSource(SedDataDescription self, string sid) -> SedDataSource
        """
        return _libsedml.SedDataDescription_removeDataSource(self, *args)

    def getElementName(self):
        """getElementName(SedDataDescription self) -> string"""
        return _libsedml.SedDataDescription_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedDataDescription self) -> int"""
        return _libsedml.SedDataDescription_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedDataDescription self) -> bool"""
        return _libsedml.SedDataDescription_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedDataDescription self)"""
        return _libsedml.SedDataDescription_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedDataDescription self, string id) -> SedBase"""
        return _libsedml.SedDataDescription_getElementBySId(self, id)


_libsedml.SedDataDescription_swigregister(SedDataDescription)

class SedListOfDataDescriptions(SedListOf):
    """Proxy of C++ SedListOfDataDescriptions class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfDataDescriptions self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfDataDescriptions
        __init__(SedListOfDataDescriptions self, SedNamespaces sedmlns) -> SedListOfDataDescriptions
        __init__(SedListOfDataDescriptions self, SedListOfDataDescriptions orig) -> SedListOfDataDescriptions
        """
        _libsedml.SedListOfDataDescriptions_swiginit(self, _libsedml.new_SedListOfDataDescriptions(*args))

    def clone(self):
        """clone(SedListOfDataDescriptions self) -> SedListOfDataDescriptions"""
        return _libsedml.SedListOfDataDescriptions_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfDataDescriptions

    def get(self, *args):
        """
        get(SedListOfDataDescriptions self, unsigned int n) -> SedDataDescription
        get(SedListOfDataDescriptions self, unsigned int n) -> SedDataDescription
        get(SedListOfDataDescriptions self, string sid) -> SedDataDescription
        get(SedListOfDataDescriptions self, string sid) -> SedDataDescription
        """
        return _libsedml.SedListOfDataDescriptions_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfDataDescriptions self, unsigned int n) -> SedDataDescription
        remove(SedListOfDataDescriptions self, string sid) -> SedDataDescription
        """
        return _libsedml.SedListOfDataDescriptions_remove(self, *args)

    def addDataDescription(self, sdd):
        """addDataDescription(SedListOfDataDescriptions self, SedDataDescription sdd) -> int"""
        return _libsedml.SedListOfDataDescriptions_addDataDescription(self, sdd)

    def getNumDataDescriptions(self):
        """getNumDataDescriptions(SedListOfDataDescriptions self) -> unsigned int"""
        return _libsedml.SedListOfDataDescriptions_getNumDataDescriptions(self)

    def createDataDescription(self):
        """createDataDescription(SedListOfDataDescriptions self) -> SedDataDescription"""
        return _libsedml.SedListOfDataDescriptions_createDataDescription(self)

    def getElementName(self):
        """getElementName(SedListOfDataDescriptions self) -> string"""
        return _libsedml.SedListOfDataDescriptions_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfDataDescriptions self) -> int"""
        return _libsedml.SedListOfDataDescriptions_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfDataDescriptions self) -> int"""
        return _libsedml.SedListOfDataDescriptions_getItemTypeCode(self)


_libsedml.SedListOfDataDescriptions_swigregister(SedListOfDataDescriptions)

class SedDataSource(SedBase):
    """Proxy of C++ SedDataSource class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedDataSource self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedDataSource
        __init__(SedDataSource self, SedNamespaces sedmlns) -> SedDataSource
        __init__(SedDataSource self, SedDataSource orig) -> SedDataSource
        """
        _libsedml.SedDataSource_swiginit(self, _libsedml.new_SedDataSource(*args))

    def clone(self):
        """clone(SedDataSource self) -> SedDataSource"""
        return _libsedml.SedDataSource_clone(self)

    __swig_destroy__ = _libsedml.delete_SedDataSource

    def getId(self):
        """getId(SedDataSource self) -> string"""
        return _libsedml.SedDataSource_getId(self)

    def getName(self):
        """getName(SedDataSource self) -> string"""
        return _libsedml.SedDataSource_getName(self)

    def getIndexSet(self):
        """getIndexSet(SedDataSource self) -> string"""
        return _libsedml.SedDataSource_getIndexSet(self)

    def isSetId(self):
        """isSetId(SedDataSource self) -> bool"""
        return _libsedml.SedDataSource_isSetId(self)

    def isSetName(self):
        """isSetName(SedDataSource self) -> bool"""
        return _libsedml.SedDataSource_isSetName(self)

    def isSetIndexSet(self):
        """isSetIndexSet(SedDataSource self) -> bool"""
        return _libsedml.SedDataSource_isSetIndexSet(self)

    def setId(self, id):
        """setId(SedDataSource self, string id) -> int"""
        return _libsedml.SedDataSource_setId(self, id)

    def setName(self, name):
        """setName(SedDataSource self, string name) -> int"""
        return _libsedml.SedDataSource_setName(self, name)

    def setIndexSet(self, indexSet):
        """setIndexSet(SedDataSource self, string indexSet) -> int"""
        return _libsedml.SedDataSource_setIndexSet(self, indexSet)

    def unsetId(self):
        """unsetId(SedDataSource self) -> int"""
        return _libsedml.SedDataSource_unsetId(self)

    def unsetName(self):
        """unsetName(SedDataSource self) -> int"""
        return _libsedml.SedDataSource_unsetName(self)

    def unsetIndexSet(self):
        """unsetIndexSet(SedDataSource self) -> int"""
        return _libsedml.SedDataSource_unsetIndexSet(self)

    def getListOfSlices(self, *args):
        """
        getListOfSlices(SedDataSource self) -> SedListOfSlices
        getListOfSlices(SedDataSource self) -> SedListOfSlices
        """
        return _libsedml.SedDataSource_getListOfSlices(self, *args)

    def getSlice(self, *args):
        """
        getSlice(SedDataSource self, unsigned int n) -> SedSlice
        getSlice(SedDataSource self, unsigned int n) -> SedSlice
        """
        return _libsedml.SedDataSource_getSlice(self, *args)

    def getSliceByReference(self, *args):
        """
        getSliceByReference(SedDataSource self, string sid) -> SedSlice
        getSliceByReference(SedDataSource self, string sid) -> SedSlice
        """
        return _libsedml.SedDataSource_getSliceByReference(self, *args)

    def getSliceByIndex(self, *args):
        """
        getSliceByIndex(SedDataSource self, string sid) -> SedSlice
        getSliceByIndex(SedDataSource self, string sid) -> SedSlice
        """
        return _libsedml.SedDataSource_getSliceByIndex(self, *args)

    def addSlice(self, ss):
        """addSlice(SedDataSource self, SedSlice ss) -> int"""
        return _libsedml.SedDataSource_addSlice(self, ss)

    def getNumSlices(self):
        """getNumSlices(SedDataSource self) -> unsigned int"""
        return _libsedml.SedDataSource_getNumSlices(self)

    def createSlice(self):
        """createSlice(SedDataSource self) -> SedSlice"""
        return _libsedml.SedDataSource_createSlice(self)

    def removeSlice(self, n):
        """removeSlice(SedDataSource self, unsigned int n) -> SedSlice"""
        return _libsedml.SedDataSource_removeSlice(self, n)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedDataSource self, string oldid, string newid)"""
        return _libsedml.SedDataSource_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedDataSource self) -> string"""
        return _libsedml.SedDataSource_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedDataSource self) -> int"""
        return _libsedml.SedDataSource_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedDataSource self) -> bool"""
        return _libsedml.SedDataSource_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedDataSource self)"""
        return _libsedml.SedDataSource_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedDataSource self, string id) -> SedBase"""
        return _libsedml.SedDataSource_getElementBySId(self, id)


_libsedml.SedDataSource_swigregister(SedDataSource)

class SedListOfDataSources(SedListOf):
    """Proxy of C++ SedListOfDataSources class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfDataSources self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfDataSources
        __init__(SedListOfDataSources self, SedNamespaces sedmlns) -> SedListOfDataSources
        __init__(SedListOfDataSources self, SedListOfDataSources orig) -> SedListOfDataSources
        """
        _libsedml.SedListOfDataSources_swiginit(self, _libsedml.new_SedListOfDataSources(*args))

    def clone(self):
        """clone(SedListOfDataSources self) -> SedListOfDataSources"""
        return _libsedml.SedListOfDataSources_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfDataSources

    def get(self, *args):
        """
        get(SedListOfDataSources self, unsigned int n) -> SedDataSource
        get(SedListOfDataSources self, unsigned int n) -> SedDataSource
        get(SedListOfDataSources self, string sid) -> SedDataSource
        get(SedListOfDataSources self, string sid) -> SedDataSource
        """
        return _libsedml.SedListOfDataSources_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfDataSources self, unsigned int n) -> SedDataSource
        remove(SedListOfDataSources self, string sid) -> SedDataSource
        """
        return _libsedml.SedListOfDataSources_remove(self, *args)

    def addDataSource(self, sds):
        """addDataSource(SedListOfDataSources self, SedDataSource sds) -> int"""
        return _libsedml.SedListOfDataSources_addDataSource(self, sds)

    def getNumDataSources(self):
        """getNumDataSources(SedListOfDataSources self) -> unsigned int"""
        return _libsedml.SedListOfDataSources_getNumDataSources(self)

    def createDataSource(self):
        """createDataSource(SedListOfDataSources self) -> SedDataSource"""
        return _libsedml.SedListOfDataSources_createDataSource(self)

    def getByIndexSet(self, *args):
        """
        getByIndexSet(SedListOfDataSources self, string sid) -> SedDataSource
        getByIndexSet(SedListOfDataSources self, string sid) -> SedDataSource
        """
        return _libsedml.SedListOfDataSources_getByIndexSet(self, *args)

    def getElementName(self):
        """getElementName(SedListOfDataSources self) -> string"""
        return _libsedml.SedListOfDataSources_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfDataSources self) -> int"""
        return _libsedml.SedListOfDataSources_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfDataSources self) -> int"""
        return _libsedml.SedListOfDataSources_getItemTypeCode(self)


_libsedml.SedListOfDataSources_swigregister(SedListOfDataSources)

class SedSlice(SedBase):
    """Proxy of C++ SedSlice class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedSlice self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedSlice
        __init__(SedSlice self, SedNamespaces sedmlns) -> SedSlice
        __init__(SedSlice self, SedSlice orig) -> SedSlice
        """
        _libsedml.SedSlice_swiginit(self, _libsedml.new_SedSlice(*args))

    def clone(self):
        """clone(SedSlice self) -> SedSlice"""
        return _libsedml.SedSlice_clone(self)

    __swig_destroy__ = _libsedml.delete_SedSlice

    def getReference(self):
        """getReference(SedSlice self) -> string"""
        return _libsedml.SedSlice_getReference(self)

    def getValue(self):
        """getValue(SedSlice self) -> string"""
        return _libsedml.SedSlice_getValue(self)

    def getIndex(self):
        """getIndex(SedSlice self) -> string"""
        return _libsedml.SedSlice_getIndex(self)

    def getStartIndex(self):
        """getStartIndex(SedSlice self) -> int"""
        return _libsedml.SedSlice_getStartIndex(self)

    def getEndIndex(self):
        """getEndIndex(SedSlice self) -> int"""
        return _libsedml.SedSlice_getEndIndex(self)

    def isSetReference(self):
        """isSetReference(SedSlice self) -> bool"""
        return _libsedml.SedSlice_isSetReference(self)

    def isSetValue(self):
        """isSetValue(SedSlice self) -> bool"""
        return _libsedml.SedSlice_isSetValue(self)

    def isSetIndex(self):
        """isSetIndex(SedSlice self) -> bool"""
        return _libsedml.SedSlice_isSetIndex(self)

    def isSetStartIndex(self):
        """isSetStartIndex(SedSlice self) -> bool"""
        return _libsedml.SedSlice_isSetStartIndex(self)

    def isSetEndIndex(self):
        """isSetEndIndex(SedSlice self) -> bool"""
        return _libsedml.SedSlice_isSetEndIndex(self)

    def setReference(self, reference):
        """setReference(SedSlice self, string reference) -> int"""
        return _libsedml.SedSlice_setReference(self, reference)

    def setValue(self, value):
        """setValue(SedSlice self, string value) -> int"""
        return _libsedml.SedSlice_setValue(self, value)

    def setIndex(self, index):
        """setIndex(SedSlice self, string index) -> int"""
        return _libsedml.SedSlice_setIndex(self, index)

    def setStartIndex(self, startIndex):
        """setStartIndex(SedSlice self, int startIndex) -> int"""
        return _libsedml.SedSlice_setStartIndex(self, startIndex)

    def setEndIndex(self, endIndex):
        """setEndIndex(SedSlice self, int endIndex) -> int"""
        return _libsedml.SedSlice_setEndIndex(self, endIndex)

    def unsetReference(self):
        """unsetReference(SedSlice self) -> int"""
        return _libsedml.SedSlice_unsetReference(self)

    def unsetValue(self):
        """unsetValue(SedSlice self) -> int"""
        return _libsedml.SedSlice_unsetValue(self)

    def unsetIndex(self):
        """unsetIndex(SedSlice self) -> int"""
        return _libsedml.SedSlice_unsetIndex(self)

    def unsetStartIndex(self):
        """unsetStartIndex(SedSlice self) -> int"""
        return _libsedml.SedSlice_unsetStartIndex(self)

    def unsetEndIndex(self):
        """unsetEndIndex(SedSlice self) -> int"""
        return _libsedml.SedSlice_unsetEndIndex(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedSlice self, string oldid, string newid)"""
        return _libsedml.SedSlice_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedSlice self) -> string"""
        return _libsedml.SedSlice_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedSlice self) -> int"""
        return _libsedml.SedSlice_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedSlice self) -> bool"""
        return _libsedml.SedSlice_hasRequiredAttributes(self)


_libsedml.SedSlice_swigregister(SedSlice)

class SedListOfSlices(SedListOf):
    """Proxy of C++ SedListOfSlices class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfSlices self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfSlices
        __init__(SedListOfSlices self, SedNamespaces sedmlns) -> SedListOfSlices
        __init__(SedListOfSlices self, SedListOfSlices orig) -> SedListOfSlices
        """
        _libsedml.SedListOfSlices_swiginit(self, _libsedml.new_SedListOfSlices(*args))

    def clone(self):
        """clone(SedListOfSlices self) -> SedListOfSlices"""
        return _libsedml.SedListOfSlices_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfSlices

    def get(self, *args):
        """
        get(SedListOfSlices self, unsigned int n) -> SedSlice
        get(SedListOfSlices self, unsigned int n) -> SedSlice
        get(SedListOfSlices self, string sid) -> SedSlice
        get(SedListOfSlices self, string sid) -> SedSlice
        """
        return _libsedml.SedListOfSlices_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfSlices self, unsigned int n) -> SedSlice
        remove(SedListOfSlices self, string sid) -> SedSlice
        """
        return _libsedml.SedListOfSlices_remove(self, *args)

    def addSlice(self, ss):
        """addSlice(SedListOfSlices self, SedSlice ss) -> int"""
        return _libsedml.SedListOfSlices_addSlice(self, ss)

    def getNumSlices(self):
        """getNumSlices(SedListOfSlices self) -> unsigned int"""
        return _libsedml.SedListOfSlices_getNumSlices(self)

    def createSlice(self):
        """createSlice(SedListOfSlices self) -> SedSlice"""
        return _libsedml.SedListOfSlices_createSlice(self)

    def getByReference(self, *args):
        """
        getByReference(SedListOfSlices self, string sid) -> SedSlice
        getByReference(SedListOfSlices self, string sid) -> SedSlice
        """
        return _libsedml.SedListOfSlices_getByReference(self, *args)

    def getByIndex(self, *args):
        """
        getByIndex(SedListOfSlices self, string sid) -> SedSlice
        getByIndex(SedListOfSlices self, string sid) -> SedSlice
        """
        return _libsedml.SedListOfSlices_getByIndex(self, *args)

    def getElementName(self):
        """getElementName(SedListOfSlices self) -> string"""
        return _libsedml.SedListOfSlices_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfSlices self) -> int"""
        return _libsedml.SedListOfSlices_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfSlices self) -> int"""
        return _libsedml.SedListOfSlices_getItemTypeCode(self)


_libsedml.SedListOfSlices_swigregister(SedListOfSlices)

class SedParameterEstimationTask(SedAbstractTask):
    """Proxy of C++ SedParameterEstimationTask class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedParameterEstimationTask self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedParameterEstimationTask
        __init__(SedParameterEstimationTask self, SedNamespaces sedmlns) -> SedParameterEstimationTask
        __init__(SedParameterEstimationTask self, SedParameterEstimationTask orig) -> SedParameterEstimationTask
        """
        _libsedml.SedParameterEstimationTask_swiginit(self, _libsedml.new_SedParameterEstimationTask(*args))

    def clone(self):
        """clone(SedParameterEstimationTask self) -> SedParameterEstimationTask"""
        return _libsedml.SedParameterEstimationTask_clone(self)

    __swig_destroy__ = _libsedml.delete_SedParameterEstimationTask

    def getAlgorithm(self, *args):
        """
        getAlgorithm(SedParameterEstimationTask self) -> SedAlgorithm
        getAlgorithm(SedParameterEstimationTask self) -> SedAlgorithm
        """
        return _libsedml.SedParameterEstimationTask_getAlgorithm(self, *args)

    def getObjective(self, *args):
        """
        getObjective(SedParameterEstimationTask self) -> SedObjective
        getObjective(SedParameterEstimationTask self) -> SedObjective
        """
        return _libsedml.SedParameterEstimationTask_getObjective(self, *args)

    def isSetAlgorithm(self):
        """isSetAlgorithm(SedParameterEstimationTask self) -> bool"""
        return _libsedml.SedParameterEstimationTask_isSetAlgorithm(self)

    def isSetObjective(self):
        """isSetObjective(SedParameterEstimationTask self) -> bool"""
        return _libsedml.SedParameterEstimationTask_isSetObjective(self)

    def setAlgorithm(self, algorithm):
        """setAlgorithm(SedParameterEstimationTask self, SedAlgorithm algorithm) -> int"""
        return _libsedml.SedParameterEstimationTask_setAlgorithm(self, algorithm)

    def setObjective(self, objective):
        """setObjective(SedParameterEstimationTask self, SedObjective objective) -> int"""
        return _libsedml.SedParameterEstimationTask_setObjective(self, objective)

    def createAlgorithm(self):
        """createAlgorithm(SedParameterEstimationTask self) -> SedAlgorithm"""
        return _libsedml.SedParameterEstimationTask_createAlgorithm(self)

    def createLeastSquareObjectiveFunction(self):
        """createLeastSquareObjectiveFunction(SedParameterEstimationTask self) -> SedLeastSquareObjectiveFunction"""
        return _libsedml.SedParameterEstimationTask_createLeastSquareObjectiveFunction(self)

    def unsetAlgorithm(self):
        """unsetAlgorithm(SedParameterEstimationTask self) -> int"""
        return _libsedml.SedParameterEstimationTask_unsetAlgorithm(self)

    def unsetObjective(self):
        """unsetObjective(SedParameterEstimationTask self) -> int"""
        return _libsedml.SedParameterEstimationTask_unsetObjective(self)

    def getListOfAdjustableParameters(self, *args):
        """
        getListOfAdjustableParameters(SedParameterEstimationTask self) -> SedListOfAdjustableParameters
        getListOfAdjustableParameters(SedParameterEstimationTask self) -> SedListOfAdjustableParameters
        """
        return _libsedml.SedParameterEstimationTask_getListOfAdjustableParameters(self, *args)

    def getAdjustableParameter(self, *args):
        """
        getAdjustableParameter(SedParameterEstimationTask self, unsigned int n) -> SedAdjustableParameter
        getAdjustableParameter(SedParameterEstimationTask self, unsigned int n) -> SedAdjustableParameter
        """
        return _libsedml.SedParameterEstimationTask_getAdjustableParameter(self, *args)

    def getAdjustableParameterByModelReference(self, *args):
        """
        getAdjustableParameterByModelReference(SedParameterEstimationTask self, string sid) -> SedAdjustableParameter
        getAdjustableParameterByModelReference(SedParameterEstimationTask self, string sid) -> SedAdjustableParameter
        """
        return _libsedml.SedParameterEstimationTask_getAdjustableParameterByModelReference(self, *args)

    def addAdjustableParameter(self, sap):
        """addAdjustableParameter(SedParameterEstimationTask self, SedAdjustableParameter sap) -> int"""
        return _libsedml.SedParameterEstimationTask_addAdjustableParameter(self, sap)

    def getNumAdjustableParameters(self):
        """getNumAdjustableParameters(SedParameterEstimationTask self) -> unsigned int"""
        return _libsedml.SedParameterEstimationTask_getNumAdjustableParameters(self)

    def createAdjustableParameter(self):
        """createAdjustableParameter(SedParameterEstimationTask self) -> SedAdjustableParameter"""
        return _libsedml.SedParameterEstimationTask_createAdjustableParameter(self)

    def removeAdjustableParameter(self, n):
        """removeAdjustableParameter(SedParameterEstimationTask self, unsigned int n) -> SedAdjustableParameter"""
        return _libsedml.SedParameterEstimationTask_removeAdjustableParameter(self, n)

    def getListOfFitExperiments(self, *args):
        """
        getListOfFitExperiments(SedParameterEstimationTask self) -> SedListOfFitExperiments
        getListOfFitExperiments(SedParameterEstimationTask self) -> SedListOfFitExperiments
        """
        return _libsedml.SedParameterEstimationTask_getListOfFitExperiments(self, *args)

    def getFitExperiment(self, *args):
        """
        getFitExperiment(SedParameterEstimationTask self, unsigned int n) -> SedFitExperiment
        getFitExperiment(SedParameterEstimationTask self, unsigned int n) -> SedFitExperiment
        getFitExperiment(SedParameterEstimationTask self, string sid) -> SedFitExperiment
        getFitExperiment(SedParameterEstimationTask self, string sid) -> SedFitExperiment
        """
        return _libsedml.SedParameterEstimationTask_getFitExperiment(self, *args)

    def addFitExperiment(self, sfe):
        """addFitExperiment(SedParameterEstimationTask self, SedFitExperiment sfe) -> int"""
        return _libsedml.SedParameterEstimationTask_addFitExperiment(self, sfe)

    def getNumFitExperiments(self):
        """getNumFitExperiments(SedParameterEstimationTask self) -> unsigned int"""
        return _libsedml.SedParameterEstimationTask_getNumFitExperiments(self)

    def createFitExperiment(self):
        """createFitExperiment(SedParameterEstimationTask self) -> SedFitExperiment"""
        return _libsedml.SedParameterEstimationTask_createFitExperiment(self)

    def removeFitExperiment(self, *args):
        """
        removeFitExperiment(SedParameterEstimationTask self, unsigned int n) -> SedFitExperiment
        removeFitExperiment(SedParameterEstimationTask self, string sid) -> SedFitExperiment
        """
        return _libsedml.SedParameterEstimationTask_removeFitExperiment(self, *args)

    def getElementName(self):
        """getElementName(SedParameterEstimationTask self) -> string"""
        return _libsedml.SedParameterEstimationTask_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedParameterEstimationTask self) -> int"""
        return _libsedml.SedParameterEstimationTask_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedParameterEstimationTask self) -> bool"""
        return _libsedml.SedParameterEstimationTask_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedParameterEstimationTask self) -> bool"""
        return _libsedml.SedParameterEstimationTask_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedParameterEstimationTask self)"""
        return _libsedml.SedParameterEstimationTask_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedParameterEstimationTask self, string id) -> SedBase"""
        return _libsedml.SedParameterEstimationTask_getElementBySId(self, id)


_libsedml.SedParameterEstimationTask_swigregister(SedParameterEstimationTask)

class SedObjective(SedBase):
    """Proxy of C++ SedObjective class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedObjective self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedObjective
        __init__(SedObjective self, SedNamespaces sedmlns) -> SedObjective
        __init__(SedObjective self, SedObjective orig) -> SedObjective
        """
        _libsedml.SedObjective_swiginit(self, _libsedml.new_SedObjective(*args))

    def clone(self):
        """clone(SedObjective self) -> SedObjective"""
        return _libsedml.SedObjective_clone(self)

    __swig_destroy__ = _libsedml.delete_SedObjective

    def isSedLeastSquareObjectiveFunction(self):
        """isSedLeastSquareObjectiveFunction(SedObjective self) -> bool"""
        return _libsedml.SedObjective_isSedLeastSquareObjectiveFunction(self)

    def getElementName(self):
        """getElementName(SedObjective self) -> string"""
        return _libsedml.SedObjective_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedObjective self, string name)"""
        return _libsedml.SedObjective_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedObjective self) -> int"""
        return _libsedml.SedObjective_getTypeCode(self)


_libsedml.SedObjective_swigregister(SedObjective)

class SedLeastSquareObjectiveFunction(SedObjective):
    """Proxy of C++ SedLeastSquareObjectiveFunction class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedLeastSquareObjectiveFunction self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedLeastSquareObjectiveFunction
        __init__(SedLeastSquareObjectiveFunction self, SedNamespaces sedmlns) -> SedLeastSquareObjectiveFunction
        __init__(SedLeastSquareObjectiveFunction self, SedLeastSquareObjectiveFunction orig) -> SedLeastSquareObjectiveFunction
        """
        _libsedml.SedLeastSquareObjectiveFunction_swiginit(self, _libsedml.new_SedLeastSquareObjectiveFunction(*args))

    def clone(self):
        """clone(SedLeastSquareObjectiveFunction self) -> SedLeastSquareObjectiveFunction"""
        return _libsedml.SedLeastSquareObjectiveFunction_clone(self)

    __swig_destroy__ = _libsedml.delete_SedLeastSquareObjectiveFunction

    def getElementName(self):
        """getElementName(SedLeastSquareObjectiveFunction self) -> string"""
        return _libsedml.SedLeastSquareObjectiveFunction_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedLeastSquareObjectiveFunction self) -> int"""
        return _libsedml.SedLeastSquareObjectiveFunction_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedLeastSquareObjectiveFunction self) -> bool"""
        return _libsedml.SedLeastSquareObjectiveFunction_hasRequiredAttributes(self)


_libsedml.SedLeastSquareObjectiveFunction_swigregister(SedLeastSquareObjectiveFunction)

class SedAdjustableParameter(SedBase):
    """Proxy of C++ SedAdjustableParameter class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedAdjustableParameter self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedAdjustableParameter
        __init__(SedAdjustableParameter self, SedNamespaces sedmlns) -> SedAdjustableParameter
        __init__(SedAdjustableParameter self, SedAdjustableParameter orig) -> SedAdjustableParameter
        """
        _libsedml.SedAdjustableParameter_swiginit(self, _libsedml.new_SedAdjustableParameter(*args))

    def clone(self):
        """clone(SedAdjustableParameter self) -> SedAdjustableParameter"""
        return _libsedml.SedAdjustableParameter_clone(self)

    __swig_destroy__ = _libsedml.delete_SedAdjustableParameter

    def getInitialValue(self):
        """getInitialValue(SedAdjustableParameter self) -> double"""
        return _libsedml.SedAdjustableParameter_getInitialValue(self)

    def getModelReference(self):
        """getModelReference(SedAdjustableParameter self) -> string"""
        return _libsedml.SedAdjustableParameter_getModelReference(self)

    def getTarget(self):
        """getTarget(SedAdjustableParameter self) -> string"""
        return _libsedml.SedAdjustableParameter_getTarget(self)

    def isSetInitialValue(self):
        """isSetInitialValue(SedAdjustableParameter self) -> bool"""
        return _libsedml.SedAdjustableParameter_isSetInitialValue(self)

    def isSetModelReference(self):
        """isSetModelReference(SedAdjustableParameter self) -> bool"""
        return _libsedml.SedAdjustableParameter_isSetModelReference(self)

    def isSetTarget(self):
        """isSetTarget(SedAdjustableParameter self) -> bool"""
        return _libsedml.SedAdjustableParameter_isSetTarget(self)

    def setInitialValue(self, initialValue):
        """setInitialValue(SedAdjustableParameter self, double initialValue) -> int"""
        return _libsedml.SedAdjustableParameter_setInitialValue(self, initialValue)

    def setModelReference(self, modelReference):
        """setModelReference(SedAdjustableParameter self, string modelReference) -> int"""
        return _libsedml.SedAdjustableParameter_setModelReference(self, modelReference)

    def setTarget(self, target):
        """setTarget(SedAdjustableParameter self, string target) -> int"""
        return _libsedml.SedAdjustableParameter_setTarget(self, target)

    def unsetInitialValue(self):
        """unsetInitialValue(SedAdjustableParameter self) -> int"""
        return _libsedml.SedAdjustableParameter_unsetInitialValue(self)

    def unsetModelReference(self):
        """unsetModelReference(SedAdjustableParameter self) -> int"""
        return _libsedml.SedAdjustableParameter_unsetModelReference(self)

    def unsetTarget(self):
        """unsetTarget(SedAdjustableParameter self) -> int"""
        return _libsedml.SedAdjustableParameter_unsetTarget(self)

    def getBounds(self, *args):
        """
        getBounds(SedAdjustableParameter self) -> SedBounds
        getBounds(SedAdjustableParameter self) -> SedBounds
        """
        return _libsedml.SedAdjustableParameter_getBounds(self, *args)

    def isSetBounds(self):
        """isSetBounds(SedAdjustableParameter self) -> bool"""
        return _libsedml.SedAdjustableParameter_isSetBounds(self)

    def setBounds(self, bounds):
        """setBounds(SedAdjustableParameter self, SedBounds bounds) -> int"""
        return _libsedml.SedAdjustableParameter_setBounds(self, bounds)

    def createBounds(self):
        """createBounds(SedAdjustableParameter self) -> SedBounds"""
        return _libsedml.SedAdjustableParameter_createBounds(self)

    def unsetBounds(self):
        """unsetBounds(SedAdjustableParameter self) -> int"""
        return _libsedml.SedAdjustableParameter_unsetBounds(self)

    def getListOfExperimentRefs(self, *args):
        """
        getListOfExperimentRefs(SedAdjustableParameter self) -> SedListOfExperimentRefs
        getListOfExperimentRefs(SedAdjustableParameter self) -> SedListOfExperimentRefs
        """
        return _libsedml.SedAdjustableParameter_getListOfExperimentRefs(self, *args)

    def getExperimentRef(self, *args):
        """
        getExperimentRef(SedAdjustableParameter self, unsigned int n) -> SedExperimentRef
        getExperimentRef(SedAdjustableParameter self, unsigned int n) -> SedExperimentRef
        """
        return _libsedml.SedAdjustableParameter_getExperimentRef(self, *args)

    def getExperimentRefByExperimentId(self, *args):
        """
        getExperimentRefByExperimentId(SedAdjustableParameter self, string sid) -> SedExperimentRef
        getExperimentRefByExperimentId(SedAdjustableParameter self, string sid) -> SedExperimentRef
        """
        return _libsedml.SedAdjustableParameter_getExperimentRefByExperimentId(self, *args)

    def addExperimentRef(self, ser):
        """addExperimentRef(SedAdjustableParameter self, SedExperimentRef ser) -> int"""
        return _libsedml.SedAdjustableParameter_addExperimentRef(self, ser)

    def getNumExperimentRefs(self):
        """getNumExperimentRefs(SedAdjustableParameter self) -> unsigned int"""
        return _libsedml.SedAdjustableParameter_getNumExperimentRefs(self)

    def createExperimentRef(self):
        """createExperimentRef(SedAdjustableParameter self) -> SedExperimentRef"""
        return _libsedml.SedAdjustableParameter_createExperimentRef(self)

    def removeExperimentRef(self, n):
        """removeExperimentRef(SedAdjustableParameter self, unsigned int n) -> SedExperimentRef"""
        return _libsedml.SedAdjustableParameter_removeExperimentRef(self, n)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedAdjustableParameter self, string oldid, string newid)"""
        return _libsedml.SedAdjustableParameter_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedAdjustableParameter self) -> string"""
        return _libsedml.SedAdjustableParameter_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedAdjustableParameter self) -> int"""
        return _libsedml.SedAdjustableParameter_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedAdjustableParameter self) -> bool"""
        return _libsedml.SedAdjustableParameter_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedAdjustableParameter self) -> bool"""
        return _libsedml.SedAdjustableParameter_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedAdjustableParameter self)"""
        return _libsedml.SedAdjustableParameter_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedAdjustableParameter self, string id) -> SedBase"""
        return _libsedml.SedAdjustableParameter_getElementBySId(self, id)


_libsedml.SedAdjustableParameter_swigregister(SedAdjustableParameter)

class SedListOfAdjustableParameters(SedListOf):
    """Proxy of C++ SedListOfAdjustableParameters class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfAdjustableParameters self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfAdjustableParameters
        __init__(SedListOfAdjustableParameters self, SedNamespaces sedmlns) -> SedListOfAdjustableParameters
        __init__(SedListOfAdjustableParameters self, SedListOfAdjustableParameters orig) -> SedListOfAdjustableParameters
        """
        _libsedml.SedListOfAdjustableParameters_swiginit(self, _libsedml.new_SedListOfAdjustableParameters(*args))

    def clone(self):
        """clone(SedListOfAdjustableParameters self) -> SedListOfAdjustableParameters"""
        return _libsedml.SedListOfAdjustableParameters_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfAdjustableParameters

    def get(self, *args):
        """
        get(SedListOfAdjustableParameters self, unsigned int n) -> SedAdjustableParameter
        get(SedListOfAdjustableParameters self, unsigned int n) -> SedAdjustableParameter
        get(SedListOfAdjustableParameters self, string sid) -> SedAdjustableParameter
        get(SedListOfAdjustableParameters self, string sid) -> SedAdjustableParameter
        """
        return _libsedml.SedListOfAdjustableParameters_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfAdjustableParameters self, unsigned int n) -> SedAdjustableParameter
        remove(SedListOfAdjustableParameters self, string sid) -> SedAdjustableParameter
        """
        return _libsedml.SedListOfAdjustableParameters_remove(self, *args)

    def addAdjustableParameter(self, sap):
        """addAdjustableParameter(SedListOfAdjustableParameters self, SedAdjustableParameter sap) -> int"""
        return _libsedml.SedListOfAdjustableParameters_addAdjustableParameter(self, sap)

    def getNumAdjustableParameters(self):
        """getNumAdjustableParameters(SedListOfAdjustableParameters self) -> unsigned int"""
        return _libsedml.SedListOfAdjustableParameters_getNumAdjustableParameters(self)

    def createAdjustableParameter(self):
        """createAdjustableParameter(SedListOfAdjustableParameters self) -> SedAdjustableParameter"""
        return _libsedml.SedListOfAdjustableParameters_createAdjustableParameter(self)

    def getByModelReference(self, *args):
        """
        getByModelReference(SedListOfAdjustableParameters self, string sid) -> SedAdjustableParameter
        getByModelReference(SedListOfAdjustableParameters self, string sid) -> SedAdjustableParameter
        """
        return _libsedml.SedListOfAdjustableParameters_getByModelReference(self, *args)

    def getElementName(self):
        """getElementName(SedListOfAdjustableParameters self) -> string"""
        return _libsedml.SedListOfAdjustableParameters_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfAdjustableParameters self) -> int"""
        return _libsedml.SedListOfAdjustableParameters_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfAdjustableParameters self) -> int"""
        return _libsedml.SedListOfAdjustableParameters_getItemTypeCode(self)


_libsedml.SedListOfAdjustableParameters_swigregister(SedListOfAdjustableParameters)

class SedExperimentRef(SedBase):
    """Proxy of C++ SedExperimentRef class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedExperimentRef self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedExperimentRef
        __init__(SedExperimentRef self, SedNamespaces sedmlns) -> SedExperimentRef
        __init__(SedExperimentRef self, SedExperimentRef orig) -> SedExperimentRef
        """
        _libsedml.SedExperimentRef_swiginit(self, _libsedml.new_SedExperimentRef(*args))

    def clone(self):
        """clone(SedExperimentRef self) -> SedExperimentRef"""
        return _libsedml.SedExperimentRef_clone(self)

    __swig_destroy__ = _libsedml.delete_SedExperimentRef

    def getExperimentId(self):
        """getExperimentId(SedExperimentRef self) -> string"""
        return _libsedml.SedExperimentRef_getExperimentId(self)

    def isSetExperimentId(self):
        """isSetExperimentId(SedExperimentRef self) -> bool"""
        return _libsedml.SedExperimentRef_isSetExperimentId(self)

    def setExperimentId(self, experimentId):
        """setExperimentId(SedExperimentRef self, string experimentId) -> int"""
        return _libsedml.SedExperimentRef_setExperimentId(self, experimentId)

    def unsetExperimentId(self):
        """unsetExperimentId(SedExperimentRef self) -> int"""
        return _libsedml.SedExperimentRef_unsetExperimentId(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedExperimentRef self, string oldid, string newid)"""
        return _libsedml.SedExperimentRef_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedExperimentRef self) -> string"""
        return _libsedml.SedExperimentRef_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedExperimentRef self) -> int"""
        return _libsedml.SedExperimentRef_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedExperimentRef self) -> bool"""
        return _libsedml.SedExperimentRef_hasRequiredAttributes(self)


_libsedml.SedExperimentRef_swigregister(SedExperimentRef)

class SedListOfExperimentRefs(SedListOf):
    """Proxy of C++ SedListOfExperimentRefs class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfExperimentRefs self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfExperimentRefs
        __init__(SedListOfExperimentRefs self, SedNamespaces sedmlns) -> SedListOfExperimentRefs
        __init__(SedListOfExperimentRefs self, SedListOfExperimentRefs orig) -> SedListOfExperimentRefs
        """
        _libsedml.SedListOfExperimentRefs_swiginit(self, _libsedml.new_SedListOfExperimentRefs(*args))

    def clone(self):
        """clone(SedListOfExperimentRefs self) -> SedListOfExperimentRefs"""
        return _libsedml.SedListOfExperimentRefs_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfExperimentRefs

    def get(self, *args):
        """
        get(SedListOfExperimentRefs self, unsigned int n) -> SedExperimentRef
        get(SedListOfExperimentRefs self, unsigned int n) -> SedExperimentRef
        get(SedListOfExperimentRefs self, string sid) -> SedExperimentRef
        get(SedListOfExperimentRefs self, string sid) -> SedExperimentRef
        """
        return _libsedml.SedListOfExperimentRefs_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfExperimentRefs self, unsigned int n) -> SedExperimentRef
        remove(SedListOfExperimentRefs self, string sid) -> SedExperimentRef
        """
        return _libsedml.SedListOfExperimentRefs_remove(self, *args)

    def addExperimentRef(self, ser):
        """addExperimentRef(SedListOfExperimentRefs self, SedExperimentRef ser) -> int"""
        return _libsedml.SedListOfExperimentRefs_addExperimentRef(self, ser)

    def getNumExperimentRefs(self):
        """getNumExperimentRefs(SedListOfExperimentRefs self) -> unsigned int"""
        return _libsedml.SedListOfExperimentRefs_getNumExperimentRefs(self)

    def createExperimentRef(self):
        """createExperimentRef(SedListOfExperimentRefs self) -> SedExperimentRef"""
        return _libsedml.SedListOfExperimentRefs_createExperimentRef(self)

    def getByExperimentId(self, *args):
        """
        getByExperimentId(SedListOfExperimentRefs self, string sid) -> SedExperimentRef
        getByExperimentId(SedListOfExperimentRefs self, string sid) -> SedExperimentRef
        """
        return _libsedml.SedListOfExperimentRefs_getByExperimentId(self, *args)

    def getElementName(self):
        """getElementName(SedListOfExperimentRefs self) -> string"""
        return _libsedml.SedListOfExperimentRefs_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfExperimentRefs self) -> int"""
        return _libsedml.SedListOfExperimentRefs_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfExperimentRefs self) -> int"""
        return _libsedml.SedListOfExperimentRefs_getItemTypeCode(self)


_libsedml.SedListOfExperimentRefs_swigregister(SedListOfExperimentRefs)

class SedFitExperiment(SedBase):
    """Proxy of C++ SedFitExperiment class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedFitExperiment self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedFitExperiment
        __init__(SedFitExperiment self, SedNamespaces sedmlns) -> SedFitExperiment
        __init__(SedFitExperiment self, SedFitExperiment orig) -> SedFitExperiment
        """
        _libsedml.SedFitExperiment_swiginit(self, _libsedml.new_SedFitExperiment(*args))

    def clone(self):
        """clone(SedFitExperiment self) -> SedFitExperiment"""
        return _libsedml.SedFitExperiment_clone(self)

    __swig_destroy__ = _libsedml.delete_SedFitExperiment

    def getId(self):
        """getId(SedFitExperiment self) -> string"""
        return _libsedml.SedFitExperiment_getId(self)

    def getType(self):
        """getType(SedFitExperiment self) -> ExperimentType_t"""
        return _libsedml.SedFitExperiment_getType(self)

    def getTypeAsString(self):
        """getTypeAsString(SedFitExperiment self) -> string"""
        return _libsedml.SedFitExperiment_getTypeAsString(self)

    def isSetId(self):
        """isSetId(SedFitExperiment self) -> bool"""
        return _libsedml.SedFitExperiment_isSetId(self)

    def isSetType(self):
        """isSetType(SedFitExperiment self) -> bool"""
        return _libsedml.SedFitExperiment_isSetType(self)

    def setId(self, id):
        """setId(SedFitExperiment self, string id) -> int"""
        return _libsedml.SedFitExperiment_setId(self, id)

    def setType(self, *args):
        """
        setType(SedFitExperiment self, ExperimentType_t const type) -> int
        setType(SedFitExperiment self, string type) -> int
        """
        return _libsedml.SedFitExperiment_setType(self, *args)

    def unsetId(self):
        """unsetId(SedFitExperiment self) -> int"""
        return _libsedml.SedFitExperiment_unsetId(self)

    def unsetType(self):
        """unsetType(SedFitExperiment self) -> int"""
        return _libsedml.SedFitExperiment_unsetType(self)

    def getAlgorithm(self, *args):
        """
        getAlgorithm(SedFitExperiment self) -> SedAlgorithm
        getAlgorithm(SedFitExperiment self) -> SedAlgorithm
        """
        return _libsedml.SedFitExperiment_getAlgorithm(self, *args)

    def isSetAlgorithm(self):
        """isSetAlgorithm(SedFitExperiment self) -> bool"""
        return _libsedml.SedFitExperiment_isSetAlgorithm(self)

    def setAlgorithm(self, algorithm):
        """setAlgorithm(SedFitExperiment self, SedAlgorithm algorithm) -> int"""
        return _libsedml.SedFitExperiment_setAlgorithm(self, algorithm)

    def createAlgorithm(self):
        """createAlgorithm(SedFitExperiment self) -> SedAlgorithm"""
        return _libsedml.SedFitExperiment_createAlgorithm(self)

    def unsetAlgorithm(self):
        """unsetAlgorithm(SedFitExperiment self) -> int"""
        return _libsedml.SedFitExperiment_unsetAlgorithm(self)

    def getListOfFitMappings(self, *args):
        """
        getListOfFitMappings(SedFitExperiment self) -> SedListOfFitMappings
        getListOfFitMappings(SedFitExperiment self) -> SedListOfFitMappings
        """
        return _libsedml.SedFitExperiment_getListOfFitMappings(self, *args)

    def getFitMapping(self, *args):
        """
        getFitMapping(SedFitExperiment self, unsigned int n) -> SedFitMapping
        getFitMapping(SedFitExperiment self, unsigned int n) -> SedFitMapping
        """
        return _libsedml.SedFitExperiment_getFitMapping(self, *args)

    def getFitMappingByDataSource(self, *args):
        """
        getFitMappingByDataSource(SedFitExperiment self, string sid) -> SedFitMapping
        getFitMappingByDataSource(SedFitExperiment self, string sid) -> SedFitMapping
        """
        return _libsedml.SedFitExperiment_getFitMappingByDataSource(self, *args)

    def getFitMappingByTarget(self, *args):
        """
        getFitMappingByTarget(SedFitExperiment self, string sid) -> SedFitMapping
        getFitMappingByTarget(SedFitExperiment self, string sid) -> SedFitMapping
        """
        return _libsedml.SedFitExperiment_getFitMappingByTarget(self, *args)

    def getFitMappingByPointWeight(self, *args):
        """
        getFitMappingByPointWeight(SedFitExperiment self, string sid) -> SedFitMapping
        getFitMappingByPointWeight(SedFitExperiment self, string sid) -> SedFitMapping
        """
        return _libsedml.SedFitExperiment_getFitMappingByPointWeight(self, *args)

    def addFitMapping(self, sfm):
        """addFitMapping(SedFitExperiment self, SedFitMapping sfm) -> int"""
        return _libsedml.SedFitExperiment_addFitMapping(self, sfm)

    def getNumFitMappings(self):
        """getNumFitMappings(SedFitExperiment self) -> unsigned int"""
        return _libsedml.SedFitExperiment_getNumFitMappings(self)

    def createFitMapping(self):
        """createFitMapping(SedFitExperiment self) -> SedFitMapping"""
        return _libsedml.SedFitExperiment_createFitMapping(self)

    def removeFitMapping(self, n):
        """removeFitMapping(SedFitExperiment self, unsigned int n) -> SedFitMapping"""
        return _libsedml.SedFitExperiment_removeFitMapping(self, n)

    def getElementName(self):
        """getElementName(SedFitExperiment self) -> string"""
        return _libsedml.SedFitExperiment_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedFitExperiment self) -> int"""
        return _libsedml.SedFitExperiment_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedFitExperiment self) -> bool"""
        return _libsedml.SedFitExperiment_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedFitExperiment self)"""
        return _libsedml.SedFitExperiment_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedFitExperiment self, string id) -> SedBase"""
        return _libsedml.SedFitExperiment_getElementBySId(self, id)


_libsedml.SedFitExperiment_swigregister(SedFitExperiment)

class SedListOfFitExperiments(SedListOf):
    """Proxy of C++ SedListOfFitExperiments class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfFitExperiments self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfFitExperiments
        __init__(SedListOfFitExperiments self, SedNamespaces sedmlns) -> SedListOfFitExperiments
        __init__(SedListOfFitExperiments self, SedListOfFitExperiments orig) -> SedListOfFitExperiments
        """
        _libsedml.SedListOfFitExperiments_swiginit(self, _libsedml.new_SedListOfFitExperiments(*args))

    def clone(self):
        """clone(SedListOfFitExperiments self) -> SedListOfFitExperiments"""
        return _libsedml.SedListOfFitExperiments_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfFitExperiments

    def get(self, *args):
        """
        get(SedListOfFitExperiments self, unsigned int n) -> SedFitExperiment
        get(SedListOfFitExperiments self, unsigned int n) -> SedFitExperiment
        get(SedListOfFitExperiments self, string sid) -> SedFitExperiment
        get(SedListOfFitExperiments self, string sid) -> SedFitExperiment
        """
        return _libsedml.SedListOfFitExperiments_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfFitExperiments self, unsigned int n) -> SedFitExperiment
        remove(SedListOfFitExperiments self, string sid) -> SedFitExperiment
        """
        return _libsedml.SedListOfFitExperiments_remove(self, *args)

    def addFitExperiment(self, sfe):
        """addFitExperiment(SedListOfFitExperiments self, SedFitExperiment sfe) -> int"""
        return _libsedml.SedListOfFitExperiments_addFitExperiment(self, sfe)

    def getNumFitExperiments(self):
        """getNumFitExperiments(SedListOfFitExperiments self) -> unsigned int"""
        return _libsedml.SedListOfFitExperiments_getNumFitExperiments(self)

    def createFitExperiment(self):
        """createFitExperiment(SedListOfFitExperiments self) -> SedFitExperiment"""
        return _libsedml.SedListOfFitExperiments_createFitExperiment(self)

    def getElementName(self):
        """getElementName(SedListOfFitExperiments self) -> string"""
        return _libsedml.SedListOfFitExperiments_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfFitExperiments self) -> int"""
        return _libsedml.SedListOfFitExperiments_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfFitExperiments self) -> int"""
        return _libsedml.SedListOfFitExperiments_getItemTypeCode(self)


_libsedml.SedListOfFitExperiments_swigregister(SedListOfFitExperiments)

class SedFitMapping(SedBase):
    """Proxy of C++ SedFitMapping class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedFitMapping self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedFitMapping
        __init__(SedFitMapping self, SedNamespaces sedmlns) -> SedFitMapping
        __init__(SedFitMapping self, SedFitMapping orig) -> SedFitMapping
        """
        _libsedml.SedFitMapping_swiginit(self, _libsedml.new_SedFitMapping(*args))

    def clone(self):
        """clone(SedFitMapping self) -> SedFitMapping"""
        return _libsedml.SedFitMapping_clone(self)

    __swig_destroy__ = _libsedml.delete_SedFitMapping

    def getDataSource(self):
        """getDataSource(SedFitMapping self) -> string"""
        return _libsedml.SedFitMapping_getDataSource(self)

    def getTarget(self):
        """getTarget(SedFitMapping self) -> string"""
        return _libsedml.SedFitMapping_getTarget(self)

    def getType(self):
        """getType(SedFitMapping self) -> MappingType_t"""
        return _libsedml.SedFitMapping_getType(self)

    def getTypeAsString(self):
        """getTypeAsString(SedFitMapping self) -> string"""
        return _libsedml.SedFitMapping_getTypeAsString(self)

    def getWeight(self):
        """getWeight(SedFitMapping self) -> double"""
        return _libsedml.SedFitMapping_getWeight(self)

    def getPointWeight(self):
        """getPointWeight(SedFitMapping self) -> string"""
        return _libsedml.SedFitMapping_getPointWeight(self)

    def isSetDataSource(self):
        """isSetDataSource(SedFitMapping self) -> bool"""
        return _libsedml.SedFitMapping_isSetDataSource(self)

    def isSetTarget(self):
        """isSetTarget(SedFitMapping self) -> bool"""
        return _libsedml.SedFitMapping_isSetTarget(self)

    def isSetType(self):
        """isSetType(SedFitMapping self) -> bool"""
        return _libsedml.SedFitMapping_isSetType(self)

    def isSetWeight(self):
        """isSetWeight(SedFitMapping self) -> bool"""
        return _libsedml.SedFitMapping_isSetWeight(self)

    def isSetPointWeight(self):
        """isSetPointWeight(SedFitMapping self) -> bool"""
        return _libsedml.SedFitMapping_isSetPointWeight(self)

    def setDataSource(self, dataSource):
        """setDataSource(SedFitMapping self, string dataSource) -> int"""
        return _libsedml.SedFitMapping_setDataSource(self, dataSource)

    def setTarget(self, target):
        """setTarget(SedFitMapping self, string target) -> int"""
        return _libsedml.SedFitMapping_setTarget(self, target)

    def setType(self, *args):
        """
        setType(SedFitMapping self, MappingType_t const type) -> int
        setType(SedFitMapping self, string type) -> int
        """
        return _libsedml.SedFitMapping_setType(self, *args)

    def setWeight(self, weight):
        """setWeight(SedFitMapping self, double weight) -> int"""
        return _libsedml.SedFitMapping_setWeight(self, weight)

    def setPointWeight(self, pointWeight):
        """setPointWeight(SedFitMapping self, string pointWeight) -> int"""
        return _libsedml.SedFitMapping_setPointWeight(self, pointWeight)

    def unsetDataSource(self):
        """unsetDataSource(SedFitMapping self) -> int"""
        return _libsedml.SedFitMapping_unsetDataSource(self)

    def unsetTarget(self):
        """unsetTarget(SedFitMapping self) -> int"""
        return _libsedml.SedFitMapping_unsetTarget(self)

    def unsetType(self):
        """unsetType(SedFitMapping self) -> int"""
        return _libsedml.SedFitMapping_unsetType(self)

    def unsetWeight(self):
        """unsetWeight(SedFitMapping self) -> int"""
        return _libsedml.SedFitMapping_unsetWeight(self)

    def unsetPointWeight(self):
        """unsetPointWeight(SedFitMapping self) -> int"""
        return _libsedml.SedFitMapping_unsetPointWeight(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedFitMapping self, string oldid, string newid)"""
        return _libsedml.SedFitMapping_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedFitMapping self) -> string"""
        return _libsedml.SedFitMapping_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedFitMapping self) -> int"""
        return _libsedml.SedFitMapping_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedFitMapping self) -> bool"""
        return _libsedml.SedFitMapping_hasRequiredAttributes(self)


_libsedml.SedFitMapping_swigregister(SedFitMapping)

class SedListOfFitMappings(SedListOf):
    """Proxy of C++ SedListOfFitMappings class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfFitMappings self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfFitMappings
        __init__(SedListOfFitMappings self, SedNamespaces sedmlns) -> SedListOfFitMappings
        __init__(SedListOfFitMappings self, SedListOfFitMappings orig) -> SedListOfFitMappings
        """
        _libsedml.SedListOfFitMappings_swiginit(self, _libsedml.new_SedListOfFitMappings(*args))

    def clone(self):
        """clone(SedListOfFitMappings self) -> SedListOfFitMappings"""
        return _libsedml.SedListOfFitMappings_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfFitMappings

    def get(self, *args):
        """
        get(SedListOfFitMappings self, unsigned int n) -> SedFitMapping
        get(SedListOfFitMappings self, unsigned int n) -> SedFitMapping
        get(SedListOfFitMappings self, string sid) -> SedFitMapping
        get(SedListOfFitMappings self, string sid) -> SedFitMapping
        """
        return _libsedml.SedListOfFitMappings_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfFitMappings self, unsigned int n) -> SedFitMapping
        remove(SedListOfFitMappings self, string sid) -> SedFitMapping
        """
        return _libsedml.SedListOfFitMappings_remove(self, *args)

    def addFitMapping(self, sfm):
        """addFitMapping(SedListOfFitMappings self, SedFitMapping sfm) -> int"""
        return _libsedml.SedListOfFitMappings_addFitMapping(self, sfm)

    def getNumFitMappings(self):
        """getNumFitMappings(SedListOfFitMappings self) -> unsigned int"""
        return _libsedml.SedListOfFitMappings_getNumFitMappings(self)

    def createFitMapping(self):
        """createFitMapping(SedListOfFitMappings self) -> SedFitMapping"""
        return _libsedml.SedListOfFitMappings_createFitMapping(self)

    def getByDataSource(self, *args):
        """
        getByDataSource(SedListOfFitMappings self, string sid) -> SedFitMapping
        getByDataSource(SedListOfFitMappings self, string sid) -> SedFitMapping
        """
        return _libsedml.SedListOfFitMappings_getByDataSource(self, *args)

    def getByTarget(self, *args):
        """
        getByTarget(SedListOfFitMappings self, string sid) -> SedFitMapping
        getByTarget(SedListOfFitMappings self, string sid) -> SedFitMapping
        """
        return _libsedml.SedListOfFitMappings_getByTarget(self, *args)

    def getByPointWeight(self, *args):
        """
        getByPointWeight(SedListOfFitMappings self, string sid) -> SedFitMapping
        getByPointWeight(SedListOfFitMappings self, string sid) -> SedFitMapping
        """
        return _libsedml.SedListOfFitMappings_getByPointWeight(self, *args)

    def getElementName(self):
        """getElementName(SedListOfFitMappings self) -> string"""
        return _libsedml.SedListOfFitMappings_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfFitMappings self) -> int"""
        return _libsedml.SedListOfFitMappings_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfFitMappings self) -> int"""
        return _libsedml.SedListOfFitMappings_getItemTypeCode(self)


_libsedml.SedListOfFitMappings_swigregister(SedListOfFitMappings)

class SedBounds(SedBase):
    """Proxy of C++ SedBounds class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedBounds self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedBounds
        __init__(SedBounds self, SedNamespaces sedmlns) -> SedBounds
        __init__(SedBounds self, SedBounds orig) -> SedBounds
        """
        _libsedml.SedBounds_swiginit(self, _libsedml.new_SedBounds(*args))

    def clone(self):
        """clone(SedBounds self) -> SedBounds"""
        return _libsedml.SedBounds_clone(self)

    __swig_destroy__ = _libsedml.delete_SedBounds

    def getLowerBound(self):
        """getLowerBound(SedBounds self) -> double"""
        return _libsedml.SedBounds_getLowerBound(self)

    def getUpperBound(self):
        """getUpperBound(SedBounds self) -> double"""
        return _libsedml.SedBounds_getUpperBound(self)

    def getScale(self):
        """getScale(SedBounds self) -> ScaleType_t"""
        return _libsedml.SedBounds_getScale(self)

    def getScaleAsString(self):
        """getScaleAsString(SedBounds self) -> string"""
        return _libsedml.SedBounds_getScaleAsString(self)

    def isSetLowerBound(self):
        """isSetLowerBound(SedBounds self) -> bool"""
        return _libsedml.SedBounds_isSetLowerBound(self)

    def isSetUpperBound(self):
        """isSetUpperBound(SedBounds self) -> bool"""
        return _libsedml.SedBounds_isSetUpperBound(self)

    def isSetScale(self):
        """isSetScale(SedBounds self) -> bool"""
        return _libsedml.SedBounds_isSetScale(self)

    def setLowerBound(self, lowerBound):
        """setLowerBound(SedBounds self, double lowerBound) -> int"""
        return _libsedml.SedBounds_setLowerBound(self, lowerBound)

    def setUpperBound(self, upperBound):
        """setUpperBound(SedBounds self, double upperBound) -> int"""
        return _libsedml.SedBounds_setUpperBound(self, upperBound)

    def setScale(self, *args):
        """
        setScale(SedBounds self, ScaleType_t const scale) -> int
        setScale(SedBounds self, string scale) -> int
        """
        return _libsedml.SedBounds_setScale(self, *args)

    def unsetLowerBound(self):
        """unsetLowerBound(SedBounds self) -> int"""
        return _libsedml.SedBounds_unsetLowerBound(self)

    def unsetUpperBound(self):
        """unsetUpperBound(SedBounds self) -> int"""
        return _libsedml.SedBounds_unsetUpperBound(self)

    def unsetScale(self):
        """unsetScale(SedBounds self) -> int"""
        return _libsedml.SedBounds_unsetScale(self)

    def getElementName(self):
        """getElementName(SedBounds self) -> string"""
        return _libsedml.SedBounds_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedBounds self) -> int"""
        return _libsedml.SedBounds_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedBounds self) -> bool"""
        return _libsedml.SedBounds_hasRequiredAttributes(self)


_libsedml.SedBounds_swigregister(SedBounds)

class SedFigure(SedOutput):
    """Proxy of C++ SedFigure class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedFigure self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedFigure
        __init__(SedFigure self, SedNamespaces sedmlns) -> SedFigure
        __init__(SedFigure self, SedFigure orig) -> SedFigure
        """
        _libsedml.SedFigure_swiginit(self, _libsedml.new_SedFigure(*args))

    def clone(self):
        """clone(SedFigure self) -> SedFigure"""
        return _libsedml.SedFigure_clone(self)

    __swig_destroy__ = _libsedml.delete_SedFigure

    def getNumRows(self):
        """getNumRows(SedFigure self) -> int"""
        return _libsedml.SedFigure_getNumRows(self)

    def getNumCols(self):
        """getNumCols(SedFigure self) -> int"""
        return _libsedml.SedFigure_getNumCols(self)

    def isSetNumRows(self):
        """isSetNumRows(SedFigure self) -> bool"""
        return _libsedml.SedFigure_isSetNumRows(self)

    def isSetNumCols(self):
        """isSetNumCols(SedFigure self) -> bool"""
        return _libsedml.SedFigure_isSetNumCols(self)

    def setNumRows(self, numRows):
        """setNumRows(SedFigure self, int numRows) -> int"""
        return _libsedml.SedFigure_setNumRows(self, numRows)

    def setNumCols(self, numCols):
        """setNumCols(SedFigure self, int numCols) -> int"""
        return _libsedml.SedFigure_setNumCols(self, numCols)

    def unsetNumRows(self):
        """unsetNumRows(SedFigure self) -> int"""
        return _libsedml.SedFigure_unsetNumRows(self)

    def unsetNumCols(self):
        """unsetNumCols(SedFigure self) -> int"""
        return _libsedml.SedFigure_unsetNumCols(self)

    def getListOfSubPlots(self, *args):
        """
        getListOfSubPlots(SedFigure self) -> SedListOfSubPlots
        getListOfSubPlots(SedFigure self) -> SedListOfSubPlots
        """
        return _libsedml.SedFigure_getListOfSubPlots(self, *args)

    def getSubPlot(self, *args):
        """
        getSubPlot(SedFigure self, unsigned int n) -> SedSubPlot
        getSubPlot(SedFigure self, unsigned int n) -> SedSubPlot
        """
        return _libsedml.SedFigure_getSubPlot(self, *args)

    def getSubPlotByPlot(self, *args):
        """
        getSubPlotByPlot(SedFigure self, string sid) -> SedSubPlot
        getSubPlotByPlot(SedFigure self, string sid) -> SedSubPlot
        """
        return _libsedml.SedFigure_getSubPlotByPlot(self, *args)

    def addSubPlot(self, ssp):
        """addSubPlot(SedFigure self, SedSubPlot ssp) -> int"""
        return _libsedml.SedFigure_addSubPlot(self, ssp)

    def getNumSubPlots(self):
        """getNumSubPlots(SedFigure self) -> unsigned int"""
        return _libsedml.SedFigure_getNumSubPlots(self)

    def createSubPlot(self):
        """createSubPlot(SedFigure self) -> SedSubPlot"""
        return _libsedml.SedFigure_createSubPlot(self)

    def removeSubPlot(self, n):
        """removeSubPlot(SedFigure self, unsigned int n) -> SedSubPlot"""
        return _libsedml.SedFigure_removeSubPlot(self, n)

    def getElementName(self):
        """getElementName(SedFigure self) -> string"""
        return _libsedml.SedFigure_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedFigure self) -> int"""
        return _libsedml.SedFigure_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedFigure self) -> bool"""
        return _libsedml.SedFigure_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(SedFigure self) -> bool"""
        return _libsedml.SedFigure_hasRequiredElements(self)

    def connectToChild(self):
        """connectToChild(SedFigure self)"""
        return _libsedml.SedFigure_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedFigure self, string id) -> SedBase"""
        return _libsedml.SedFigure_getElementBySId(self, id)


_libsedml.SedFigure_swigregister(SedFigure)

class SedSubPlot(SedBase):
    """Proxy of C++ SedSubPlot class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedSubPlot self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedSubPlot
        __init__(SedSubPlot self, SedNamespaces sedmlns) -> SedSubPlot
        __init__(SedSubPlot self, SedSubPlot orig) -> SedSubPlot
        """
        _libsedml.SedSubPlot_swiginit(self, _libsedml.new_SedSubPlot(*args))

    def clone(self):
        """clone(SedSubPlot self) -> SedSubPlot"""
        return _libsedml.SedSubPlot_clone(self)

    __swig_destroy__ = _libsedml.delete_SedSubPlot

    def getPlot(self):
        """getPlot(SedSubPlot self) -> string"""
        return _libsedml.SedSubPlot_getPlot(self)

    def getRow(self):
        """getRow(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_getRow(self)

    def getCol(self):
        """getCol(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_getCol(self)

    def getRowSpan(self):
        """getRowSpan(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_getRowSpan(self)

    def getColSpan(self):
        """getColSpan(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_getColSpan(self)

    def isSetPlot(self):
        """isSetPlot(SedSubPlot self) -> bool"""
        return _libsedml.SedSubPlot_isSetPlot(self)

    def isSetRow(self):
        """isSetRow(SedSubPlot self) -> bool"""
        return _libsedml.SedSubPlot_isSetRow(self)

    def isSetCol(self):
        """isSetCol(SedSubPlot self) -> bool"""
        return _libsedml.SedSubPlot_isSetCol(self)

    def isSetRowSpan(self):
        """isSetRowSpan(SedSubPlot self) -> bool"""
        return _libsedml.SedSubPlot_isSetRowSpan(self)

    def isSetColSpan(self):
        """isSetColSpan(SedSubPlot self) -> bool"""
        return _libsedml.SedSubPlot_isSetColSpan(self)

    def setPlot(self, plot):
        """setPlot(SedSubPlot self, string plot) -> int"""
        return _libsedml.SedSubPlot_setPlot(self, plot)

    def setRow(self, row):
        """setRow(SedSubPlot self, int row) -> int"""
        return _libsedml.SedSubPlot_setRow(self, row)

    def setCol(self, col):
        """setCol(SedSubPlot self, int col) -> int"""
        return _libsedml.SedSubPlot_setCol(self, col)

    def setRowSpan(self, rowSpan):
        """setRowSpan(SedSubPlot self, int rowSpan) -> int"""
        return _libsedml.SedSubPlot_setRowSpan(self, rowSpan)

    def setColSpan(self, colSpan):
        """setColSpan(SedSubPlot self, int colSpan) -> int"""
        return _libsedml.SedSubPlot_setColSpan(self, colSpan)

    def unsetPlot(self):
        """unsetPlot(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_unsetPlot(self)

    def unsetRow(self):
        """unsetRow(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_unsetRow(self)

    def unsetCol(self):
        """unsetCol(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_unsetCol(self)

    def unsetRowSpan(self):
        """unsetRowSpan(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_unsetRowSpan(self)

    def unsetColSpan(self):
        """unsetColSpan(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_unsetColSpan(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedSubPlot self, string oldid, string newid)"""
        return _libsedml.SedSubPlot_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedSubPlot self) -> string"""
        return _libsedml.SedSubPlot_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedSubPlot self) -> int"""
        return _libsedml.SedSubPlot_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedSubPlot self) -> bool"""
        return _libsedml.SedSubPlot_hasRequiredAttributes(self)


_libsedml.SedSubPlot_swigregister(SedSubPlot)

class SedListOfSubPlots(SedListOf):
    """Proxy of C++ SedListOfSubPlots class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfSubPlots self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfSubPlots
        __init__(SedListOfSubPlots self, SedNamespaces sedmlns) -> SedListOfSubPlots
        __init__(SedListOfSubPlots self, SedListOfSubPlots orig) -> SedListOfSubPlots
        """
        _libsedml.SedListOfSubPlots_swiginit(self, _libsedml.new_SedListOfSubPlots(*args))

    def clone(self):
        """clone(SedListOfSubPlots self) -> SedListOfSubPlots"""
        return _libsedml.SedListOfSubPlots_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfSubPlots

    def get(self, *args):
        """
        get(SedListOfSubPlots self, unsigned int n) -> SedSubPlot
        get(SedListOfSubPlots self, unsigned int n) -> SedSubPlot
        get(SedListOfSubPlots self, string sid) -> SedSubPlot
        get(SedListOfSubPlots self, string sid) -> SedSubPlot
        """
        return _libsedml.SedListOfSubPlots_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfSubPlots self, unsigned int n) -> SedSubPlot
        remove(SedListOfSubPlots self, string sid) -> SedSubPlot
        """
        return _libsedml.SedListOfSubPlots_remove(self, *args)

    def addSubPlot(self, ssp):
        """addSubPlot(SedListOfSubPlots self, SedSubPlot ssp) -> int"""
        return _libsedml.SedListOfSubPlots_addSubPlot(self, ssp)

    def getNumSubPlots(self):
        """getNumSubPlots(SedListOfSubPlots self) -> unsigned int"""
        return _libsedml.SedListOfSubPlots_getNumSubPlots(self)

    def createSubPlot(self):
        """createSubPlot(SedListOfSubPlots self) -> SedSubPlot"""
        return _libsedml.SedListOfSubPlots_createSubPlot(self)

    def getByPlot(self, *args):
        """
        getByPlot(SedListOfSubPlots self, string sid) -> SedSubPlot
        getByPlot(SedListOfSubPlots self, string sid) -> SedSubPlot
        """
        return _libsedml.SedListOfSubPlots_getByPlot(self, *args)

    def getElementName(self):
        """getElementName(SedListOfSubPlots self) -> string"""
        return _libsedml.SedListOfSubPlots_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfSubPlots self) -> int"""
        return _libsedml.SedListOfSubPlots_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfSubPlots self) -> int"""
        return _libsedml.SedListOfSubPlots_getItemTypeCode(self)


_libsedml.SedListOfSubPlots_swigregister(SedListOfSubPlots)

class SedAxis(SedBase):
    """Proxy of C++ SedAxis class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedAxis self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedAxis
        __init__(SedAxis self, SedNamespaces sedmlns) -> SedAxis
        __init__(SedAxis self, SedAxis orig) -> SedAxis
        """
        _libsedml.SedAxis_swiginit(self, _libsedml.new_SedAxis(*args))

    def clone(self):
        """clone(SedAxis self) -> SedAxis"""
        return _libsedml.SedAxis_clone(self)

    __swig_destroy__ = _libsedml.delete_SedAxis

    def getType(self):
        """getType(SedAxis self) -> AxisType_t"""
        return _libsedml.SedAxis_getType(self)

    def getTypeAsString(self):
        """getTypeAsString(SedAxis self) -> string"""
        return _libsedml.SedAxis_getTypeAsString(self)

    def getMin(self):
        """getMin(SedAxis self) -> double"""
        return _libsedml.SedAxis_getMin(self)

    def getMax(self):
        """getMax(SedAxis self) -> double"""
        return _libsedml.SedAxis_getMax(self)

    def getGrid(self):
        """getGrid(SedAxis self) -> bool"""
        return _libsedml.SedAxis_getGrid(self)

    def getStyle(self):
        """getStyle(SedAxis self) -> string"""
        return _libsedml.SedAxis_getStyle(self)

    def isSetType(self):
        """isSetType(SedAxis self) -> bool"""
        return _libsedml.SedAxis_isSetType(self)

    def isSetMin(self):
        """isSetMin(SedAxis self) -> bool"""
        return _libsedml.SedAxis_isSetMin(self)

    def isSetMax(self):
        """isSetMax(SedAxis self) -> bool"""
        return _libsedml.SedAxis_isSetMax(self)

    def isSetGrid(self):
        """isSetGrid(SedAxis self) -> bool"""
        return _libsedml.SedAxis_isSetGrid(self)

    def isSetStyle(self):
        """isSetStyle(SedAxis self) -> bool"""
        return _libsedml.SedAxis_isSetStyle(self)

    def setType(self, *args):
        """
        setType(SedAxis self, AxisType_t const type) -> int
        setType(SedAxis self, string type) -> int
        """
        return _libsedml.SedAxis_setType(self, *args)

    def setMin(self, min):
        """setMin(SedAxis self, double min) -> int"""
        return _libsedml.SedAxis_setMin(self, min)

    def setMax(self, max):
        """setMax(SedAxis self, double max) -> int"""
        return _libsedml.SedAxis_setMax(self, max)

    def setGrid(self, grid):
        """setGrid(SedAxis self, bool grid) -> int"""
        return _libsedml.SedAxis_setGrid(self, grid)

    def setStyle(self, style):
        """setStyle(SedAxis self, string style) -> int"""
        return _libsedml.SedAxis_setStyle(self, style)

    def unsetType(self):
        """unsetType(SedAxis self) -> int"""
        return _libsedml.SedAxis_unsetType(self)

    def unsetMin(self):
        """unsetMin(SedAxis self) -> int"""
        return _libsedml.SedAxis_unsetMin(self)

    def unsetMax(self):
        """unsetMax(SedAxis self) -> int"""
        return _libsedml.SedAxis_unsetMax(self)

    def unsetGrid(self):
        """unsetGrid(SedAxis self) -> int"""
        return _libsedml.SedAxis_unsetGrid(self)

    def unsetStyle(self):
        """unsetStyle(SedAxis self) -> int"""
        return _libsedml.SedAxis_unsetStyle(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedAxis self, string oldid, string newid)"""
        return _libsedml.SedAxis_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedAxis self) -> string"""
        return _libsedml.SedAxis_getElementName(self)

    def setElementName(self, name):
        """setElementName(SedAxis self, string name)"""
        return _libsedml.SedAxis_setElementName(self, name)

    def getTypeCode(self):
        """getTypeCode(SedAxis self) -> int"""
        return _libsedml.SedAxis_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedAxis self) -> bool"""
        return _libsedml.SedAxis_hasRequiredAttributes(self)


_libsedml.SedAxis_swigregister(SedAxis)

class SedStyle(SedBase):
    """Proxy of C++ SedStyle class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedStyle self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedStyle
        __init__(SedStyle self, SedNamespaces sedmlns) -> SedStyle
        __init__(SedStyle self, SedStyle orig) -> SedStyle
        """
        _libsedml.SedStyle_swiginit(self, _libsedml.new_SedStyle(*args))

    def clone(self):
        """clone(SedStyle self) -> SedStyle"""
        return _libsedml.SedStyle_clone(self)

    __swig_destroy__ = _libsedml.delete_SedStyle

    def getId(self):
        """getId(SedStyle self) -> string"""
        return _libsedml.SedStyle_getId(self)

    def getBaseStyle(self):
        """getBaseStyle(SedStyle self) -> string"""
        return _libsedml.SedStyle_getBaseStyle(self)

    def isSetId(self):
        """isSetId(SedStyle self) -> bool"""
        return _libsedml.SedStyle_isSetId(self)

    def isSetBaseStyle(self):
        """isSetBaseStyle(SedStyle self) -> bool"""
        return _libsedml.SedStyle_isSetBaseStyle(self)

    def setId(self, id):
        """setId(SedStyle self, string id) -> int"""
        return _libsedml.SedStyle_setId(self, id)

    def setBaseStyle(self, baseStyle):
        """setBaseStyle(SedStyle self, string baseStyle) -> int"""
        return _libsedml.SedStyle_setBaseStyle(self, baseStyle)

    def unsetId(self):
        """unsetId(SedStyle self) -> int"""
        return _libsedml.SedStyle_unsetId(self)

    def unsetBaseStyle(self):
        """unsetBaseStyle(SedStyle self) -> int"""
        return _libsedml.SedStyle_unsetBaseStyle(self)

    def getLineStyle(self, *args):
        """
        getLineStyle(SedStyle self) -> SedLine
        getLineStyle(SedStyle self) -> SedLine
        """
        return _libsedml.SedStyle_getLineStyle(self, *args)

    def getMarkerStyle(self, *args):
        """
        getMarkerStyle(SedStyle self) -> SedMarker
        getMarkerStyle(SedStyle self) -> SedMarker
        """
        return _libsedml.SedStyle_getMarkerStyle(self, *args)

    def getFillStyle(self, *args):
        """
        getFillStyle(SedStyle self) -> SedFill
        getFillStyle(SedStyle self) -> SedFill
        """
        return _libsedml.SedStyle_getFillStyle(self, *args)

    def isSetLineStyle(self):
        """isSetLineStyle(SedStyle self) -> bool"""
        return _libsedml.SedStyle_isSetLineStyle(self)

    def isSetMarkerStyle(self):
        """isSetMarkerStyle(SedStyle self) -> bool"""
        return _libsedml.SedStyle_isSetMarkerStyle(self)

    def isSetFillStyle(self):
        """isSetFillStyle(SedStyle self) -> bool"""
        return _libsedml.SedStyle_isSetFillStyle(self)

    def setLineStyle(self, lineStyle):
        """setLineStyle(SedStyle self, SedLine lineStyle) -> int"""
        return _libsedml.SedStyle_setLineStyle(self, lineStyle)

    def setMarkerStyle(self, markerStyle):
        """setMarkerStyle(SedStyle self, SedMarker markerStyle) -> int"""
        return _libsedml.SedStyle_setMarkerStyle(self, markerStyle)

    def setFillStyle(self, fillStyle):
        """setFillStyle(SedStyle self, SedFill fillStyle) -> int"""
        return _libsedml.SedStyle_setFillStyle(self, fillStyle)

    def createLineStyle(self):
        """createLineStyle(SedStyle self) -> SedLine"""
        return _libsedml.SedStyle_createLineStyle(self)

    def createMarkerStyle(self):
        """createMarkerStyle(SedStyle self) -> SedMarker"""
        return _libsedml.SedStyle_createMarkerStyle(self)

    def createFillStyle(self):
        """createFillStyle(SedStyle self) -> SedFill"""
        return _libsedml.SedStyle_createFillStyle(self)

    def unsetLineStyle(self):
        """unsetLineStyle(SedStyle self) -> int"""
        return _libsedml.SedStyle_unsetLineStyle(self)

    def unsetMarkerStyle(self):
        """unsetMarkerStyle(SedStyle self) -> int"""
        return _libsedml.SedStyle_unsetMarkerStyle(self)

    def unsetFillStyle(self):
        """unsetFillStyle(SedStyle self) -> int"""
        return _libsedml.SedStyle_unsetFillStyle(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedStyle self, string oldid, string newid)"""
        return _libsedml.SedStyle_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedStyle self) -> string"""
        return _libsedml.SedStyle_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedStyle self) -> int"""
        return _libsedml.SedStyle_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedStyle self) -> bool"""
        return _libsedml.SedStyle_hasRequiredAttributes(self)

    def connectToChild(self):
        """connectToChild(SedStyle self)"""
        return _libsedml.SedStyle_connectToChild(self)

    def getElementBySId(self, id):
        """getElementBySId(SedStyle self, string id) -> SedBase"""
        return _libsedml.SedStyle_getElementBySId(self, id)


_libsedml.SedStyle_swigregister(SedStyle)

class SedLine(SedBase):
    """Proxy of C++ SedLine class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedLine self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedLine
        __init__(SedLine self, SedNamespaces sedmlns) -> SedLine
        __init__(SedLine self, SedLine orig) -> SedLine
        """
        _libsedml.SedLine_swiginit(self, _libsedml.new_SedLine(*args))

    def clone(self):
        """clone(SedLine self) -> SedLine"""
        return _libsedml.SedLine_clone(self)

    __swig_destroy__ = _libsedml.delete_SedLine

    def getStyle(self):
        """getStyle(SedLine self) -> LineType_t"""
        return _libsedml.SedLine_getStyle(self)

    def getStyleAsString(self):
        """getStyleAsString(SedLine self) -> string"""
        return _libsedml.SedLine_getStyleAsString(self)

    def getColor(self):
        """getColor(SedLine self) -> string"""
        return _libsedml.SedLine_getColor(self)

    def getThickness(self):
        """getThickness(SedLine self) -> double"""
        return _libsedml.SedLine_getThickness(self)

    def isSetStyle(self):
        """isSetStyle(SedLine self) -> bool"""
        return _libsedml.SedLine_isSetStyle(self)

    def isSetColor(self):
        """isSetColor(SedLine self) -> bool"""
        return _libsedml.SedLine_isSetColor(self)

    def isSetThickness(self):
        """isSetThickness(SedLine self) -> bool"""
        return _libsedml.SedLine_isSetThickness(self)

    def setStyle(self, *args):
        """
        setStyle(SedLine self, LineType_t const style) -> int
        setStyle(SedLine self, string style) -> int
        """
        return _libsedml.SedLine_setStyle(self, *args)

    def setColor(self, color):
        """setColor(SedLine self, string color) -> int"""
        return _libsedml.SedLine_setColor(self, color)

    def setThickness(self, thickness):
        """setThickness(SedLine self, double thickness) -> int"""
        return _libsedml.SedLine_setThickness(self, thickness)

    def unsetStyle(self):
        """unsetStyle(SedLine self) -> int"""
        return _libsedml.SedLine_unsetStyle(self)

    def unsetColor(self):
        """unsetColor(SedLine self) -> int"""
        return _libsedml.SedLine_unsetColor(self)

    def unsetThickness(self):
        """unsetThickness(SedLine self) -> int"""
        return _libsedml.SedLine_unsetThickness(self)

    def getElementName(self):
        """getElementName(SedLine self) -> string"""
        return _libsedml.SedLine_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedLine self) -> int"""
        return _libsedml.SedLine_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedLine self) -> bool"""
        return _libsedml.SedLine_hasRequiredAttributes(self)


_libsedml.SedLine_swigregister(SedLine)

class SedMarker(SedBase):
    """Proxy of C++ SedMarker class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedMarker self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedMarker
        __init__(SedMarker self, SedNamespaces sedmlns) -> SedMarker
        __init__(SedMarker self, SedMarker orig) -> SedMarker
        """
        _libsedml.SedMarker_swiginit(self, _libsedml.new_SedMarker(*args))

    def clone(self):
        """clone(SedMarker self) -> SedMarker"""
        return _libsedml.SedMarker_clone(self)

    __swig_destroy__ = _libsedml.delete_SedMarker

    def getSize(self):
        """getSize(SedMarker self) -> double"""
        return _libsedml.SedMarker_getSize(self)

    def getStyle(self):
        """getStyle(SedMarker self) -> MarkerType_t"""
        return _libsedml.SedMarker_getStyle(self)

    def getStyleAsString(self):
        """getStyleAsString(SedMarker self) -> string"""
        return _libsedml.SedMarker_getStyleAsString(self)

    def getFill(self):
        """getFill(SedMarker self) -> string"""
        return _libsedml.SedMarker_getFill(self)

    def getLineColor(self):
        """getLineColor(SedMarker self) -> string"""
        return _libsedml.SedMarker_getLineColor(self)

    def getLineThickness(self):
        """getLineThickness(SedMarker self) -> double"""
        return _libsedml.SedMarker_getLineThickness(self)

    def isSetSize(self):
        """isSetSize(SedMarker self) -> bool"""
        return _libsedml.SedMarker_isSetSize(self)

    def isSetStyle(self):
        """isSetStyle(SedMarker self) -> bool"""
        return _libsedml.SedMarker_isSetStyle(self)

    def isSetFill(self):
        """isSetFill(SedMarker self) -> bool"""
        return _libsedml.SedMarker_isSetFill(self)

    def isSetLineColor(self):
        """isSetLineColor(SedMarker self) -> bool"""
        return _libsedml.SedMarker_isSetLineColor(self)

    def isSetLineThickness(self):
        """isSetLineThickness(SedMarker self) -> bool"""
        return _libsedml.SedMarker_isSetLineThickness(self)

    def setSize(self, size):
        """setSize(SedMarker self, double size) -> int"""
        return _libsedml.SedMarker_setSize(self, size)

    def setStyle(self, *args):
        """
        setStyle(SedMarker self, MarkerType_t const style) -> int
        setStyle(SedMarker self, string style) -> int
        """
        return _libsedml.SedMarker_setStyle(self, *args)

    def setFill(self, fill):
        """setFill(SedMarker self, string fill) -> int"""
        return _libsedml.SedMarker_setFill(self, fill)

    def setLineColor(self, lineColor):
        """setLineColor(SedMarker self, string lineColor) -> int"""
        return _libsedml.SedMarker_setLineColor(self, lineColor)

    def setLineThickness(self, lineThickness):
        """setLineThickness(SedMarker self, double lineThickness) -> int"""
        return _libsedml.SedMarker_setLineThickness(self, lineThickness)

    def unsetSize(self):
        """unsetSize(SedMarker self) -> int"""
        return _libsedml.SedMarker_unsetSize(self)

    def unsetStyle(self):
        """unsetStyle(SedMarker self) -> int"""
        return _libsedml.SedMarker_unsetStyle(self)

    def unsetFill(self):
        """unsetFill(SedMarker self) -> int"""
        return _libsedml.SedMarker_unsetFill(self)

    def unsetLineColor(self):
        """unsetLineColor(SedMarker self) -> int"""
        return _libsedml.SedMarker_unsetLineColor(self)

    def unsetLineThickness(self):
        """unsetLineThickness(SedMarker self) -> int"""
        return _libsedml.SedMarker_unsetLineThickness(self)

    def getElementName(self):
        """getElementName(SedMarker self) -> string"""
        return _libsedml.SedMarker_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedMarker self) -> int"""
        return _libsedml.SedMarker_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedMarker self) -> bool"""
        return _libsedml.SedMarker_hasRequiredAttributes(self)


_libsedml.SedMarker_swigregister(SedMarker)

class SedFill(SedBase):
    """Proxy of C++ SedFill class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedFill self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedFill
        __init__(SedFill self, SedNamespaces sedmlns) -> SedFill
        __init__(SedFill self, SedFill orig) -> SedFill
        """
        _libsedml.SedFill_swiginit(self, _libsedml.new_SedFill(*args))

    def clone(self):
        """clone(SedFill self) -> SedFill"""
        return _libsedml.SedFill_clone(self)

    __swig_destroy__ = _libsedml.delete_SedFill

    def getColor(self):
        """getColor(SedFill self) -> string"""
        return _libsedml.SedFill_getColor(self)

    def getSecondColor(self):
        """getSecondColor(SedFill self) -> string"""
        return _libsedml.SedFill_getSecondColor(self)

    def isSetColor(self):
        """isSetColor(SedFill self) -> bool"""
        return _libsedml.SedFill_isSetColor(self)

    def isSetSecondColor(self):
        """isSetSecondColor(SedFill self) -> bool"""
        return _libsedml.SedFill_isSetSecondColor(self)

    def setColor(self, color):
        """setColor(SedFill self, string color) -> int"""
        return _libsedml.SedFill_setColor(self, color)

    def setSecondColor(self, secondColor):
        """setSecondColor(SedFill self, string secondColor) -> int"""
        return _libsedml.SedFill_setSecondColor(self, secondColor)

    def unsetColor(self):
        """unsetColor(SedFill self) -> int"""
        return _libsedml.SedFill_unsetColor(self)

    def unsetSecondColor(self):
        """unsetSecondColor(SedFill self) -> int"""
        return _libsedml.SedFill_unsetSecondColor(self)

    def getElementName(self):
        """getElementName(SedFill self) -> string"""
        return _libsedml.SedFill_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedFill self) -> int"""
        return _libsedml.SedFill_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedFill self) -> bool"""
        return _libsedml.SedFill_hasRequiredAttributes(self)


_libsedml.SedFill_swigregister(SedFill)

class SedDependentVariable(SedVariable):
    """Proxy of C++ SedDependentVariable class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedDependentVariable self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedDependentVariable
        __init__(SedDependentVariable self, SedNamespaces sedmlns) -> SedDependentVariable
        __init__(SedDependentVariable self, SedDependentVariable orig) -> SedDependentVariable
        """
        _libsedml.SedDependentVariable_swiginit(self, _libsedml.new_SedDependentVariable(*args))

    def clone(self):
        """clone(SedDependentVariable self) -> SedDependentVariable"""
        return _libsedml.SedDependentVariable_clone(self)

    __swig_destroy__ = _libsedml.delete_SedDependentVariable

    def getTerm(self):
        """getTerm(SedDependentVariable self) -> string"""
        return _libsedml.SedDependentVariable_getTerm(self)

    def getTarget2(self):
        """getTarget2(SedDependentVariable self) -> string"""
        return _libsedml.SedDependentVariable_getTarget2(self)

    def getSymbol2(self):
        """getSymbol2(SedDependentVariable self) -> string"""
        return _libsedml.SedDependentVariable_getSymbol2(self)

    def isSetTerm(self):
        """isSetTerm(SedDependentVariable self) -> bool"""
        return _libsedml.SedDependentVariable_isSetTerm(self)

    def isSetTarget2(self):
        """isSetTarget2(SedDependentVariable self) -> bool"""
        return _libsedml.SedDependentVariable_isSetTarget2(self)

    def isSetSymbol2(self):
        """isSetSymbol2(SedDependentVariable self) -> bool"""
        return _libsedml.SedDependentVariable_isSetSymbol2(self)

    def setTerm(self, term):
        """setTerm(SedDependentVariable self, string term) -> int"""
        return _libsedml.SedDependentVariable_setTerm(self, term)

    def setTarget2(self, target2):
        """setTarget2(SedDependentVariable self, string target2) -> int"""
        return _libsedml.SedDependentVariable_setTarget2(self, target2)

    def setSymbol2(self, symbol2):
        """setSymbol2(SedDependentVariable self, string symbol2) -> int"""
        return _libsedml.SedDependentVariable_setSymbol2(self, symbol2)

    def unsetTerm(self):
        """unsetTerm(SedDependentVariable self) -> int"""
        return _libsedml.SedDependentVariable_unsetTerm(self)

    def unsetTarget2(self):
        """unsetTarget2(SedDependentVariable self) -> int"""
        return _libsedml.SedDependentVariable_unsetTarget2(self)

    def unsetSymbol2(self):
        """unsetSymbol2(SedDependentVariable self) -> int"""
        return _libsedml.SedDependentVariable_unsetSymbol2(self)

    def getElementName(self):
        """getElementName(SedDependentVariable self) -> string"""
        return _libsedml.SedDependentVariable_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedDependentVariable self) -> int"""
        return _libsedml.SedDependentVariable_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedDependentVariable self) -> bool"""
        return _libsedml.SedDependentVariable_hasRequiredAttributes(self)


_libsedml.SedDependentVariable_swigregister(SedDependentVariable)

class SedRemainingDimension(SedBase):
    """Proxy of C++ SedRemainingDimension class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedRemainingDimension self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedRemainingDimension
        __init__(SedRemainingDimension self, SedNamespaces sedmlns) -> SedRemainingDimension
        __init__(SedRemainingDimension self, SedRemainingDimension orig) -> SedRemainingDimension
        """
        _libsedml.SedRemainingDimension_swiginit(self, _libsedml.new_SedRemainingDimension(*args))

    def clone(self):
        """clone(SedRemainingDimension self) -> SedRemainingDimension"""
        return _libsedml.SedRemainingDimension_clone(self)

    __swig_destroy__ = _libsedml.delete_SedRemainingDimension

    def getTarget(self):
        """getTarget(SedRemainingDimension self) -> string"""
        return _libsedml.SedRemainingDimension_getTarget(self)

    def getDimensionTarget(self):
        """getDimensionTarget(SedRemainingDimension self) -> string"""
        return _libsedml.SedRemainingDimension_getDimensionTarget(self)

    def isSetTarget(self):
        """isSetTarget(SedRemainingDimension self) -> bool"""
        return _libsedml.SedRemainingDimension_isSetTarget(self)

    def isSetDimensionTarget(self):
        """isSetDimensionTarget(SedRemainingDimension self) -> bool"""
        return _libsedml.SedRemainingDimension_isSetDimensionTarget(self)

    def setTarget(self, target):
        """setTarget(SedRemainingDimension self, string target) -> int"""
        return _libsedml.SedRemainingDimension_setTarget(self, target)

    def setDimensionTarget(self, dimensionTarget):
        """setDimensionTarget(SedRemainingDimension self, string dimensionTarget) -> int"""
        return _libsedml.SedRemainingDimension_setDimensionTarget(self, dimensionTarget)

    def unsetTarget(self):
        """unsetTarget(SedRemainingDimension self) -> int"""
        return _libsedml.SedRemainingDimension_unsetTarget(self)

    def unsetDimensionTarget(self):
        """unsetDimensionTarget(SedRemainingDimension self) -> int"""
        return _libsedml.SedRemainingDimension_unsetDimensionTarget(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedRemainingDimension self, string oldid, string newid)"""
        return _libsedml.SedRemainingDimension_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedRemainingDimension self) -> string"""
        return _libsedml.SedRemainingDimension_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedRemainingDimension self) -> int"""
        return _libsedml.SedRemainingDimension_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedRemainingDimension self) -> bool"""
        return _libsedml.SedRemainingDimension_hasRequiredAttributes(self)


_libsedml.SedRemainingDimension_swigregister(SedRemainingDimension)

class SedListOfRemainingDimensions(SedListOf):
    """Proxy of C++ SedListOfRemainingDimensions class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedListOfRemainingDimensions self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedListOfRemainingDimensions
        __init__(SedListOfRemainingDimensions self, SedNamespaces sedmlns) -> SedListOfRemainingDimensions
        __init__(SedListOfRemainingDimensions self, SedListOfRemainingDimensions orig) -> SedListOfRemainingDimensions
        """
        _libsedml.SedListOfRemainingDimensions_swiginit(self, _libsedml.new_SedListOfRemainingDimensions(*args))

    def clone(self):
        """clone(SedListOfRemainingDimensions self) -> SedListOfRemainingDimensions"""
        return _libsedml.SedListOfRemainingDimensions_clone(self)

    __swig_destroy__ = _libsedml.delete_SedListOfRemainingDimensions

    def get(self, *args):
        """
        get(SedListOfRemainingDimensions self, unsigned int n) -> SedRemainingDimension
        get(SedListOfRemainingDimensions self, unsigned int n) -> SedRemainingDimension
        get(SedListOfRemainingDimensions self, string sid) -> SedRemainingDimension
        get(SedListOfRemainingDimensions self, string sid) -> SedRemainingDimension
        """
        return _libsedml.SedListOfRemainingDimensions_get(self, *args)

    def remove(self, *args):
        """
        remove(SedListOfRemainingDimensions self, unsigned int n) -> SedRemainingDimension
        remove(SedListOfRemainingDimensions self, string sid) -> SedRemainingDimension
        """
        return _libsedml.SedListOfRemainingDimensions_remove(self, *args)

    def addRemainingDimension(self, srd):
        """addRemainingDimension(SedListOfRemainingDimensions self, SedRemainingDimension srd) -> int"""
        return _libsedml.SedListOfRemainingDimensions_addRemainingDimension(self, srd)

    def getNumRemainingDimensions(self):
        """getNumRemainingDimensions(SedListOfRemainingDimensions self) -> unsigned int"""
        return _libsedml.SedListOfRemainingDimensions_getNumRemainingDimensions(self)

    def createRemainingDimension(self):
        """createRemainingDimension(SedListOfRemainingDimensions self) -> SedRemainingDimension"""
        return _libsedml.SedListOfRemainingDimensions_createRemainingDimension(self)

    def getByTarget(self, *args):
        """
        getByTarget(SedListOfRemainingDimensions self, string sid) -> SedRemainingDimension
        getByTarget(SedListOfRemainingDimensions self, string sid) -> SedRemainingDimension
        """
        return _libsedml.SedListOfRemainingDimensions_getByTarget(self, *args)

    def getByDimensionTarget(self, *args):
        """
        getByDimensionTarget(SedListOfRemainingDimensions self, string sid) -> SedRemainingDimension
        getByDimensionTarget(SedListOfRemainingDimensions self, string sid) -> SedRemainingDimension
        """
        return _libsedml.SedListOfRemainingDimensions_getByDimensionTarget(self, *args)

    def getElementName(self):
        """getElementName(SedListOfRemainingDimensions self) -> string"""
        return _libsedml.SedListOfRemainingDimensions_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedListOfRemainingDimensions self) -> int"""
        return _libsedml.SedListOfRemainingDimensions_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(SedListOfRemainingDimensions self) -> int"""
        return _libsedml.SedListOfRemainingDimensions_getItemTypeCode(self)


_libsedml.SedListOfRemainingDimensions_swigregister(SedListOfRemainingDimensions)

class SedDataRange(SedRange):
    """Proxy of C++ SedDataRange class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedDataRange self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedDataRange
        __init__(SedDataRange self, SedNamespaces sedmlns) -> SedDataRange
        __init__(SedDataRange self, SedDataRange orig) -> SedDataRange
        """
        _libsedml.SedDataRange_swiginit(self, _libsedml.new_SedDataRange(*args))

    def clone(self):
        """clone(SedDataRange self) -> SedDataRange"""
        return _libsedml.SedDataRange_clone(self)

    __swig_destroy__ = _libsedml.delete_SedDataRange

    def getSourceRef(self):
        """getSourceRef(SedDataRange self) -> string"""
        return _libsedml.SedDataRange_getSourceRef(self)

    def isSetSourceRef(self):
        """isSetSourceRef(SedDataRange self) -> bool"""
        return _libsedml.SedDataRange_isSetSourceRef(self)

    def setSourceRef(self, sourceRef):
        """setSourceRef(SedDataRange self, string sourceRef) -> int"""
        return _libsedml.SedDataRange_setSourceRef(self, sourceRef)

    def unsetSourceRef(self):
        """unsetSourceRef(SedDataRange self) -> int"""
        return _libsedml.SedDataRange_unsetSourceRef(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedDataRange self, string oldid, string newid)"""
        return _libsedml.SedDataRange_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedDataRange self) -> string"""
        return _libsedml.SedDataRange_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedDataRange self) -> int"""
        return _libsedml.SedDataRange_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedDataRange self) -> bool"""
        return _libsedml.SedDataRange_hasRequiredAttributes(self)


_libsedml.SedDataRange_swigregister(SedDataRange)

class SedSimpleRepeatedTask(SedTask):
    """Proxy of C++ SedSimpleRepeatedTask class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedSimpleRepeatedTask self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedSimpleRepeatedTask
        __init__(SedSimpleRepeatedTask self, SedNamespaces sedmlns) -> SedSimpleRepeatedTask
        __init__(SedSimpleRepeatedTask self, SedSimpleRepeatedTask orig) -> SedSimpleRepeatedTask
        """
        _libsedml.SedSimpleRepeatedTask_swiginit(self, _libsedml.new_SedSimpleRepeatedTask(*args))

    def clone(self):
        """clone(SedSimpleRepeatedTask self) -> SedSimpleRepeatedTask"""
        return _libsedml.SedSimpleRepeatedTask_clone(self)

    __swig_destroy__ = _libsedml.delete_SedSimpleRepeatedTask

    def getResetModel(self):
        """getResetModel(SedSimpleRepeatedTask self) -> bool"""
        return _libsedml.SedSimpleRepeatedTask_getResetModel(self)

    def getNumRepeats(self):
        """getNumRepeats(SedSimpleRepeatedTask self) -> int"""
        return _libsedml.SedSimpleRepeatedTask_getNumRepeats(self)

    def isSetResetModel(self):
        """isSetResetModel(SedSimpleRepeatedTask self) -> bool"""
        return _libsedml.SedSimpleRepeatedTask_isSetResetModel(self)

    def isSetNumRepeats(self):
        """isSetNumRepeats(SedSimpleRepeatedTask self) -> bool"""
        return _libsedml.SedSimpleRepeatedTask_isSetNumRepeats(self)

    def setResetModel(self, resetModel):
        """setResetModel(SedSimpleRepeatedTask self, bool resetModel) -> int"""
        return _libsedml.SedSimpleRepeatedTask_setResetModel(self, resetModel)

    def setNumRepeats(self, numRepeats):
        """setNumRepeats(SedSimpleRepeatedTask self, int numRepeats) -> int"""
        return _libsedml.SedSimpleRepeatedTask_setNumRepeats(self, numRepeats)

    def unsetResetModel(self):
        """unsetResetModel(SedSimpleRepeatedTask self) -> int"""
        return _libsedml.SedSimpleRepeatedTask_unsetResetModel(self)

    def unsetNumRepeats(self):
        """unsetNumRepeats(SedSimpleRepeatedTask self) -> int"""
        return _libsedml.SedSimpleRepeatedTask_unsetNumRepeats(self)

    def getElementName(self):
        """getElementName(SedSimpleRepeatedTask self) -> string"""
        return _libsedml.SedSimpleRepeatedTask_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedSimpleRepeatedTask self) -> int"""
        return _libsedml.SedSimpleRepeatedTask_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedSimpleRepeatedTask self) -> bool"""
        return _libsedml.SedSimpleRepeatedTask_hasRequiredAttributes(self)


_libsedml.SedSimpleRepeatedTask_swigregister(SedSimpleRepeatedTask)

class SedShadedArea(SedAbstractCurve):
    """Proxy of C++ SedShadedArea class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedShadedArea self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedShadedArea
        __init__(SedShadedArea self, SedNamespaces sedmlns) -> SedShadedArea
        __init__(SedShadedArea self, SedShadedArea orig) -> SedShadedArea
        """
        _libsedml.SedShadedArea_swiginit(self, _libsedml.new_SedShadedArea(*args))

    def clone(self):
        """clone(SedShadedArea self) -> SedShadedArea"""
        return _libsedml.SedShadedArea_clone(self)

    __swig_destroy__ = _libsedml.delete_SedShadedArea

    def getYDataReferenceFrom(self):
        """getYDataReferenceFrom(SedShadedArea self) -> string"""
        return _libsedml.SedShadedArea_getYDataReferenceFrom(self)

    def getYDataReferenceTo(self):
        """getYDataReferenceTo(SedShadedArea self) -> string"""
        return _libsedml.SedShadedArea_getYDataReferenceTo(self)

    def isSetYDataReferenceFrom(self):
        """isSetYDataReferenceFrom(SedShadedArea self) -> bool"""
        return _libsedml.SedShadedArea_isSetYDataReferenceFrom(self)

    def isSetYDataReferenceTo(self):
        """isSetYDataReferenceTo(SedShadedArea self) -> bool"""
        return _libsedml.SedShadedArea_isSetYDataReferenceTo(self)

    def setYDataReferenceFrom(self, yDataReferenceFrom):
        """setYDataReferenceFrom(SedShadedArea self, string yDataReferenceFrom) -> int"""
        return _libsedml.SedShadedArea_setYDataReferenceFrom(self, yDataReferenceFrom)

    def setYDataReferenceTo(self, yDataReferenceTo):
        """setYDataReferenceTo(SedShadedArea self, string yDataReferenceTo) -> int"""
        return _libsedml.SedShadedArea_setYDataReferenceTo(self, yDataReferenceTo)

    def unsetYDataReferenceFrom(self):
        """unsetYDataReferenceFrom(SedShadedArea self) -> int"""
        return _libsedml.SedShadedArea_unsetYDataReferenceFrom(self)

    def unsetYDataReferenceTo(self):
        """unsetYDataReferenceTo(SedShadedArea self) -> int"""
        return _libsedml.SedShadedArea_unsetYDataReferenceTo(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedShadedArea self, string oldid, string newid)"""
        return _libsedml.SedShadedArea_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedShadedArea self) -> string"""
        return _libsedml.SedShadedArea_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedShadedArea self) -> int"""
        return _libsedml.SedShadedArea_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedShadedArea self) -> bool"""
        return _libsedml.SedShadedArea_hasRequiredAttributes(self)


_libsedml.SedShadedArea_swigregister(SedShadedArea)

class SedParameterEstimationResultPlot(SedPlot):
    """Proxy of C++ SedParameterEstimationResultPlot class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedParameterEstimationResultPlot self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedParameterEstimationResultPlot
        __init__(SedParameterEstimationResultPlot self, SedNamespaces sedmlns) -> SedParameterEstimationResultPlot
        __init__(SedParameterEstimationResultPlot self, SedParameterEstimationResultPlot orig) -> SedParameterEstimationResultPlot
        """
        _libsedml.SedParameterEstimationResultPlot_swiginit(self, _libsedml.new_SedParameterEstimationResultPlot(*args))

    def clone(self):
        """clone(SedParameterEstimationResultPlot self) -> SedParameterEstimationResultPlot"""
        return _libsedml.SedParameterEstimationResultPlot_clone(self)

    __swig_destroy__ = _libsedml.delete_SedParameterEstimationResultPlot

    def getTaskRef(self):
        """getTaskRef(SedParameterEstimationResultPlot self) -> string"""
        return _libsedml.SedParameterEstimationResultPlot_getTaskRef(self)

    def isSetTaskRef(self):
        """isSetTaskRef(SedParameterEstimationResultPlot self) -> bool"""
        return _libsedml.SedParameterEstimationResultPlot_isSetTaskRef(self)

    def setTaskRef(self, taskRef):
        """setTaskRef(SedParameterEstimationResultPlot self, string taskRef) -> int"""
        return _libsedml.SedParameterEstimationResultPlot_setTaskRef(self, taskRef)

    def unsetTaskRef(self):
        """unsetTaskRef(SedParameterEstimationResultPlot self) -> int"""
        return _libsedml.SedParameterEstimationResultPlot_unsetTaskRef(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedParameterEstimationResultPlot self, string oldid, string newid)"""
        return _libsedml.SedParameterEstimationResultPlot_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedParameterEstimationResultPlot self) -> string"""
        return _libsedml.SedParameterEstimationResultPlot_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedParameterEstimationResultPlot self) -> int"""
        return _libsedml.SedParameterEstimationResultPlot_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedParameterEstimationResultPlot self) -> bool"""
        return _libsedml.SedParameterEstimationResultPlot_hasRequiredAttributes(self)


_libsedml.SedParameterEstimationResultPlot_swigregister(SedParameterEstimationResultPlot)

class SedWaterfallPlot(SedPlot):
    """Proxy of C++ SedWaterfallPlot class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedWaterfallPlot self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedWaterfallPlot
        __init__(SedWaterfallPlot self, SedNamespaces sedmlns) -> SedWaterfallPlot
        __init__(SedWaterfallPlot self, SedWaterfallPlot orig) -> SedWaterfallPlot
        """
        _libsedml.SedWaterfallPlot_swiginit(self, _libsedml.new_SedWaterfallPlot(*args))

    def clone(self):
        """clone(SedWaterfallPlot self) -> SedWaterfallPlot"""
        return _libsedml.SedWaterfallPlot_clone(self)

    __swig_destroy__ = _libsedml.delete_SedWaterfallPlot

    def getTaskRef(self):
        """getTaskRef(SedWaterfallPlot self) -> string"""
        return _libsedml.SedWaterfallPlot_getTaskRef(self)

    def isSetTaskRef(self):
        """isSetTaskRef(SedWaterfallPlot self) -> bool"""
        return _libsedml.SedWaterfallPlot_isSetTaskRef(self)

    def setTaskRef(self, taskRef):
        """setTaskRef(SedWaterfallPlot self, string taskRef) -> int"""
        return _libsedml.SedWaterfallPlot_setTaskRef(self, taskRef)

    def unsetTaskRef(self):
        """unsetTaskRef(SedWaterfallPlot self) -> int"""
        return _libsedml.SedWaterfallPlot_unsetTaskRef(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedWaterfallPlot self, string oldid, string newid)"""
        return _libsedml.SedWaterfallPlot_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedWaterfallPlot self) -> string"""
        return _libsedml.SedWaterfallPlot_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedWaterfallPlot self) -> int"""
        return _libsedml.SedWaterfallPlot_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedWaterfallPlot self) -> bool"""
        return _libsedml.SedWaterfallPlot_hasRequiredAttributes(self)


_libsedml.SedWaterfallPlot_swigregister(SedWaterfallPlot)

class SedParameterEstimationReport(SedOutput):
    """Proxy of C++ SedParameterEstimationReport class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(SedParameterEstimationReport self, unsigned int level=SEDML_DEFAULT_LEVEL, unsigned int version=SEDML_DEFAULT_VERSION) -> SedParameterEstimationReport
        __init__(SedParameterEstimationReport self, SedNamespaces sedmlns) -> SedParameterEstimationReport
        __init__(SedParameterEstimationReport self, SedParameterEstimationReport orig) -> SedParameterEstimationReport
        """
        _libsedml.SedParameterEstimationReport_swiginit(self, _libsedml.new_SedParameterEstimationReport(*args))

    def clone(self):
        """clone(SedParameterEstimationReport self) -> SedParameterEstimationReport"""
        return _libsedml.SedParameterEstimationReport_clone(self)

    __swig_destroy__ = _libsedml.delete_SedParameterEstimationReport

    def getTaskRef(self):
        """getTaskRef(SedParameterEstimationReport self) -> string"""
        return _libsedml.SedParameterEstimationReport_getTaskRef(self)

    def isSetTaskRef(self):
        """isSetTaskRef(SedParameterEstimationReport self) -> bool"""
        return _libsedml.SedParameterEstimationReport_isSetTaskRef(self)

    def setTaskRef(self, taskRef):
        """setTaskRef(SedParameterEstimationReport self, string taskRef) -> int"""
        return _libsedml.SedParameterEstimationReport_setTaskRef(self, taskRef)

    def unsetTaskRef(self):
        """unsetTaskRef(SedParameterEstimationReport self) -> int"""
        return _libsedml.SedParameterEstimationReport_unsetTaskRef(self)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(SedParameterEstimationReport self, string oldid, string newid)"""
        return _libsedml.SedParameterEstimationReport_renameSIdRefs(self, oldid, newid)

    def getElementName(self):
        """getElementName(SedParameterEstimationReport self) -> string"""
        return _libsedml.SedParameterEstimationReport_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(SedParameterEstimationReport self) -> int"""
        return _libsedml.SedParameterEstimationReport_getTypeCode(self)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(SedParameterEstimationReport self) -> bool"""
        return _libsedml.SedParameterEstimationReport_hasRequiredAttributes(self)


_libsedml.SedParameterEstimationReport_swigregister(SedParameterEstimationReport)

class SyntaxChecker(object):
    """Proxy of C++ SyntaxChecker class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    @staticmethod
    def isValidSBMLSId(sid):
        """isValidSBMLSId(string sid) -> bool"""
        return _libsedml.SyntaxChecker_isValidSBMLSId(sid)

    @staticmethod
    def isValidXMLID(id):
        """isValidXMLID(string id) -> bool"""
        return _libsedml.SyntaxChecker_isValidXMLID(id)

    @staticmethod
    def isValidXMLanyURI(uri):
        """isValidXMLanyURI(string uri) -> bool"""
        return _libsedml.SyntaxChecker_isValidXMLanyURI(uri)

    @staticmethod
    def isValidUnitSId(units):
        """isValidUnitSId(string units) -> bool"""
        return _libsedml.SyntaxChecker_isValidUnitSId(units)

    @staticmethod
    def hasExpectedXHTMLSyntax(xhtml, sbmlns=None):
        """hasExpectedXHTMLSyntax(XMLNode xhtml, SBMLNamespaces * sbmlns=None) -> bool"""
        return _libsedml.SyntaxChecker_hasExpectedXHTMLSyntax(xhtml, sbmlns)

    @staticmethod
    def isValidInternalSId(sid):
        """isValidInternalSId(string sid) -> bool"""
        return _libsedml.SyntaxChecker_isValidInternalSId(sid)

    @staticmethod
    def isValidInternalUnitSId(sid):
        """isValidInternalUnitSId(string sid) -> bool"""
        return _libsedml.SyntaxChecker_isValidInternalUnitSId(sid)

    def __init__(self):
        """__init__(SyntaxChecker self) -> SyntaxChecker"""
        _libsedml.SyntaxChecker_swiginit(self, _libsedml.new_SyntaxChecker())

    __swig_destroy__ = _libsedml.delete_SyntaxChecker


_libsedml.SyntaxChecker_swigregister(SyntaxChecker)

def SyntaxChecker_isValidSBMLSId(sid):
    """SyntaxChecker_isValidSBMLSId(string sid) -> bool"""
    return _libsedml.SyntaxChecker_isValidSBMLSId(sid)


def SyntaxChecker_isValidXMLID(id):
    """SyntaxChecker_isValidXMLID(string id) -> bool"""
    return _libsedml.SyntaxChecker_isValidXMLID(id)


def SyntaxChecker_isValidXMLanyURI(uri):
    """SyntaxChecker_isValidXMLanyURI(string uri) -> bool"""
    return _libsedml.SyntaxChecker_isValidXMLanyURI(uri)


def SyntaxChecker_isValidUnitSId(units):
    """SyntaxChecker_isValidUnitSId(string units) -> bool"""
    return _libsedml.SyntaxChecker_isValidUnitSId(units)


def SyntaxChecker_hasExpectedXHTMLSyntax(xhtml, sbmlns=None):
    """SyntaxChecker_hasExpectedXHTMLSyntax(XMLNode xhtml, SBMLNamespaces * sbmlns=None) -> bool"""
    return _libsedml.SyntaxChecker_hasExpectedXHTMLSyntax(xhtml, sbmlns)


def SyntaxChecker_isValidInternalSId(sid):
    """SyntaxChecker_isValidInternalSId(string sid) -> bool"""
    return _libsedml.SyntaxChecker_isValidInternalSId(sid)


def SyntaxChecker_isValidInternalUnitSId(sid):
    """SyntaxChecker_isValidInternalUnitSId(string sid) -> bool"""
    return _libsedml.SyntaxChecker_isValidInternalUnitSId(sid)


class XMLAttributes(object):
    """Proxy of C++ XMLAttributes class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_XMLAttributes

    def __init__(self, *args):
        """
        __init__(XMLAttributes self) -> XMLAttributes
        __init__(XMLAttributes self, XMLAttributes orig) -> XMLAttributes
        """
        _libsedml.XMLAttributes_swiginit(self, _libsedml.new_XMLAttributes(*args))

    def clone(self):
        """clone(XMLAttributes self) -> XMLAttributes"""
        return _libsedml.XMLAttributes_clone(self)

    def add(self, *args):
        """
        add(XMLAttributes self, string name, string value, string namespaceURI="", string prefix="") -> int
        add(XMLAttributes self, XMLTriple triple, string value) -> int
        """
        return _libsedml.XMLAttributes_add(self, *args)

    def addResource(self, name, value):
        """addResource(XMLAttributes self, string name, string value) -> int"""
        return _libsedml.XMLAttributes_addResource(self, name, value)

    def removeResource(self, n):
        """removeResource(XMLAttributes self, int n) -> int"""
        return _libsedml.XMLAttributes_removeResource(self, n)

    def remove(self, *args):
        """
        remove(XMLAttributes self, int n) -> int
        remove(XMLAttributes self, string name, string uri="") -> int
        remove(XMLAttributes self, XMLTriple triple) -> int
        """
        return _libsedml.XMLAttributes_remove(self, *args)

    def clear(self):
        """clear(XMLAttributes self) -> int"""
        return _libsedml.XMLAttributes_clear(self)

    def getIndex(self, *args):
        """
        getIndex(XMLAttributes self, string name) -> int
        getIndex(XMLAttributes self, string name, string uri) -> int
        getIndex(XMLAttributes self, XMLTriple triple) -> int
        """
        return _libsedml.XMLAttributes_getIndex(self, *args)

    def getLength(self):
        """getLength(XMLAttributes self) -> int"""
        return _libsedml.XMLAttributes_getLength(self)

    def getNumAttributes(self):
        """getNumAttributes(XMLAttributes self) -> int"""
        return _libsedml.XMLAttributes_getNumAttributes(self)

    def getName(self, index):
        """getName(XMLAttributes self, int index) -> string"""
        return _libsedml.XMLAttributes_getName(self, index)

    def getPrefix(self, index):
        """getPrefix(XMLAttributes self, int index) -> string"""
        return _libsedml.XMLAttributes_getPrefix(self, index)

    def getPrefixedName(self, index):
        """getPrefixedName(XMLAttributes self, int index) -> string"""
        return _libsedml.XMLAttributes_getPrefixedName(self, index)

    def getURI(self, index):
        """getURI(XMLAttributes self, int index) -> string"""
        return _libsedml.XMLAttributes_getURI(self, index)

    def getValue(self, *args):
        """
        getValue(XMLAttributes self, int index) -> string
        getValue(XMLAttributes self, string name) -> string
        getValue(XMLAttributes self, string name, string uri) -> string
        getValue(XMLAttributes self, XMLTriple triple) -> string
        """
        return _libsedml.XMLAttributes_getValue(self, *args)

    def hasAttribute(self, *args):
        """
        hasAttribute(XMLAttributes self, int index) -> bool
        hasAttribute(XMLAttributes self, string name, string uri="") -> bool
        hasAttribute(XMLAttributes self, XMLTriple triple) -> bool
        """
        return _libsedml.XMLAttributes_hasAttribute(self, *args)

    def isEmpty(self):
        """isEmpty(XMLAttributes self) -> bool"""
        return _libsedml.XMLAttributes_isEmpty(self)

    def write(self, stream):
        """write(XMLAttributes self, XMLOutputStream stream)"""
        return _libsedml.XMLAttributes_write(self, stream)

    def setErrorLog(self, log):
        """setErrorLog(XMLAttributes self, XMLErrorLog log) -> int"""
        return _libsedml.XMLAttributes_setErrorLog(self, log)

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True


_libsedml.XMLAttributes_swigregister(XMLAttributes)

class XMLNamespaces(object):
    """Proxy of C++ XMLNamespaces class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_XMLNamespaces

    def __init__(self, *args):
        """
        __init__(XMLNamespaces self) -> XMLNamespaces
        __init__(XMLNamespaces self, XMLNamespaces orig) -> XMLNamespaces
        """
        _libsedml.XMLNamespaces_swiginit(self, _libsedml.new_XMLNamespaces(*args))

    def clone(self):
        """clone(XMLNamespaces self) -> XMLNamespaces"""
        return _libsedml.XMLNamespaces_clone(self)

    def add(self, *args):
        """add(XMLNamespaces self, string uri, string prefix="") -> int"""
        return _libsedml.XMLNamespaces_add(self, *args)

    def remove(self, *args):
        """
        remove(XMLNamespaces self, int index) -> int
        remove(XMLNamespaces self, string prefix) -> int
        """
        return _libsedml.XMLNamespaces_remove(self, *args)

    def clear(self):
        """clear(XMLNamespaces self) -> int"""
        return _libsedml.XMLNamespaces_clear(self)

    def getIndex(self, uri):
        """getIndex(XMLNamespaces self, string uri) -> int"""
        return _libsedml.XMLNamespaces_getIndex(self, uri)

    def containsUri(self, uri):
        """containsUri(XMLNamespaces self, string uri) -> bool"""
        return _libsedml.XMLNamespaces_containsUri(self, uri)

    def getIndexByPrefix(self, prefix):
        """getIndexByPrefix(XMLNamespaces self, string prefix) -> int"""
        return _libsedml.XMLNamespaces_getIndexByPrefix(self, prefix)

    def getLength(self):
        """getLength(XMLNamespaces self) -> int"""
        return _libsedml.XMLNamespaces_getLength(self)

    def getNumNamespaces(self):
        """getNumNamespaces(XMLNamespaces self) -> int"""
        return _libsedml.XMLNamespaces_getNumNamespaces(self)

    def getPrefix(self, *args):
        """
        getPrefix(XMLNamespaces self, int index) -> string
        getPrefix(XMLNamespaces self, string uri) -> string
        """
        return _libsedml.XMLNamespaces_getPrefix(self, *args)

    def getURI(self, *args):
        """
        getURI(XMLNamespaces self, int index) -> string
        getURI(XMLNamespaces self, string prefix="") -> string
        """
        return _libsedml.XMLNamespaces_getURI(self, *args)

    def isEmpty(self):
        """isEmpty(XMLNamespaces self) -> bool"""
        return _libsedml.XMLNamespaces_isEmpty(self)

    def hasURI(self, uri):
        """hasURI(XMLNamespaces self, string uri) -> bool"""
        return _libsedml.XMLNamespaces_hasURI(self, uri)

    def hasPrefix(self, prefix):
        """hasPrefix(XMLNamespaces self, string prefix) -> bool"""
        return _libsedml.XMLNamespaces_hasPrefix(self, prefix)

    def hasNS(self, uri, prefix):
        """hasNS(XMLNamespaces self, string uri, string prefix) -> bool"""
        return _libsedml.XMLNamespaces_hasNS(self, uri, prefix)

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True


_libsedml.XMLNamespaces_swigregister(XMLNamespaces)

class XMLToken(object):
    """Proxy of C++ XMLToken class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_XMLToken

    def __init__(self, *args):
        """
        __init__(XMLToken self) -> XMLToken
        __init__(XMLToken self, XMLTriple triple, XMLAttributes attributes, XMLNamespaces namespaces, unsigned int const line=0, unsigned int const column=0) -> XMLToken
        __init__(XMLToken self, XMLTriple triple, XMLAttributes attributes, unsigned int const line=0, unsigned int const column=0) -> XMLToken
        __init__(XMLToken self, XMLTriple triple, unsigned int const line=0, unsigned int const column=0) -> XMLToken
        __init__(XMLToken self, string chars, unsigned int const line=0, unsigned int const column=0) -> XMLToken
        __init__(XMLToken self, XMLToken orig) -> XMLToken
        """
        _libsedml.XMLToken_swiginit(self, _libsedml.new_XMLToken(*args))

    def clone(self):
        """clone(XMLToken self) -> XMLToken"""
        return _libsedml.XMLToken_clone(self)

    def getAttributes(self):
        """getAttributes(XMLToken self) -> XMLAttributes"""
        return _libsedml.XMLToken_getAttributes(self)

    def setAttributes(self, attributes):
        """setAttributes(XMLToken self, XMLAttributes attributes) -> int"""
        return _libsedml.XMLToken_setAttributes(self, attributes)

    def addAttr(self, *args):
        """
        addAttr(XMLToken self, string name, string value, string namespaceURI="", string prefix="") -> int
        addAttr(XMLToken self, XMLTriple triple, string value) -> int
        """
        return _libsedml.XMLToken_addAttr(self, *args)

    def removeAttr(self, *args):
        """
        removeAttr(XMLToken self, int n) -> int
        removeAttr(XMLToken self, string name, string uri="") -> int
        removeAttr(XMLToken self, XMLTriple triple) -> int
        """
        return _libsedml.XMLToken_removeAttr(self, *args)

    def clearAttributes(self):
        """clearAttributes(XMLToken self) -> int"""
        return _libsedml.XMLToken_clearAttributes(self)

    def getAttrIndex(self, *args):
        """
        getAttrIndex(XMLToken self, string name, string uri="") -> int
        getAttrIndex(XMLToken self, XMLTriple triple) -> int
        """
        return _libsedml.XMLToken_getAttrIndex(self, *args)

    def getAttributesLength(self):
        """getAttributesLength(XMLToken self) -> int"""
        return _libsedml.XMLToken_getAttributesLength(self)

    def getAttrName(self, index):
        """getAttrName(XMLToken self, int index) -> string"""
        return _libsedml.XMLToken_getAttrName(self, index)

    def getAttrPrefix(self, index):
        """getAttrPrefix(XMLToken self, int index) -> string"""
        return _libsedml.XMLToken_getAttrPrefix(self, index)

    def getAttrPrefixedName(self, index):
        """getAttrPrefixedName(XMLToken self, int index) -> string"""
        return _libsedml.XMLToken_getAttrPrefixedName(self, index)

    def getAttrURI(self, index):
        """getAttrURI(XMLToken self, int index) -> string"""
        return _libsedml.XMLToken_getAttrURI(self, index)

    def getAttrValue(self, *args):
        """
        getAttrValue(XMLToken self, int index) -> string
        getAttrValue(XMLToken self, string name, string uri="") -> string
        getAttrValue(XMLToken self, XMLTriple triple) -> string
        """
        return _libsedml.XMLToken_getAttrValue(self, *args)

    def hasAttr(self, *args):
        """
        hasAttr(XMLToken self, int index) -> bool
        hasAttr(XMLToken self, string name, string uri="") -> bool
        hasAttr(XMLToken self, XMLTriple triple) -> bool
        """
        return _libsedml.XMLToken_hasAttr(self, *args)

    def isAttributesEmpty(self):
        """isAttributesEmpty(XMLToken self) -> bool"""
        return _libsedml.XMLToken_isAttributesEmpty(self)

    def getNamespaces(self):
        """getNamespaces(XMLToken self) -> XMLNamespaces"""
        return _libsedml.XMLToken_getNamespaces(self)

    def setNamespaces(self, namespaces):
        """setNamespaces(XMLToken self, XMLNamespaces namespaces) -> int"""
        return _libsedml.XMLToken_setNamespaces(self, namespaces)

    def addNamespace(self, *args):
        """addNamespace(XMLToken self, string uri, string prefix="") -> int"""
        return _libsedml.XMLToken_addNamespace(self, *args)

    def removeNamespace(self, *args):
        """
        removeNamespace(XMLToken self, int index) -> int
        removeNamespace(XMLToken self, string prefix) -> int
        """
        return _libsedml.XMLToken_removeNamespace(self, *args)

    def clearNamespaces(self):
        """clearNamespaces(XMLToken self) -> int"""
        return _libsedml.XMLToken_clearNamespaces(self)

    def getNamespaceIndex(self, uri):
        """getNamespaceIndex(XMLToken self, string uri) -> int"""
        return _libsedml.XMLToken_getNamespaceIndex(self, uri)

    def getNamespaceIndexByPrefix(self, prefix):
        """getNamespaceIndexByPrefix(XMLToken self, string prefix) -> int"""
        return _libsedml.XMLToken_getNamespaceIndexByPrefix(self, prefix)

    def getNamespacesLength(self):
        """getNamespacesLength(XMLToken self) -> int"""
        return _libsedml.XMLToken_getNamespacesLength(self)

    def getNamespacePrefix(self, *args):
        """
        getNamespacePrefix(XMLToken self, int index) -> string
        getNamespacePrefix(XMLToken self, string uri) -> string
        """
        return _libsedml.XMLToken_getNamespacePrefix(self, *args)

    def getNamespaceURI(self, *args):
        """
        getNamespaceURI(XMLToken self, int index) -> string
        getNamespaceURI(XMLToken self, string prefix="") -> string
        """
        return _libsedml.XMLToken_getNamespaceURI(self, *args)

    def isNamespacesEmpty(self):
        """isNamespacesEmpty(XMLToken self) -> bool"""
        return _libsedml.XMLToken_isNamespacesEmpty(self)

    def hasNamespaceURI(self, uri):
        """hasNamespaceURI(XMLToken self, string uri) -> bool"""
        return _libsedml.XMLToken_hasNamespaceURI(self, uri)

    def hasNamespacePrefix(self, prefix):
        """hasNamespacePrefix(XMLToken self, string prefix) -> bool"""
        return _libsedml.XMLToken_hasNamespacePrefix(self, prefix)

    def hasNamespaceNS(self, uri, prefix):
        """hasNamespaceNS(XMLToken self, string uri, string prefix) -> bool"""
        return _libsedml.XMLToken_hasNamespaceNS(self, uri, prefix)

    def setTriple(self, triple):
        """setTriple(XMLToken self, XMLTriple triple) -> int"""
        return _libsedml.XMLToken_setTriple(self, triple)

    def getName(self):
        """getName(XMLToken self) -> string"""
        return _libsedml.XMLToken_getName(self)

    def getPrefix(self):
        """getPrefix(XMLToken self) -> string"""
        return _libsedml.XMLToken_getPrefix(self)

    def getURI(self):
        """getURI(XMLToken self) -> string"""
        return _libsedml.XMLToken_getURI(self)

    def getCharacters(self):
        """getCharacters(XMLToken self) -> string"""
        return _libsedml.XMLToken_getCharacters(self)

    def setCharacters(self, chars):
        """setCharacters(XMLToken self, string chars) -> int"""
        return _libsedml.XMLToken_setCharacters(self, chars)

    def append(self, chars):
        """append(XMLToken self, string chars) -> int"""
        return _libsedml.XMLToken_append(self, chars)

    def getColumn(self):
        """getColumn(XMLToken self) -> unsigned int"""
        return _libsedml.XMLToken_getColumn(self)

    def getLine(self):
        """getLine(XMLToken self) -> unsigned int"""
        return _libsedml.XMLToken_getLine(self)

    def isElement(self):
        """isElement(XMLToken self) -> bool"""
        return _libsedml.XMLToken_isElement(self)

    def isEnd(self):
        """isEnd(XMLToken self) -> bool"""
        return _libsedml.XMLToken_isEnd(self)

    def isEndFor(self, element):
        """isEndFor(XMLToken self, XMLToken element) -> bool"""
        return _libsedml.XMLToken_isEndFor(self, element)

    def isEOF(self):
        """isEOF(XMLToken self) -> bool"""
        return _libsedml.XMLToken_isEOF(self)

    def isStart(self):
        """isStart(XMLToken self) -> bool"""
        return _libsedml.XMLToken_isStart(self)

    def isText(self):
        """isText(XMLToken self) -> bool"""
        return _libsedml.XMLToken_isText(self)

    def setEnd(self):
        """setEnd(XMLToken self) -> int"""
        return _libsedml.XMLToken_setEnd(self)

    def setEOF(self):
        """setEOF(XMLToken self) -> int"""
        return _libsedml.XMLToken_setEOF(self)

    def unsetEnd(self):
        """unsetEnd(XMLToken self) -> int"""
        return _libsedml.XMLToken_unsetEnd(self)

    def toString(self):
        """toString(XMLToken self) -> string"""
        return _libsedml.XMLToken_toString(self)

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True


_libsedml.XMLToken_swigregister(XMLToken)

class XMLNode(XMLToken):
    """Proxy of C++ XMLNode class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_XMLNode

    def __init__(self, *args):
        """
        __init__(XMLNode self) -> XMLNode
        __init__(XMLNode self, XMLToken token) -> XMLNode
        __init__(XMLNode self, XMLTriple triple, XMLAttributes attributes, XMLNamespaces namespaces, unsigned int const line=0, unsigned int const column=0) -> XMLNode
        __init__(XMLNode self, XMLTriple triple, XMLAttributes attributes, unsigned int const line=0, unsigned int const column=0) -> XMLNode
        __init__(XMLNode self, XMLTriple triple, unsigned int const line=0, unsigned int const column=0) -> XMLNode
        __init__(XMLNode self, string chars, unsigned int const line=0, unsigned int const column=0) -> XMLNode
        __init__(XMLNode self, XMLInputStream stream) -> XMLNode
        __init__(XMLNode self, XMLNode orig) -> XMLNode
        """
        _libsedml.XMLNode_swiginit(self, _libsedml.new_XMLNode(*args))

    def clone(self):
        """clone(XMLNode self) -> XMLNode"""
        return _libsedml.XMLNode_clone(self)

    def addChild(self, node):
        """addChild(XMLNode self, XMLNode node) -> int"""
        return _libsedml.XMLNode_addChild(self, node)

    def insertChild(self, n, node):
        """insertChild(XMLNode self, unsigned int n, XMLNode node) -> XMLNode"""
        return _libsedml.XMLNode_insertChild(self, n, node)

    def removeChild(self, n):
        """removeChild(XMLNode self, unsigned int n) -> XMLNode"""
        return _libsedml.XMLNode_removeChild(self, n)

    def removeChildren(self):
        """removeChildren(XMLNode self) -> int"""
        return _libsedml.XMLNode_removeChildren(self)

    def getChild(self, *args):
        """
        getChild(XMLNode self, unsigned int n) -> XMLNode
        getChild(XMLNode self, unsigned int n) -> XMLNode
        getChild(XMLNode self, string name) -> XMLNode
        getChild(XMLNode self, string name) -> XMLNode
        """
        return _libsedml.XMLNode_getChild(self, *args)

    def getIndex(self, name):
        """getIndex(XMLNode self, string name) -> int"""
        return _libsedml.XMLNode_getIndex(self, name)

    def hasChild(self, name):
        """hasChild(XMLNode self, string name) -> bool"""
        return _libsedml.XMLNode_hasChild(self, name)

    def equals(self, other, ignoreURI=False, ignoreAttributeValues=False):
        """equals(XMLNode self, XMLNode other, bool ignoreURI=False, bool ignoreAttributeValues=False) -> bool"""
        return _libsedml.XMLNode_equals(self, other, ignoreURI, ignoreAttributeValues)

    def getNumChildren(self):
        """getNumChildren(XMLNode self) -> unsigned int"""
        return _libsedml.XMLNode_getNumChildren(self)

    def writeToStream(self, stream):
        """writeToStream(XMLNode self, XMLOutputStream stream)"""
        return _libsedml.XMLNode_writeToStream(self, stream)

    def toXMLString(self):
        """toXMLString(XMLNode self) -> string"""
        return _libsedml.XMLNode_toXMLString(self)

    @staticmethod
    def convertXMLNodeToString(node):
        """convertXMLNodeToString(XMLNode node) -> string"""
        return _libsedml.XMLNode_convertXMLNodeToString(node)

    @staticmethod
    def convertStringToXMLNode(xmlstr, xmlns=None):
        """convertStringToXMLNode(string xmlstr, XMLNamespaces xmlns=None) -> XMLNode"""
        return _libsedml.XMLNode_convertStringToXMLNode(xmlstr, xmlns)


_libsedml.XMLNode_swigregister(XMLNode)

def XMLNode_convertXMLNodeToString(node):
    """XMLNode_convertXMLNodeToString(XMLNode node) -> string"""
    return _libsedml.XMLNode_convertXMLNodeToString(node)


def XMLNode_convertStringToXMLNode(xmlstr, xmlns=None):
    """XMLNode_convertStringToXMLNode(string xmlstr, XMLNamespaces xmlns=None) -> XMLNode"""
    return _libsedml.XMLNode_convertStringToXMLNode(xmlstr, xmlns)


class XMLTriple(object):
    """Proxy of C++ XMLTriple class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(XMLTriple self) -> XMLTriple
        __init__(XMLTriple self, string name, string uri, string prefix) -> XMLTriple
        __init__(XMLTriple self, string triplet, char const sepchar=' ') -> XMLTriple
        __init__(XMLTriple self, XMLTriple orig) -> XMLTriple
        """
        _libsedml.XMLTriple_swiginit(self, _libsedml.new_XMLTriple(*args))

    def clone(self):
        """clone(XMLTriple self) -> XMLTriple"""
        return _libsedml.XMLTriple_clone(self)

    def getName(self):
        """getName(XMLTriple self) -> string"""
        return _libsedml.XMLTriple_getName(self)

    def getPrefix(self):
        """getPrefix(XMLTriple self) -> string"""
        return _libsedml.XMLTriple_getPrefix(self)

    def getURI(self):
        """getURI(XMLTriple self) -> string"""
        return _libsedml.XMLTriple_getURI(self)

    def getPrefixedName(self):
        """getPrefixedName(XMLTriple self) -> string"""
        return _libsedml.XMLTriple_getPrefixedName(self)

    def isEmpty(self):
        """isEmpty(XMLTriple self) -> bool"""
        return _libsedml.XMLTriple_isEmpty(self)

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True

    __swig_destroy__ = _libsedml.delete_XMLTriple


_libsedml.XMLTriple_swigregister(XMLTriple)

class XMLOutputStream(object):
    """Proxy of C++ XMLOutputStream class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """__init__(XMLOutputStream self, ostream stream, string encoding="UTF-8", bool writeXMLDecl=True, string programName="", string programVersion="") -> XMLOutputStream"""
        _libsedml.XMLOutputStream_swiginit(self, _libsedml.new_XMLOutputStream(*args))

    __swig_destroy__ = _libsedml.delete_XMLOutputStream

    def endElement(self, *args):
        """
        endElement(XMLOutputStream self, string name, string prefix="")
        endElement(XMLOutputStream self, XMLTriple triple, bool text=False)
        """
        return _libsedml.XMLOutputStream_endElement(self, *args)

    def setAutoIndent(self, indent):
        """setAutoIndent(XMLOutputStream self, bool indent)"""
        return _libsedml.XMLOutputStream_setAutoIndent(self, indent)

    def startElement(self, *args):
        """
        startElement(XMLOutputStream self, string name, string prefix="")
        startElement(XMLOutputStream self, XMLTriple triple)
        """
        return _libsedml.XMLOutputStream_startElement(self, *args)

    def startEndElement(self, *args):
        """
        startEndElement(XMLOutputStream self, string name, string prefix="")
        startEndElement(XMLOutputStream self, XMLTriple triple)
        """
        return _libsedml.XMLOutputStream_startEndElement(self, *args)

    def writeAttribute(self, *args):
        """
        writeAttribute(XMLOutputStream self, string name, string value)
        writeAttribute(XMLOutputStream self, string name, string prefix, string value)
        writeAttribute(XMLOutputStream self, XMLTriple triple, string value)
        writeAttribute(XMLOutputStream self, string name, char const * value)
        writeAttribute(XMLOutputStream self, string name, string prefix, char const * value)
        writeAttribute(XMLOutputStream self, XMLTriple triple, char const * value)
        writeAttribute(XMLOutputStream self, string name, bool const & value)
        writeAttribute(XMLOutputStream self, string name, string prefix, bool const & value)
        writeAttribute(XMLOutputStream self, XMLTriple triple, bool const & value)
        writeAttribute(XMLOutputStream self, string name, double const & value)
        writeAttribute(XMLOutputStream self, string name, string prefix, double const & value)
        writeAttribute(XMLOutputStream self, XMLTriple triple, double const & value)
        writeAttribute(XMLOutputStream self, string name, long const & value)
        writeAttribute(XMLOutputStream self, string name, string prefix, long const & value)
        writeAttribute(XMLOutputStream self, XMLTriple triple, long const & value)
        writeAttribute(XMLOutputStream self, string name, int const & value)
        writeAttribute(XMLOutputStream self, string name, string prefix, int const & value)
        writeAttribute(XMLOutputStream self, XMLTriple triple, int const & value)
        writeAttribute(XMLOutputStream self, string name, string prefix, unsigned int const & value)
        """
        if type(args[1]) == type(True):
            return _libsedml.XMLOutputStream_writeAttributeBool(self, *args)
        return _libsedml.XMLOutputStream_writeAttribute(self, *args)

    def writeXMLDecl(self):
        """writeXMLDecl(XMLOutputStream self)"""
        return _libsedml.XMLOutputStream_writeXMLDecl(self)

    def writeComment(self, programName, programVersion, writeTimestamp=True):
        """writeComment(XMLOutputStream self, string programName, string programVersion, bool writeTimestamp=True)"""
        return _libsedml.XMLOutputStream_writeComment(self, programName, programVersion, writeTimestamp)

    def downIndent(self):
        """downIndent(XMLOutputStream self)"""
        return _libsedml.XMLOutputStream_downIndent(self)

    def upIndent(self):
        """upIndent(XMLOutputStream self)"""
        return _libsedml.XMLOutputStream_upIndent(self)

    def getSBMLNamespaces(self):
        """getSBMLNamespaces(XMLOutputStream self) -> SBMLNamespaces *"""
        return _libsedml.XMLOutputStream_getSBMLNamespaces(self)

    def setSBMLNamespaces(self, sbmlns):
        """setSBMLNamespaces(XMLOutputStream self, SBMLNamespaces * sbmlns)"""
        return _libsedml.XMLOutputStream_setSBMLNamespaces(self, sbmlns)

    @staticmethod
    def getWriteComment():
        """getWriteComment() -> bool"""
        return _libsedml.XMLOutputStream_getWriteComment()

    @staticmethod
    def setWriteComment(writeComment):
        """setWriteComment(bool writeComment)"""
        return _libsedml.XMLOutputStream_setWriteComment(writeComment)

    @staticmethod
    def getWriteTimestamp():
        """getWriteTimestamp() -> bool"""
        return _libsedml.XMLOutputStream_getWriteTimestamp()

    @staticmethod
    def setWriteTimestamp(writeTimestamp):
        """setWriteTimestamp(bool writeTimestamp)"""
        return _libsedml.XMLOutputStream_setWriteTimestamp(writeTimestamp)

    @staticmethod
    def getLibraryName():
        """getLibraryName() -> string"""
        return _libsedml.XMLOutputStream_getLibraryName()

    @staticmethod
    def setLibraryName(libraryName):
        """setLibraryName(string libraryName)"""
        return _libsedml.XMLOutputStream_setLibraryName(libraryName)

    @staticmethod
    def getLibraryVersion():
        """getLibraryVersion() -> string"""
        return _libsedml.XMLOutputStream_getLibraryVersion()

    @staticmethod
    def setLibraryVersion(libraryVersion):
        """setLibraryVersion(string libraryVersion)"""
        return _libsedml.XMLOutputStream_setLibraryVersion(libraryVersion)

    def getIndent(self):
        """getIndent(XMLOutputStream self) -> unsigned int"""
        return _libsedml.XMLOutputStream_getIndent(self)

    def setIndent(self, indent):
        """setIndent(XMLOutputStream self, unsigned int indent)"""
        return _libsedml.XMLOutputStream_setIndent(self, indent)

    def writeAttributeBool(self, *args):
        """
        writeAttributeBool(XMLOutputStream self, string name, bool const & value)
        writeAttributeBool(XMLOutputStream self, XMLTriple name, bool const & value)
        """
        return _libsedml.XMLOutputStream_writeAttributeBool(self, *args)

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True


_libsedml.XMLOutputStream_swigregister(XMLOutputStream)

def XMLOutputStream_getWriteComment():
    """XMLOutputStream_getWriteComment() -> bool"""
    return _libsedml.XMLOutputStream_getWriteComment()


def XMLOutputStream_setWriteComment(writeComment):
    """XMLOutputStream_setWriteComment(bool writeComment)"""
    return _libsedml.XMLOutputStream_setWriteComment(writeComment)


def XMLOutputStream_getWriteTimestamp():
    """XMLOutputStream_getWriteTimestamp() -> bool"""
    return _libsedml.XMLOutputStream_getWriteTimestamp()


def XMLOutputStream_setWriteTimestamp(writeTimestamp):
    """XMLOutputStream_setWriteTimestamp(bool writeTimestamp)"""
    return _libsedml.XMLOutputStream_setWriteTimestamp(writeTimestamp)


def XMLOutputStream_getLibraryName():
    """XMLOutputStream_getLibraryName() -> string"""
    return _libsedml.XMLOutputStream_getLibraryName()


def XMLOutputStream_setLibraryName(libraryName):
    """XMLOutputStream_setLibraryName(string libraryName)"""
    return _libsedml.XMLOutputStream_setLibraryName(libraryName)


def XMLOutputStream_getLibraryVersion():
    """XMLOutputStream_getLibraryVersion() -> string"""
    return _libsedml.XMLOutputStream_getLibraryVersion()


def XMLOutputStream_setLibraryVersion(libraryVersion):
    """XMLOutputStream_setLibraryVersion(string libraryVersion)"""
    return _libsedml.XMLOutputStream_setLibraryVersion(libraryVersion)


class XMLOwningOutputStringStream(object):
    """Proxy of C++ XMLOwningOutputStringStream class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """__init__(XMLOwningOutputStringStream self, string encoding="UTF-8", bool writeXMLDecl=True, string programName="", string programVersion="") -> XMLOwningOutputStringStream"""
        _libsedml.XMLOwningOutputStringStream_swiginit(self, _libsedml.new_XMLOwningOutputStringStream(*args))

    __swig_destroy__ = _libsedml.delete_XMLOwningOutputStringStream


_libsedml.XMLOwningOutputStringStream_swigregister(XMLOwningOutputStringStream)

class XMLOwningOutputFileStream(object):
    """Proxy of C++ XMLOwningOutputFileStream class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """__init__(XMLOwningOutputFileStream self, string filename, string encoding="UTF-8", bool writeXMLDecl=True, string programName="", string programVersion="") -> XMLOwningOutputFileStream"""
        _libsedml.XMLOwningOutputFileStream_swiginit(self, _libsedml.new_XMLOwningOutputFileStream(*args))

    __swig_destroy__ = _libsedml.delete_XMLOwningOutputFileStream


_libsedml.XMLOwningOutputFileStream_swigregister(XMLOwningOutputFileStream)

class XMLInputStream(object):
    """Proxy of C++ XMLInputStream class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """__init__(XMLInputStream self, char const * content, bool isFile=True, string library="", XMLErrorLog errorLog=None) -> XMLInputStream"""
        _libsedml.XMLInputStream_swiginit(self, _libsedml.new_XMLInputStream(*args))

    __swig_destroy__ = _libsedml.delete_XMLInputStream

    def getEncoding(self):
        """getEncoding(XMLInputStream self) -> string"""
        return _libsedml.XMLInputStream_getEncoding(self)

    def getVersion(self):
        """getVersion(XMLInputStream self) -> string"""
        return _libsedml.XMLInputStream_getVersion(self)

    def getErrorLog(self):
        """getErrorLog(XMLInputStream self) -> XMLErrorLog"""
        return _libsedml.XMLInputStream_getErrorLog(self)

    def isEOF(self):
        """isEOF(XMLInputStream self) -> bool"""
        return _libsedml.XMLInputStream_isEOF(self)

    def isError(self):
        """isError(XMLInputStream self) -> bool"""
        return _libsedml.XMLInputStream_isError(self)

    def isGood(self):
        """isGood(XMLInputStream self) -> bool"""
        return _libsedml.XMLInputStream_isGood(self)

    def next(self):
        """next(XMLInputStream self) -> XMLToken"""
        return _libsedml.XMLInputStream_next(self)

    def peek(self):
        """peek(XMLInputStream self) -> XMLToken"""
        return _libsedml.XMLInputStream_peek(self)

    def skipPastEnd(self, element):
        """skipPastEnd(XMLInputStream self, XMLToken element)"""
        return _libsedml.XMLInputStream_skipPastEnd(self, element)

    def skipText(self):
        """skipText(XMLInputStream self)"""
        return _libsedml.XMLInputStream_skipText(self)

    def setErrorLog(self, log):
        """setErrorLog(XMLInputStream self, XMLErrorLog log) -> int"""
        return _libsedml.XMLInputStream_setErrorLog(self, log)

    def toString(self):
        """toString(XMLInputStream self) -> string"""
        return _libsedml.XMLInputStream_toString(self)

    def getSBMLNamespaces(self):
        """getSBMLNamespaces(XMLInputStream self) -> SBMLNamespaces *"""
        return _libsedml.XMLInputStream_getSBMLNamespaces(self)

    def setSBMLNamespaces(self, sbmlns):
        """setSBMLNamespaces(XMLInputStream self, SBMLNamespaces * sbmlns)"""
        return _libsedml.XMLInputStream_setSBMLNamespaces(self, sbmlns)

    def determineNumberChildren(self, *args):
        """determineNumberChildren(XMLInputStream self, string elementName="") -> unsigned int"""
        return _libsedml.XMLInputStream_determineNumberChildren(self, *args)

    def determineNumSpecificChildren(self, childName, container):
        """determineNumSpecificChildren(XMLInputStream self, string childName, string container) -> unsigned int"""
        return _libsedml.XMLInputStream_determineNumSpecificChildren(self, childName, container)

    def containsChild(self, childName, container):
        """containsChild(XMLInputStream self, string childName, string container) -> bool"""
        return _libsedml.XMLInputStream_containsChild(self, childName, container)


_libsedml.XMLInputStream_swigregister(XMLInputStream)

class ASTNode(object):
    """Proxy of C++ ASTNode class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(ASTNode self, ASTNodeType_t type=AST_UNKNOWN) -> ASTNode
        __init__(ASTNode self, ASTNode orig) -> ASTNode
        """
        _libsedml.ASTNode_swiginit(self, _libsedml.new_ASTNode(*args))

    __swig_destroy__ = _libsedml.delete_ASTNode

    def freeName(self):
        """freeName(ASTNode self) -> int"""
        return _libsedml.ASTNode_freeName(self)

    def canonicalize(self):
        """canonicalize(ASTNode self) -> bool"""
        return _libsedml.ASTNode_canonicalize(self)

    def addChild(self, disownedChild, inRead=False):
        """addChild(ASTNode self, ASTNode disownedChild, bool inRead=False) -> int"""
        if disownedChild is not None:
            disownedChild.thisown = 0
        return _libsedml.ASTNode_addChild(self, disownedChild, inRead)

    def prependChild(self, disownedChild):
        """prependChild(ASTNode self, ASTNode disownedChild) -> int"""
        if disownedChild is not None:
            disownedChild.thisown = 0
        return _libsedml.ASTNode_prependChild(self, disownedChild)

    def removeChild(self, n):
        """removeChild(ASTNode self, unsigned int n) -> int"""
        return _libsedml.ASTNode_removeChild(self, n)

    def replaceChild(self, n, disownedChild, delreplaced=False):
        """replaceChild(ASTNode self, unsigned int n, ASTNode disownedChild, bool delreplaced=False) -> int"""
        if disownedChild is not None:
            disownedChild.thisown = 0
        return _libsedml.ASTNode_replaceChild(self, n, disownedChild, delreplaced)

    def insertChild(self, n, disownedChild):
        """insertChild(ASTNode self, unsigned int n, ASTNode disownedChild) -> int"""
        if disownedChild is not None:
            disownedChild.thisown = 0
        return _libsedml.ASTNode_insertChild(self, n, disownedChild)

    def deepCopy(self):
        """deepCopy(ASTNode self) -> ASTNode"""
        return _libsedml.ASTNode_deepCopy(self)

    def getChild(self, n):
        """getChild(ASTNode self, unsigned int n) -> ASTNode"""
        return _libsedml.ASTNode_getChild(self, n)

    def getLeftChild(self):
        """getLeftChild(ASTNode self) -> ASTNode"""
        return _libsedml.ASTNode_getLeftChild(self)

    def getRightChild(self):
        """getRightChild(ASTNode self) -> ASTNode"""
        return _libsedml.ASTNode_getRightChild(self)

    def getNumChildren(self):
        """getNumChildren(ASTNode self) -> unsigned int"""
        return _libsedml.ASTNode_getNumChildren(self)

    def addSemanticsAnnotation(self, disownedAnnotation):
        """addSemanticsAnnotation(ASTNode self, XMLNode disownedAnnotation) -> int"""
        if disownedAnnotation is not None:
            disownedAnnotation.thisown = 0
        return _libsedml.ASTNode_addSemanticsAnnotation(self, disownedAnnotation)

    def getNumSemanticsAnnotations(self):
        """getNumSemanticsAnnotations(ASTNode self) -> unsigned int"""
        return _libsedml.ASTNode_getNumSemanticsAnnotations(self)

    def getSemanticsAnnotation(self, n):
        """getSemanticsAnnotation(ASTNode self, unsigned int n) -> XMLNode"""
        return _libsedml.ASTNode_getSemanticsAnnotation(self, n)

    def getCharacter(self):
        """getCharacter(ASTNode self) -> char"""
        return _libsedml.ASTNode_getCharacter(self)

    def getId(self):
        """getId(ASTNode self) -> string"""
        return _libsedml.ASTNode_getId(self)

    def getClass(self):
        """getClass(ASTNode self) -> string"""
        return _libsedml.ASTNode_getClass(self)

    def getStyle(self):
        """getStyle(ASTNode self) -> string"""
        return _libsedml.ASTNode_getStyle(self)

    def getInteger(self):
        """getInteger(ASTNode self) -> long"""
        return _libsedml.ASTNode_getInteger(self)

    def getName(self):
        """getName(ASTNode self) -> char const *"""
        return _libsedml.ASTNode_getName(self)

    def getOperatorName(self):
        """getOperatorName(ASTNode self) -> char const *"""
        return _libsedml.ASTNode_getOperatorName(self)

    def getNumerator(self):
        """getNumerator(ASTNode self) -> long"""
        return _libsedml.ASTNode_getNumerator(self)

    def getDenominator(self):
        """getDenominator(ASTNode self) -> long"""
        return _libsedml.ASTNode_getDenominator(self)

    def getReal(self):
        """getReal(ASTNode self) -> double"""
        return _libsedml.ASTNode_getReal(self)

    def getMantissa(self):
        """getMantissa(ASTNode self) -> double"""
        return _libsedml.ASTNode_getMantissa(self)

    def getExponent(self):
        """getExponent(ASTNode self) -> long"""
        return _libsedml.ASTNode_getExponent(self)

    def getValue(self):
        """getValue(ASTNode self) -> double"""
        return _libsedml.ASTNode_getValue(self)

    def getPrecedence(self):
        """getPrecedence(ASTNode self) -> int"""
        return _libsedml.ASTNode_getPrecedence(self)

    def getType(self):
        """getType(ASTNode self) -> ASTNodeType_t"""
        return _libsedml.ASTNode_getType(self)

    def getUnits(self):
        """getUnits(ASTNode self) -> string"""
        return _libsedml.ASTNode_getUnits(self)

    def isAvogadro(self):
        """isAvogadro(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isAvogadro(self)

    def isBoolean(self):
        """isBoolean(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isBoolean(self)

    def returnsBoolean(self, model=None):
        """returnsBoolean(ASTNode self, Model const * model=None) -> bool"""
        return _libsedml.ASTNode_returnsBoolean(self, model)

    def isConstant(self):
        """isConstant(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isConstant(self)

    def isCiNumber(self):
        """isCiNumber(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isCiNumber(self)

    def isConstantNumber(self):
        """isConstantNumber(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isConstantNumber(self)

    def isCSymbolFunction(self):
        """isCSymbolFunction(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isCSymbolFunction(self)

    def isFunction(self):
        """isFunction(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isFunction(self)

    def isInfinity(self):
        """isInfinity(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isInfinity(self)

    def isInteger(self):
        """isInteger(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isInteger(self)

    def isLambda(self):
        """isLambda(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isLambda(self)

    def isLog10(self):
        """isLog10(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isLog10(self)

    def isLogical(self):
        """isLogical(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isLogical(self)

    def isName(self):
        """isName(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isName(self)

    def isNaN(self):
        """isNaN(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isNaN(self)

    def isNegInfinity(self):
        """isNegInfinity(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isNegInfinity(self)

    def isNumber(self):
        """isNumber(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isNumber(self)

    def isOperator(self):
        """isOperator(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isOperator(self)

    def isPiecewise(self):
        """isPiecewise(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isPiecewise(self)

    def isRational(self):
        """isRational(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isRational(self)

    def isReal(self):
        """isReal(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isReal(self)

    def isRelational(self):
        """isRelational(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isRelational(self)

    def isSqrt(self):
        """isSqrt(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isSqrt(self)

    def isUMinus(self):
        """isUMinus(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isUMinus(self)

    def isUPlus(self):
        """isUPlus(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isUPlus(self)

    def isUserFunction(self):
        """isUserFunction(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isUserFunction(self)

    def hasTypeAndNumChildren(self, type, numchildren):
        """hasTypeAndNumChildren(ASTNode self, ASTNodeType_t type, unsigned int numchildren) -> int"""
        return _libsedml.ASTNode_hasTypeAndNumChildren(self, type, numchildren)

    def isUnknown(self):
        """isUnknown(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isUnknown(self)

    def isSetId(self):
        """isSetId(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isSetId(self)

    def isSetClass(self):
        """isSetClass(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isSetClass(self)

    def isSetStyle(self):
        """isSetStyle(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isSetStyle(self)

    def isSetUnits(self):
        """isSetUnits(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isSetUnits(self)

    def hasUnits(self):
        """hasUnits(ASTNode self) -> bool"""
        return _libsedml.ASTNode_hasUnits(self)

    def setCharacter(self, value):
        """setCharacter(ASTNode self, char value) -> int"""
        return _libsedml.ASTNode_setCharacter(self, value)

    def setId(self, id):
        """setId(ASTNode self, string id) -> int"""
        return _libsedml.ASTNode_setId(self, id)

    def setClass(self, className):
        """setClass(ASTNode self, string className) -> int"""
        return _libsedml.ASTNode_setClass(self, className)

    def setStyle(self, style):
        """setStyle(ASTNode self, string style) -> int"""
        return _libsedml.ASTNode_setStyle(self, style)

    def setName(self, name):
        """setName(ASTNode self, char const * name) -> int"""
        return _libsedml.ASTNode_setName(self, name)

    def setValue(self, *args):
        """
        setValue(ASTNode self, long value) -> int
        setValue(ASTNode self, long numerator, long denominator) -> int
        setValue(ASTNode self, double value) -> int
        setValue(ASTNode self, double mantissa, long exponent) -> int
        """
        return _libsedml.ASTNode_setValue(self, *args)

    def setType(self, type):
        """setType(ASTNode self, ASTNodeType_t type) -> int"""
        return _libsedml.ASTNode_setType(self, type)

    def setUnits(self, units):
        """setUnits(ASTNode self, string units) -> int"""
        return _libsedml.ASTNode_setUnits(self, units)

    def swapChildren(self, that):
        """swapChildren(ASTNode self, ASTNode that) -> int"""
        return _libsedml.ASTNode_swapChildren(self, that)

    def renameSIdRefs(self, oldid, newid):
        """renameSIdRefs(ASTNode self, string oldid, string newid)"""
        return _libsedml.ASTNode_renameSIdRefs(self, oldid, newid)

    def renameUnitSIdRefs(self, oldid, newid):
        """renameUnitSIdRefs(ASTNode self, string oldid, string newid)"""
        return _libsedml.ASTNode_renameUnitSIdRefs(self, oldid, newid)

    def replaceIDWithFunction(self, id, function):
        """replaceIDWithFunction(ASTNode self, string id, ASTNode function)"""
        return _libsedml.ASTNode_replaceIDWithFunction(self, id, function)

    def multiplyTimeBy(self, function):
        """multiplyTimeBy(ASTNode self, ASTNode function)"""
        return _libsedml.ASTNode_multiplyTimeBy(self, function)

    def unsetUnits(self):
        """unsetUnits(ASTNode self) -> int"""
        return _libsedml.ASTNode_unsetUnits(self)

    def unsetId(self):
        """unsetId(ASTNode self) -> int"""
        return _libsedml.ASTNode_unsetId(self)

    def unsetClass(self):
        """unsetClass(ASTNode self) -> int"""
        return _libsedml.ASTNode_unsetClass(self)

    def unsetStyle(self):
        """unsetStyle(ASTNode self) -> int"""
        return _libsedml.ASTNode_unsetStyle(self)

    def getDefinitionURL(self):
        """getDefinitionURL(ASTNode self) -> XMLAttributes"""
        return _libsedml.ASTNode_getDefinitionURL(self)

    def replaceArgument(self, bvar, arg):
        """replaceArgument(ASTNode self, string bvar, ASTNode arg)"""
        return _libsedml.ASTNode_replaceArgument(self, bvar, arg)

    def getParentSBMLObject(self):
        """getParentSBMLObject(ASTNode self) -> SBase *"""
        return _libsedml.ASTNode_getParentSBMLObject(self)

    def unsetParentSBMLObject(self):
        """unsetParentSBMLObject(ASTNode self) -> int"""
        return _libsedml.ASTNode_unsetParentSBMLObject(self)

    def isSetParentSBMLObject(self):
        """isSetParentSBMLObject(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isSetParentSBMLObject(self)

    def reduceToBinary(self):
        """reduceToBinary(ASTNode self)"""
        return _libsedml.ASTNode_reduceToBinary(self)

    def unsetUserData(self):
        """unsetUserData(ASTNode self) -> int"""
        return _libsedml.ASTNode_unsetUserData(self)

    def isSetUserData(self):
        """isSetUserData(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isSetUserData(self)

    def isWellFormedASTNode(self):
        """isWellFormedASTNode(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isWellFormedASTNode(self)

    def hasCorrectNumberArguments(self):
        """hasCorrectNumberArguments(ASTNode self) -> bool"""
        return _libsedml.ASTNode_hasCorrectNumberArguments(self)

    def getDefinitionURLString(self):
        """getDefinitionURLString(ASTNode self) -> string"""
        return _libsedml.ASTNode_getDefinitionURLString(self)

    def representsBvar(self):
        """representsBvar(ASTNode self) -> bool"""
        return _libsedml.ASTNode_representsBvar(self)

    def isBvar(self):
        """isBvar(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isBvar(self)

    def setBvar(self):
        """setBvar(ASTNode self)"""
        return _libsedml.ASTNode_setBvar(self)

    def usesL3V2MathConstructs(self):
        """usesL3V2MathConstructs(ASTNode self) -> bool"""
        return _libsedml.ASTNode_usesL3V2MathConstructs(self)

    def usesRateOf(self):
        """usesRateOf(ASTNode self) -> bool"""
        return _libsedml.ASTNode_usesRateOf(self)

    def isQualifier(self):
        """isQualifier(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isQualifier(self)

    def isSemantics(self):
        """isSemantics(ASTNode self) -> bool"""
        return _libsedml.ASTNode_isSemantics(self)

    def getNumBvars(self):
        """getNumBvars(ASTNode self) -> unsigned int"""
        return _libsedml.ASTNode_getNumBvars(self)

    def addPlugin(self, plugin):
        """addPlugin(ASTNode self, ASTBasePlugin * plugin)"""
        return _libsedml.ASTNode_addPlugin(self, plugin)

    def loadASTPlugins(self, sbmlns):
        """loadASTPlugins(ASTNode self, SBMLNamespaces const * sbmlns)"""
        return _libsedml.ASTNode_loadASTPlugins(self, sbmlns)

    def loadASTPlugin(self, pkgName):
        """loadASTPlugin(ASTNode self, string pkgName)"""
        return _libsedml.ASTNode_loadASTPlugin(self, pkgName)

    def getASTPlugin(self, *args):
        """
        getASTPlugin(ASTNode self, SBMLNamespaces const * sbmlns) -> ASTBasePlugin
        getASTPlugin(ASTNode self, ASTNodeType_t type) -> ASTBasePlugin
        getASTPlugin(ASTNode self, string name, bool isCsymbol=False, bool strCmpIsCaseSensitive=False) -> ASTBasePlugin
        getASTPlugin(ASTNode self, SBMLNamespaces const * sbmlns) -> ASTBasePlugin const
        getASTPlugin(ASTNode self, ASTNodeType_t type) -> ASTBasePlugin const
        getASTPlugin(ASTNode self, string name, bool isCsymbol=False, bool strCmpIsCaseSensitive=False) -> ASTBasePlugin const
        """
        return _libsedml.ASTNode_getASTPlugin(self, *args)

    def getPlugin(self, *args):
        """
        getPlugin(ASTNode self, string package) -> ASTBasePlugin
        getPlugin(ASTNode self, string package) -> ASTBasePlugin const
        getPlugin(ASTNode self, unsigned int n) -> ASTBasePlugin
        getPlugin(ASTNode self, unsigned int n) -> ASTBasePlugin const *
        """
        return _libsedml.ASTNode_getPlugin(self, *args)

    def getNumPlugins(self):
        """getNumPlugins(ASTNode self) -> unsigned int"""
        return _libsedml.ASTNode_getNumPlugins(self)

    def __eq__(self, rhs):
        if self is None and rhs is None:
            return True
        else:
            if self is None or rhs is None:
                return False
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return True
            return False

    def __ne__(self, rhs):
        if self is None and rhs is None:
            return False
        else:
            if self is None or rhs is None:
                return True
            if hasattr(self, 'this') and hasattr(rhs, 'this'):
                if self.this == rhs.this:
                    return False
            return True

    def getListOfNodes(self):
        """getListOfNodes(ASTNode self) -> ASTNodeList"""
        return _libsedml.ASTNode_getListOfNodes(self)


_libsedml.ASTNode_swigregister(ASTNode)

def readMathMLFromString(xml):
    """readMathMLFromString(char const * xml) -> ASTNode"""
    return _libsedml.readMathMLFromString(xml)


def readMathMLFromStringWithNamespaces(xml, xmlns):
    """readMathMLFromStringWithNamespaces(char const * xml, XMLNamespaces_t * xmlns) -> ASTNode"""
    return _libsedml.readMathMLFromStringWithNamespaces(xml, xmlns)


def writeMathMLToString(node):
    """writeMathMLToString(ASTNode node) -> char *"""
    return _libsedml.writeMathMLToString(node)


def writeMathMLWithNamespaceToString(node, sbmlns):
    """writeMathMLWithNamespaceToString(ASTNode node, SBMLNamespaces_t * sbmlns) -> char *"""
    return _libsedml.writeMathMLWithNamespaceToString(node, sbmlns)


def parseFormula(formula):
    """parseFormula(char const * formula) -> ASTNode"""
    return _libsedml.parseFormula(formula)


def formulaToL3String(tree):
    """formulaToL3String(ASTNode tree) -> char *"""
    return _libsedml.formulaToL3String(tree)


def formulaToL3StringWithSettings(tree, settings):
    """formulaToL3StringWithSettings(ASTNode tree, L3ParserSettings_t const * settings) -> char *"""
    return _libsedml.formulaToL3StringWithSettings(tree, settings)


def formulaToString(tree):
    """formulaToString(ASTNode tree) -> char *"""
    return _libsedml.formulaToString(tree)


def parseL3Formula(formula):
    """parseL3Formula(char const * formula) -> ASTNode"""
    return _libsedml.parseL3Formula(formula)


def parseL3FormulaWithModel(formula, model):
    """parseL3FormulaWithModel(char const * formula, Model_t const * model) -> ASTNode"""
    return _libsedml.parseL3FormulaWithModel(formula, model)


def parseL3FormulaWithSettings(formula, settings):
    """parseL3FormulaWithSettings(char const * formula, L3ParserSettings_t const * settings) -> ASTNode"""
    return _libsedml.parseL3FormulaWithSettings(formula, settings)


def getDefaultL3ParserSettings():
    """getDefaultL3ParserSettings() -> L3ParserSettings_t *"""
    return _libsedml.getDefaultL3ParserSettings()


def getLastParseL3Error():
    """getLastParseL3Error() -> char *"""
    return _libsedml.getLastParseL3Error()


def SBML_deleteL3Parser():
    """SBML_deleteL3Parser()"""
    return _libsedml.SBML_deleteL3Parser()


L3P_PARSE_LOG_AS_LOG10 = _libsedml.L3P_PARSE_LOG_AS_LOG10
L3P_PARSE_LOG_AS_LN = _libsedml.L3P_PARSE_LOG_AS_LN
L3P_PARSE_LOG_AS_ERROR = _libsedml.L3P_PARSE_LOG_AS_ERROR
L3P_COLLAPSE_UNARY_MINUS = _libsedml.L3P_COLLAPSE_UNARY_MINUS
L3P_EXPAND_UNARY_MINUS = _libsedml.L3P_EXPAND_UNARY_MINUS
L3P_PARSE_UNITS = _libsedml.L3P_PARSE_UNITS
L3P_NO_UNITS = _libsedml.L3P_NO_UNITS
L3P_AVOGADRO_IS_CSYMBOL = _libsedml.L3P_AVOGADRO_IS_CSYMBOL
L3P_AVOGADRO_IS_NAME = _libsedml.L3P_AVOGADRO_IS_NAME
L3P_COMPARE_BUILTINS_CASE_INSENSITIVE = _libsedml.L3P_COMPARE_BUILTINS_CASE_INSENSITIVE
L3P_COMPARE_BUILTINS_CASE_SENSITIVE = _libsedml.L3P_COMPARE_BUILTINS_CASE_SENSITIVE
L3P_MODULO_IS_REM = _libsedml.L3P_MODULO_IS_REM
L3P_MODULO_IS_PIECEWISE = _libsedml.L3P_MODULO_IS_PIECEWISE
L3P_PARSE_L3V2_FUNCTIONS_DIRECTLY = _libsedml.L3P_PARSE_L3V2_FUNCTIONS_DIRECTLY
L3P_PARSE_L3V2_FUNCTIONS_AS_GENERIC = _libsedml.L3P_PARSE_L3V2_FUNCTIONS_AS_GENERIC
L3P_PARSE_PACKAGE_MATH_DIRECTLY = _libsedml.L3P_PARSE_PACKAGE_MATH_DIRECTLY
L3P_PARSE_PACKAGE_MATH_AS_GENERIC = _libsedml.L3P_PARSE_PACKAGE_MATH_AS_GENERIC
INFIX_SYNTAX_NAMED_SQUARE_BRACKETS = _libsedml.INFIX_SYNTAX_NAMED_SQUARE_BRACKETS
INFIX_SYNTAX_CURLY_BRACES = _libsedml.INFIX_SYNTAX_CURLY_BRACES
INFIX_SYNTAX_CURLY_BRACES_SEMICOLON = _libsedml.INFIX_SYNTAX_CURLY_BRACES_SEMICOLON

class L3ParserSettings(object):
    """Proxy of C++ L3ParserSettings class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(L3ParserSettings self) -> L3ParserSettings
        __init__(L3ParserSettings self, Model * model, ParseLogType_t parselog, bool collapseminus, bool parseunits, bool avocsymbol, bool caseSensitive=False, SBMLNamespaces * sbmlns=None, bool moduloL3v2=False, bool l3v2functions=False) -> L3ParserSettings
        __init__(L3ParserSettings self, L3ParserSettings source) -> L3ParserSettings
        """
        _libsedml.L3ParserSettings_swiginit(self, _libsedml.new_L3ParserSettings(*args))

    __swig_destroy__ = _libsedml.delete_L3ParserSettings

    def setModel(self, model):
        """setModel(L3ParserSettings self, Model const * model)"""
        return _libsedml.L3ParserSettings_setModel(self, model)

    def getModel(self):
        """getModel(L3ParserSettings self) -> Model const *"""
        return _libsedml.L3ParserSettings_getModel(self)

    def unsetModel(self):
        """unsetModel(L3ParserSettings self)"""
        return _libsedml.L3ParserSettings_unsetModel(self)

    def setParseLog(self, type):
        """setParseLog(L3ParserSettings self, ParseLogType_t type)"""
        return _libsedml.L3ParserSettings_setParseLog(self, type)

    def getParseLog(self):
        """getParseLog(L3ParserSettings self) -> ParseLogType_t"""
        return _libsedml.L3ParserSettings_getParseLog(self)

    def setParseCollapseMinus(self, collapseminus):
        """setParseCollapseMinus(L3ParserSettings self, bool collapseminus)"""
        return _libsedml.L3ParserSettings_setParseCollapseMinus(self, collapseminus)

    def getParseCollapseMinus(self):
        """getParseCollapseMinus(L3ParserSettings self) -> bool"""
        return _libsedml.L3ParserSettings_getParseCollapseMinus(self)

    def setParseUnits(self, units):
        """setParseUnits(L3ParserSettings self, bool units)"""
        return _libsedml.L3ParserSettings_setParseUnits(self, units)

    def getParseUnits(self):
        """getParseUnits(L3ParserSettings self) -> bool"""
        return _libsedml.L3ParserSettings_getParseUnits(self)

    def setParseAvogadroCsymbol(self, l2only):
        """setParseAvogadroCsymbol(L3ParserSettings self, bool l2only)"""
        return _libsedml.L3ParserSettings_setParseAvogadroCsymbol(self, l2only)

    def getParseAvogadroCsymbol(self):
        """getParseAvogadroCsymbol(L3ParserSettings self) -> bool"""
        return _libsedml.L3ParserSettings_getParseAvogadroCsymbol(self)

    def setComparisonCaseSensitivity(self, strcmp):
        """setComparisonCaseSensitivity(L3ParserSettings self, bool strcmp)"""
        return _libsedml.L3ParserSettings_setComparisonCaseSensitivity(self, strcmp)

    def getComparisonCaseSensitivity(self):
        """getComparisonCaseSensitivity(L3ParserSettings self) -> bool"""
        return _libsedml.L3ParserSettings_getComparisonCaseSensitivity(self)

    def setParseModuloL3v2(self, modulol3v2):
        """setParseModuloL3v2(L3ParserSettings self, bool modulol3v2)"""
        return _libsedml.L3ParserSettings_setParseModuloL3v2(self, modulol3v2)

    def getParseModuloL3v2(self):
        """getParseModuloL3v2(L3ParserSettings self) -> bool"""
        return _libsedml.L3ParserSettings_getParseModuloL3v2(self)

    def setParseL3v2Functions(self, l3v2functions):
        """setParseL3v2Functions(L3ParserSettings self, bool l3v2functions)"""
        return _libsedml.L3ParserSettings_setParseL3v2Functions(self, l3v2functions)

    def getParseL3v2Functions(self):
        """getParseL3v2Functions(L3ParserSettings self) -> bool"""
        return _libsedml.L3ParserSettings_getParseL3v2Functions(self)

    def setParsePackageMath(self, package, parsepackage):
        """setParsePackageMath(L3ParserSettings self, ExtendedMathType_t package, bool parsepackage)"""
        return _libsedml.L3ParserSettings_setParsePackageMath(self, package, parsepackage)

    def getParsePackageMath(self, package):
        """getParsePackageMath(L3ParserSettings self, ExtendedMathType_t package) -> bool"""
        return _libsedml.L3ParserSettings_getParsePackageMath(self, package)

    def visitPackageInfixSyntax(self, parent, node, sb):
        """visitPackageInfixSyntax(L3ParserSettings self, ASTNode parent, ASTNode node, StringBuffer_t * sb)"""
        return _libsedml.L3ParserSettings_visitPackageInfixSyntax(self, parent, node, sb)


_libsedml.L3ParserSettings_swigregister(L3ParserSettings)
LIBNUML_NAMESPACE_H = _libsedml.LIBNUML_NAMESPACE_H
LIBNUML_DOTTED_VERSION = _libsedml.LIBNUML_DOTTED_VERSION
LIBNUML_VERSION = _libsedml.LIBNUML_VERSION
LIBNUML_VERSION_STRING = _libsedml.LIBNUML_VERSION_STRING

def getLibNUMLVersion():
    """getLibNUMLVersion() -> int"""
    return _libsedml.getLibNUMLVersion()


def getLibNUMLDottedVersion():
    """getLibNUMLDottedVersion() -> char const *"""
    return _libsedml.getLibNUMLDottedVersion()


def getLibNUMLVersionString():
    """getLibNUMLVersionString() -> char const *"""
    return _libsedml.getLibNUMLVersionString()


LIBNUML_OPERATION_RETURN_VALUES_H = _libsedml.LIBNUML_OPERATION_RETURN_VALUES_H
LIBNUML_OPERATION_SUCCESS = _libsedml.LIBNUML_OPERATION_SUCCESS
LIBNUML_INDEX_EXCEEDS_SIZE = _libsedml.LIBNUML_INDEX_EXCEEDS_SIZE
LIBNUML_UNEXPECTED_ATTRIBUTE = _libsedml.LIBNUML_UNEXPECTED_ATTRIBUTE
LIBNUML_OPERATION_FAILED = _libsedml.LIBNUML_OPERATION_FAILED
LIBNUML_INVALID_ATTRIBUTE_VALUE = _libsedml.LIBNUML_INVALID_ATTRIBUTE_VALUE
LIBNUML_INVALID_OBJECT = _libsedml.LIBNUML_INVALID_OBJECT
LIBNUML_DUPLICATE_OBJECT_ID = _libsedml.LIBNUML_DUPLICATE_OBJECT_ID
LIBNUML_LEVEL_MISMATCH = _libsedml.LIBNUML_LEVEL_MISMATCH
LIBNUML_VERSION_MISMATCH = _libsedml.LIBNUML_VERSION_MISMATCH
LIBNUML_INVALID_XML_OPERATION = _libsedml.LIBNUML_INVALID_XML_OPERATION
LIBNUML_DUPLICATE_ANNOTATION_NS = _libsedml.LIBNUML_DUPLICATE_ANNOTATION_NS
LIBNUML_ANNOTATION_NAME_NOT_FOUND = _libsedml.LIBNUML_ANNOTATION_NAME_NOT_FOUND
LIBNUML_ANNOTATION_NS_NOT_FOUND = _libsedml.LIBNUML_ANNOTATION_NS_NOT_FOUND

class NUMLNamespaces(object):
    """Proxy of C++ NUMLNamespaces class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_NUMLNamespaces

    def __init__(self, *args):
        """
        __init__(NUMLNamespaces self, unsigned int level=NUML_DEFAULT_LEVEL, unsigned int version=NUML_DEFAULT_VERSION) -> NUMLNamespaces
        __init__(NUMLNamespaces self, NUMLNamespaces orig) -> NUMLNamespaces
        """
        _libsedml.NUMLNamespaces_swiginit(self, _libsedml.new_NUMLNamespaces(*args))

    def clone(self):
        """clone(NUMLNamespaces self) -> NUMLNamespaces"""
        return _libsedml.NUMLNamespaces_clone(self)

    @staticmethod
    def getNUMLNamespaceURI(level, version):
        """getNUMLNamespaceURI(unsigned int level, unsigned int version) -> string"""
        return _libsedml.NUMLNamespaces_getNUMLNamespaceURI(level, version)

    def getLevel(self):
        """getLevel(NUMLNamespaces self) -> unsigned int"""
        return _libsedml.NUMLNamespaces_getLevel(self)

    def getVersion(self):
        """getVersion(NUMLNamespaces self) -> unsigned int"""
        return _libsedml.NUMLNamespaces_getVersion(self)

    def getNamespaces(self):
        """getNamespaces(NUMLNamespaces self) -> XMLNamespaces"""
        return _libsedml.NUMLNamespaces_getNamespaces(self)

    def addNamespaces(self, xmlns):
        """addNamespaces(NUMLNamespaces self, XMLNamespaces xmlns)"""
        return _libsedml.NUMLNamespaces_addNamespaces(self, xmlns)

    def setLevel(self, level):
        """setLevel(NUMLNamespaces self, unsigned int level)"""
        return _libsedml.NUMLNamespaces_setLevel(self, level)

    def setVersion(self, version):
        """setVersion(NUMLNamespaces self, unsigned int version)"""
        return _libsedml.NUMLNamespaces_setVersion(self, version)

    def setNamespaces(self, xmlns):
        """setNamespaces(NUMLNamespaces self, XMLNamespaces xmlns)"""
        return _libsedml.NUMLNamespaces_setNamespaces(self, xmlns)


_libsedml.NUMLNamespaces_swigregister(NUMLNamespaces)
NUML_DEFAULT_LEVEL = cvar.NUML_DEFAULT_LEVEL
NUML_DEFAULT_VERSION = cvar.NUML_DEFAULT_VERSION
NUML_XMLNS_L1 = cvar.NUML_XMLNS_L1
NUML_XMLNS_L1V1 = cvar.NUML_XMLNS_L1V1

def NUMLNamespaces_getNUMLNamespaceURI(level, version):
    """NUMLNamespaces_getNUMLNamespaceURI(unsigned int level, unsigned int version) -> string"""
    return _libsedml.NUMLNamespaces_getNUMLNamespaceURI(level, version)


NUML_UNKNOWN = _libsedml.NUML_UNKNOWN
NUML_DOCUMENT = _libsedml.NUML_DOCUMENT
NUML_ONTOLOGYTERMS = _libsedml.NUML_ONTOLOGYTERMS
NUML_ONTOLOGYTERM = _libsedml.NUML_ONTOLOGYTERM
NUML_RESULTCOMPONENT = _libsedml.NUML_RESULTCOMPONENT
NUML_RESULTCOMPONENTS = _libsedml.NUML_RESULTCOMPONENTS
NUML_DIMENSION = _libsedml.NUML_DIMENSION
NUML_DIMENSIONDESCRIPTION = _libsedml.NUML_DIMENSIONDESCRIPTION
NUML_COMPOSITEVALUE = _libsedml.NUML_COMPOSITEVALUE
NUML_COMPOSITEVALUES = _libsedml.NUML_COMPOSITEVALUES
NUML_TUPLE = _libsedml.NUML_TUPLE
NUML_TUPLES = _libsedml.NUML_TUPLES
NUML_ATOMICVALUE = _libsedml.NUML_ATOMICVALUE
NUML_ATOMICVALUES = _libsedml.NUML_ATOMICVALUES
NUML_COMPOSITEDESCRIPTION = _libsedml.NUML_COMPOSITEDESCRIPTION
NUML_TUPLEDESCRIPTION = _libsedml.NUML_TUPLEDESCRIPTION
NUML_ATOMICDESCRIPTION = _libsedml.NUML_ATOMICDESCRIPTION
NUML_NUMLLIST = _libsedml.NUML_NUMLLIST

def NUMLTypeCode_toString(tc):
    """NUMLTypeCode_toString(NUMLTypeCode_t tc) -> char const *"""
    return _libsedml.NUMLTypeCode_toString(tc)


NUMLUnknownError = _libsedml.NUMLUnknownError
NUMLNotUTF8 = _libsedml.NUMLNotUTF8
NUMLUnrecognizedElement = _libsedml.NUMLUnrecognizedElement
NUMLNotSchemaConformant = _libsedml.NUMLNotSchemaConformant
NUMLInvalidMathElement = _libsedml.NUMLInvalidMathElement
NUMLMultipleAssignmentOrRateRules = _libsedml.NUMLMultipleAssignmentOrRateRules
NUMLMultipleEventAssignmentsForId = _libsedml.NUMLMultipleEventAssignmentsForId
NUMLEventAndAssignmentRuleForId = _libsedml.NUMLEventAndAssignmentRuleForId
NUMLDuplicateMetaId = _libsedml.NUMLDuplicateMetaId
NUMLInvalidSBOTermSyntax = _libsedml.NUMLInvalidSBOTermSyntax
NUMLInvalidMetaidSyntax = _libsedml.NUMLInvalidMetaidSyntax
NUMLInvalidIdSyntax = _libsedml.NUMLInvalidIdSyntax
NUMLInvalidUnitIdSyntax = _libsedml.NUMLInvalidUnitIdSyntax
NUMLMissingAnnotationNamespace = _libsedml.NUMLMissingAnnotationNamespace
NUMLDuplicateAnnotationNamespaces = _libsedml.NUMLDuplicateAnnotationNamespaces
NUMLNamespaceInAnnotation = _libsedml.NUMLNamespaceInAnnotation
NUMLMissingOntologyTerms = _libsedml.NUMLMissingOntologyTerms
NUMLMissingResultComponents = _libsedml.NUMLMissingResultComponents
NUMLInconsistentArgUnits = _libsedml.NUMLInconsistentArgUnits
NUMLAssignRuleCompartmentMismatch = _libsedml.NUMLAssignRuleCompartmentMismatch
NUMLOverdeterminedSystem = _libsedml.NUMLOverdeterminedSystem
NUMLInvalidModelSBOTerm = _libsedml.NUMLInvalidModelSBOTerm
NUMLInvalidFunctionDefSBOTerm = _libsedml.NUMLInvalidFunctionDefSBOTerm
NUMLInvalidRuleSBOTerm = _libsedml.NUMLInvalidRuleSBOTerm
NUMLInvalidConstraintSBOTerm = _libsedml.NUMLInvalidConstraintSBOTerm
NUMLNotesNotInXHTMLNamespace = _libsedml.NUMLNotesNotInXHTMLNamespace
NUMLNotesContainsXMLDecl = _libsedml.NUMLNotesContainsXMLDecl
NUMLNotesContainsDOCTYPE = _libsedml.NUMLNotesContainsDOCTYPE
NUMLInvalidNotesContent = _libsedml.NUMLInvalidNotesContent
NUMLInvalidNamespaceOnNUML = _libsedml.NUMLInvalidNamespaceOnNUML
NUMLMissingOrInconsistentLevel = _libsedml.NUMLMissingOrInconsistentLevel
NUMLMissingOrInconsistentVersion = _libsedml.NUMLMissingOrInconsistentVersion
NUMLAnnotationNotesNotAllowedLevel1 = _libsedml.NUMLAnnotationNotesNotAllowedLevel1
NUMLMissingModel = _libsedml.NUMLMissingModel
NUMLIncorrectOrderInModel = _libsedml.NUMLIncorrectOrderInModel
NUMLEmptyListElement = _libsedml.NUMLEmptyListElement
NUMLNeedCompartmentIfHaveSpecies = _libsedml.NUMLNeedCompartmentIfHaveSpecies
NUMLFunctionDefMathNotLambda = _libsedml.NUMLFunctionDefMathNotLambda
NUMLInvalidApplyCiInLambda = _libsedml.NUMLInvalidApplyCiInLambda
NUMLConstraintNotInXHTMLNamespace = _libsedml.NUMLConstraintNotInXHTMLNamespace
NUMLConstraintContainsXMLDecl = _libsedml.NUMLConstraintContainsXMLDecl
NUMLConstraintContainsDOCTYPE = _libsedml.NUMLConstraintContainsDOCTYPE
NUMLInvalidConstraintContent = _libsedml.NUMLInvalidConstraintContent
NUMLEventAssignmentForConstantEntity = _libsedml.NUMLEventAssignmentForConstantEntity
NUMLGeneralWarningNotSpecified = _libsedml.NUMLGeneralWarningNotSpecified
LibNUMLAdditionalCodesLowerBound = _libsedml.LibNUMLAdditionalCodesLowerBound
NUMLCannotConvertToL1V1 = _libsedml.NUMLCannotConvertToL1V1
NUMLNoEventsInL1 = _libsedml.NUMLNoEventsInL1
NUMLStrictUnitsRequiredInL1 = _libsedml.NUMLStrictUnitsRequiredInL1
NUMLNoConstraintsInL2v1 = _libsedml.NUMLNoConstraintsInL2v1
NUMLStrictUnitsRequiredInL2v1 = _libsedml.NUMLStrictUnitsRequiredInL2v1
InvalidNUMLLevelVersion = _libsedml.InvalidNUMLLevelVersion
NUMLInvalidRuleOrdering = _libsedml.NUMLInvalidRuleOrdering
NUMLNoTimeSymbolInFunctionDef = _libsedml.NUMLNoTimeSymbolInFunctionDef
NUMLUnrecognisedSBOTerm = _libsedml.NUMLUnrecognisedSBOTerm
NUMLObseleteSBOTerm = _libsedml.NUMLObseleteSBOTerm
NUMLOffsetNotValidAttribute = _libsedml.NUMLOffsetNotValidAttribute
NUMLCodesUpperBound = _libsedml.NUMLCodesUpperBound
LIBNUML_CAT_INTERNAL = _libsedml.LIBNUML_CAT_INTERNAL
LIBNUML_CAT_NUML = _libsedml.LIBNUML_CAT_NUML
LIBNUML_CAT_NUML_L1_COMPAT = _libsedml.LIBNUML_CAT_NUML_L1_COMPAT
LIBNUML_CAT_NUML_L1V1_COMPAT = _libsedml.LIBNUML_CAT_NUML_L1V1_COMPAT
LIBNUML_CAT_GENERAL_CONSISTENCY = _libsedml.LIBNUML_CAT_GENERAL_CONSISTENCY
LIBNUML_CAT_IDENTIFIER_CONSISTENCY = _libsedml.LIBNUML_CAT_IDENTIFIER_CONSISTENCY
LIBNUML_CAT_INTERNAL_CONSISTENCY = _libsedml.LIBNUML_CAT_INTERNAL_CONSISTENCY
LIBNUML_SEV_ERROR = _libsedml.LIBNUML_SEV_ERROR
LIBNUML_SEV_FATAL = _libsedml.LIBNUML_SEV_FATAL
LIBNUML_SEV_WARNING = _libsedml.LIBNUML_SEV_WARNING
LIBNUML_SEV_SCHEMA_ERROR = _libsedml.LIBNUML_SEV_SCHEMA_ERROR
LIBNUML_SEV_GENERAL_WARNING = _libsedml.LIBNUML_SEV_GENERAL_WARNING
LIBNUML_SEV_NOT_APPLICABLE = _libsedml.LIBNUML_SEV_NOT_APPLICABLE

class NUMLError(XMLError):
    """Proxy of C++ NUMLError class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(NUMLError self, unsigned int const errorId=0, unsigned int const level=NUML_DEFAULT_LEVEL, unsigned int const version=NUML_DEFAULT_VERSION, string details="", unsigned int const line=0, unsigned int const column=0, unsigned int const severity=LIBNUML_SEV_ERROR, unsigned int const category=LIBNUML_CAT_NUML) -> NUMLError
        __init__(NUMLError self, NUMLError orig) -> NUMLError
        """
        _libsedml.NUMLError_swiginit(self, _libsedml.new_NUMLError(*args))

    def clone(self):
        """clone(NUMLError self) -> NUMLError"""
        return _libsedml.NUMLError_clone(self)

    __swig_destroy__ = _libsedml.delete_NUMLError


_libsedml.NUMLError_swigregister(NUMLError)

class NUMLErrorLog(XMLErrorLog):
    """Proxy of C++ NUMLErrorLog class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getError(self, n):
        """getError(NUMLErrorLog self, unsigned int n) -> NUMLError"""
        return _libsedml.NUMLErrorLog_getError(self, n)

    def getNumFailsWithSeverity(self, severity):
        """getNumFailsWithSeverity(NUMLErrorLog self, unsigned int severity) -> unsigned int"""
        return _libsedml.NUMLErrorLog_getNumFailsWithSeverity(self, severity)

    def __init__(self):
        """__init__(NUMLErrorLog self) -> NUMLErrorLog"""
        _libsedml.NUMLErrorLog_swiginit(self, _libsedml.new_NUMLErrorLog())

    __swig_destroy__ = _libsedml.delete_NUMLErrorLog

    def logError(self, *args):
        """logError(NUMLErrorLog self, unsigned int const errorId=0, unsigned int const level=NUML_DEFAULT_LEVEL, unsigned int const version=NUML_DEFAULT_VERSION, string details="", unsigned int const line=0, unsigned int const column=0, unsigned int const severity=LIBNUML_SEV_ERROR, unsigned int const category=LIBNUML_CAT_NUML)"""
        return _libsedml.NUMLErrorLog_logError(self, *args)

    def add(self, *args):
        """
        add(NUMLErrorLog self, NUMLError error)
        add(NUMLErrorLog self, std::list< NUMLError > const & errors)
        """
        return _libsedml.NUMLErrorLog_add(self, *args)

    def remove(self, errorId):
        """remove(NUMLErrorLog self, unsigned int const errorId)"""
        return _libsedml.NUMLErrorLog_remove(self, errorId)


_libsedml.NUMLErrorLog_swigregister(NUMLErrorLog)

class NUMLReader(object):
    """Proxy of C++ NUMLReader class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        """__init__(NUMLReader self) -> NUMLReader"""
        _libsedml.NUMLReader_swiginit(self, _libsedml.new_NUMLReader())

    __swig_destroy__ = _libsedml.delete_NUMLReader

    def readNUML(self, filename):
        """readNUML(NUMLReader self, string filename) -> NUMLDocument"""
        return _libsedml.NUMLReader_readNUML(self, filename)

    def readNUMLFromFile(self, filename):
        """readNUMLFromFile(NUMLReader self, string filename) -> NUMLDocument"""
        return _libsedml.NUMLReader_readNUMLFromFile(self, filename)

    def readNUMLFromString(self, xml):
        """readNUMLFromString(NUMLReader self, string xml) -> NUMLDocument"""
        return _libsedml.NUMLReader_readNUMLFromString(self, xml)

    @staticmethod
    def hasZlib():
        """hasZlib() -> bool"""
        return _libsedml.NUMLReader_hasZlib()

    @staticmethod
    def hasBzip2():
        """hasBzip2() -> bool"""
        return _libsedml.NUMLReader_hasBzip2()


_libsedml.NUMLReader_swigregister(NUMLReader)

def NUMLReader_hasZlib():
    """NUMLReader_hasZlib() -> bool"""
    return _libsedml.NUMLReader_hasZlib()


def NUMLReader_hasBzip2():
    """NUMLReader_hasBzip2() -> bool"""
    return _libsedml.NUMLReader_hasBzip2()


def readNUML(filename):
    """readNUML(char const * filename) -> NUMLDocument_t *"""
    return _libsedml.readNUML(filename)


def readNUMLFromFile(filename):
    """readNUMLFromFile(char const * filename) -> NUMLDocument_t *"""
    return _libsedml.readNUMLFromFile(filename)


def readNUMLFromString(xml):
    """readNUMLFromString(char const * xml) -> NUMLDocument_t *"""
    return _libsedml.readNUMLFromString(xml)


class NUMLWriter(object):
    """Proxy of C++ NUMLWriter class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        """__init__(NUMLWriter self) -> NUMLWriter"""
        _libsedml.NUMLWriter_swiginit(self, _libsedml.new_NUMLWriter())

    __swig_destroy__ = _libsedml.delete_NUMLWriter

    def setProgramName(self, name):
        """setProgramName(NUMLWriter self, string name) -> int"""
        return _libsedml.NUMLWriter_setProgramName(self, name)

    def setProgramVersion(self, version):
        """setProgramVersion(NUMLWriter self, string version) -> int"""
        return _libsedml.NUMLWriter_setProgramVersion(self, version)

    def writeNUML(self, *args):
        """
        writeNUML(NUMLWriter self, NUMLDocument d, string filename) -> bool
        writeNUML(NUMLWriter self, NUMLDocument d, ostream stream) -> bool
        """
        return _libsedml.NUMLWriter_writeNUML(self, *args)

    def writeToString(self, d):
        """writeToString(NUMLWriter self, NUMLDocument d) -> char *"""
        return _libsedml.NUMLWriter_writeToString(self, d)

    @staticmethod
    def hasZlib():
        """hasZlib() -> bool"""
        return _libsedml.NUMLWriter_hasZlib()

    @staticmethod
    def hasBzip2():
        """hasBzip2() -> bool"""
        return _libsedml.NUMLWriter_hasBzip2()


_libsedml.NUMLWriter_swigregister(NUMLWriter)

def NUMLWriter_hasZlib():
    """NUMLWriter_hasZlib() -> bool"""
    return _libsedml.NUMLWriter_hasZlib()


def NUMLWriter_hasBzip2():
    """NUMLWriter_hasBzip2() -> bool"""
    return _libsedml.NUMLWriter_hasBzip2()


def writeNUML(d, filename):
    """writeNUML(NUMLDocument_t const * d, char const * filename) -> int"""
    return _libsedml.writeNUML(d, filename)


def writeNUMLToString(d):
    """writeNUMLToString(NUMLDocument_t const * d) -> char *"""
    return _libsedml.writeNUMLToString(d)


class NUMLConstructorException(object):
    """Proxy of C++ NUMLConstructorException class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        """__init__(NUMLConstructorException self) -> NUMLConstructorException"""
        _libsedml.NUMLConstructorException_swiginit(self, _libsedml.new_NUMLConstructorException())

    __swig_destroy__ = _libsedml.delete_NUMLConstructorException


_libsedml.NUMLConstructorException_swigregister(NUMLConstructorException)

class NMBase(object):
    """Proxy of C++ NMBase class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined - class is abstract')

    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_NMBase

    def clone(self):
        """clone(NMBase self) -> NMBase"""
        return _libsedml.NMBase_clone(self)

    def getMetaId(self, *args):
        """
        getMetaId(NMBase self) -> string
        getMetaId(NMBase self) -> string
        """
        return _libsedml.NMBase_getMetaId(self, *args)

    def getId(self):
        """getId(NMBase self) -> string"""
        return _libsedml.NMBase_getId(self)

    def getName(self):
        """getName(NMBase self) -> string"""
        return _libsedml.NMBase_getName(self)

    def getNamespaces(self):
        """getNamespaces(NMBase self) -> XMLNamespaces"""
        return _libsedml.NMBase_getNamespaces(self)

    def getNUMLDocument(self, *args):
        """
        getNUMLDocument(NMBase self) -> NUMLDocument
        getNUMLDocument(NMBase self) -> NUMLDocument
        """
        return _libsedml.NMBase_getNUMLDocument(self, *args)

    def getParentNUMLObject(self):
        """getParentNUMLObject(NMBase self) -> NMBase"""
        return _libsedml.NMBase_getParentNUMLObject(self)

    def getAncestorOfType(self, type):
        """getAncestorOfType(NMBase self, NUMLTypeCode_t type) -> NMBase"""
        return _libsedml.NMBase_getAncestorOfType(self, type)

    def getLine(self):
        """getLine(NMBase self) -> unsigned int"""
        return _libsedml.NMBase_getLine(self)

    def getColumn(self):
        """getColumn(NMBase self) -> unsigned int"""
        return _libsedml.NMBase_getColumn(self)

    def isSetMetaId(self):
        """isSetMetaId(NMBase self) -> bool"""
        return _libsedml.NMBase_isSetMetaId(self)

    def isSetName(self):
        """isSetName(NMBase self) -> bool"""
        return _libsedml.NMBase_isSetName(self)

    def setMetaId(self, metaid):
        """setMetaId(NMBase self, string metaid) -> int"""
        return _libsedml.NMBase_setMetaId(self, metaid)

    def setId(self, sid):
        """setId(NMBase self, string sid) -> int"""
        return _libsedml.NMBase_setId(self, sid)

    def setNUMLDocument(self, d):
        """setNUMLDocument(NMBase self, NUMLDocument d)"""
        return _libsedml.NMBase_setNUMLDocument(self, d)

    def setParentNUMLObject(self, sb):
        """setParentNUMLObject(NMBase self, NMBase sb)"""
        return _libsedml.NMBase_setParentNUMLObject(self, sb)

    def setNamespaces(self, xmlns):
        """setNamespaces(NMBase self, XMLNamespaces xmlns) -> int"""
        return _libsedml.NMBase_setNamespaces(self, xmlns)

    def unsetMetaId(self):
        """unsetMetaId(NMBase self) -> int"""
        return _libsedml.NMBase_unsetMetaId(self)

    def getLevel(self):
        """getLevel(NMBase self) -> unsigned int"""
        return _libsedml.NMBase_getLevel(self)

    def getVersion(self):
        """getVersion(NMBase self) -> unsigned int"""
        return _libsedml.NMBase_getVersion(self)

    def getTypeCode(self):
        """getTypeCode(NMBase self) -> NUMLTypeCode_t"""
        return _libsedml.NMBase_getTypeCode(self)

    def hasValidLevelVersionNamespaceCombination(self):
        """hasValidLevelVersionNamespaceCombination(NMBase self) -> bool"""
        return _libsedml.NMBase_hasValidLevelVersionNamespaceCombination(self)

    def getElementName(self):
        """getElementName(NMBase self) -> string"""
        return _libsedml.NMBase_getElementName(self)

    def toNUML(self):
        """toNUML(NMBase self) -> char *"""
        return _libsedml.NMBase_toNUML(self)

    def read(self, stream):
        """read(NMBase self, XMLInputStream stream)"""
        return _libsedml.NMBase_read(self, stream)

    def write(self, stream):
        """write(NMBase self, XMLOutputStream stream)"""
        return _libsedml.NMBase_write(self, stream)

    def hasRequiredAttributes(self):
        """hasRequiredAttributes(NMBase self) -> bool"""
        return _libsedml.NMBase_hasRequiredAttributes(self)

    def hasRequiredElements(self):
        """hasRequiredElements(NMBase self) -> bool"""
        return _libsedml.NMBase_hasRequiredElements(self)

    def setNUMLNamespaces(self, numlns):
        """setNUMLNamespaces(NMBase self, NUMLNamespaces numlns)"""
        return _libsedml.NMBase_setNUMLNamespaces(self, numlns)

    def getNUMLNamespaces(self):
        """getNUMLNamespaces(NMBase self) -> NUMLNamespaces"""
        return _libsedml.NMBase_getNUMLNamespaces(self)

    def syncAnnotation(self):
        """syncAnnotation(NMBase self)"""
        return _libsedml.NMBase_syncAnnotation(self)

    def isSetNotes(self):
        """isSetNotes(NMBase self) -> bool"""
        return _libsedml.NMBase_isSetNotes(self)

    def isSetAnnotation(self):
        """isSetAnnotation(NMBase self) -> bool"""
        return _libsedml.NMBase_isSetAnnotation(self)

    def setAnnotation(self, *args):
        """
        setAnnotation(NMBase self, XMLNode annotation) -> int
        setAnnotation(NMBase self, string annotation) -> int
        """
        return _libsedml.NMBase_setAnnotation(self, *args)

    def appendAnnotation(self, *args):
        """
        appendAnnotation(NMBase self, XMLNode annotation) -> int
        appendAnnotation(NMBase self, string annotation) -> int
        """
        return _libsedml.NMBase_appendAnnotation(self, *args)

    def removeTopLevelAnnotationElement(self, *args):
        """removeTopLevelAnnotationElement(NMBase self, string elementName, string elementURI="") -> int"""
        return _libsedml.NMBase_removeTopLevelAnnotationElement(self, *args)

    def replaceTopLevelAnnotationElement(self, *args):
        """
        replaceTopLevelAnnotationElement(NMBase self, XMLNode annotation) -> int
        replaceTopLevelAnnotationElement(NMBase self, string annotation) -> int
        """
        return _libsedml.NMBase_replaceTopLevelAnnotationElement(self, *args)

    def setNotes(self, *args):
        """
        setNotes(NMBase self, XMLNode notes) -> int
        setNotes(NMBase self, string notes, bool addXHTMLMarkup=False) -> int
        """
        return _libsedml.NMBase_setNotes(self, *args)

    def appendNotes(self, *args):
        """
        appendNotes(NMBase self, XMLNode notes) -> int
        appendNotes(NMBase self, string notes) -> int
        """
        return _libsedml.NMBase_appendNotes(self, *args)

    def unsetNotes(self):
        """unsetNotes(NMBase self) -> int"""
        return _libsedml.NMBase_unsetNotes(self)

    def unsetAnnotation(self):
        """unsetAnnotation(NMBase self) -> int"""
        return _libsedml.NMBase_unsetAnnotation(self)

    def getNotes(self):
        """getNotes(NMBase self) -> XMLNode"""
        return _libsedml.NMBase_getNotes(self)

    def getNotesString(self):
        """getNotesString(NMBase self) -> string"""
        return _libsedml.NMBase_getNotesString(self)

    def getAnnotation(self):
        """getAnnotation(NMBase self) -> XMLNode"""
        return _libsedml.NMBase_getAnnotation(self)

    def getAnnotationString(self):
        """getAnnotationString(NMBase self) -> string"""
        return _libsedml.NMBase_getAnnotationString(self)


_libsedml.NMBase_swigregister(NMBase)

class NUMLList(NMBase):
    """Proxy of C++ NUMLList class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_NUMLList

    def __init__(self, *args):
        """
        __init__(NUMLList self, unsigned int level, unsigned int version) -> NUMLList
        __init__(NUMLList self, NUMLNamespaces numlns) -> NUMLList
        __init__(NUMLList self) -> NUMLList
        __init__(NUMLList self, NUMLList orig) -> NUMLList
        """
        _libsedml.NUMLList_swiginit(self, _libsedml.new_NUMLList(*args))

    def clone(self):
        """clone(NUMLList self) -> NMBase"""
        return _libsedml.NUMLList_clone(self)

    def append(self, item):
        """append(NUMLList self, NMBase item)"""
        return _libsedml.NUMLList_append(self, item)

    def appendAndOwn(self, item):
        """appendAndOwn(NUMLList self, NMBase item)"""
        return _libsedml.NUMLList_appendAndOwn(self, item)

    def get(self, *args):
        """
        get(NUMLList self, unsigned int n) -> NMBase
        get(NUMLList self, unsigned int n) -> NMBase
        """
        return _libsedml.NUMLList_get(self, *args)

    def clear(self, doDelete=True):
        """clear(NUMLList self, bool doDelete=True)"""
        return _libsedml.NUMLList_clear(self, doDelete)

    def remove(self, n):
        """remove(NUMLList self, unsigned int n) -> NMBase"""
        return _libsedml.NUMLList_remove(self, n)

    def size(self):
        """size(NUMLList self) -> unsigned int"""
        return _libsedml.NUMLList_size(self)

    def setNUMLDocument(self, d):
        """setNUMLDocument(NUMLList self, NUMLDocument d)"""
        return _libsedml.NUMLList_setNUMLDocument(self, d)

    def setParentNUMLObject(self, sb):
        """setParentNUMLObject(NUMLList self, NMBase sb)"""
        return _libsedml.NUMLList_setParentNUMLObject(self, sb)

    def getTypeCode(self):
        """getTypeCode(NUMLList self) -> NUMLTypeCode_t"""
        return _libsedml.NUMLList_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(NUMLList self) -> NUMLTypeCode_t"""
        return _libsedml.NUMLList_getItemTypeCode(self)

    def getElementName(self):
        """getElementName(NUMLList self) -> string"""
        return _libsedml.NUMLList_getElementName(self)


_libsedml.NUMLList_swigregister(NUMLList)

class OntologyTerm(NMBase):
    """Proxy of C++ OntologyTerm class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(OntologyTerm self, unsigned int level, unsigned int version) -> OntologyTerm
        __init__(OntologyTerm self, NUMLNamespaces numlns) -> OntologyTerm
        """
        _libsedml.OntologyTerm_swiginit(self, _libsedml.new_OntologyTerm(*args))

    def clone(self):
        """clone(OntologyTerm self) -> OntologyTerm"""
        return _libsedml.OntologyTerm_clone(self)

    def getId(self):
        """getId(OntologyTerm self) -> string"""
        return _libsedml.OntologyTerm_getId(self)

    def getTerm(self):
        """getTerm(OntologyTerm self) -> string"""
        return _libsedml.OntologyTerm_getTerm(self)

    def getSourceTermId(self):
        """getSourceTermId(OntologyTerm self) -> string"""
        return _libsedml.OntologyTerm_getSourceTermId(self)

    def getOntologyURI(self):
        """getOntologyURI(OntologyTerm self) -> string"""
        return _libsedml.OntologyTerm_getOntologyURI(self)

    __swig_destroy__ = _libsedml.delete_OntologyTerm

    def setId(self, sid):
        """setId(OntologyTerm self, string sid) -> int"""
        return _libsedml.OntologyTerm_setId(self, sid)

    def setTerm(self, term):
        """setTerm(OntologyTerm self, string term) -> int"""
        return _libsedml.OntologyTerm_setTerm(self, term)

    def setSourceTermId(self, sourceTermId):
        """setSourceTermId(OntologyTerm self, string sourceTermId) -> int"""
        return _libsedml.OntologyTerm_setSourceTermId(self, sourceTermId)

    def setOntologyURI(self, ontologyURI):
        """setOntologyURI(OntologyTerm self, string ontologyURI) -> int"""
        return _libsedml.OntologyTerm_setOntologyURI(self, ontologyURI)

    def getTypeCode(self):
        """getTypeCode(OntologyTerm self) -> NUMLTypeCode_t"""
        return _libsedml.OntologyTerm_getTypeCode(self)

    def getElementName(self):
        """getElementName(OntologyTerm self) -> string"""
        return _libsedml.OntologyTerm_getElementName(self)

    def readAttributes(self, attributes):
        """readAttributes(OntologyTerm self, XMLAttributes attributes)"""
        return _libsedml.OntologyTerm_readAttributes(self, attributes)

    def writeAttributes(self, stream):
        """writeAttributes(OntologyTerm self, XMLOutputStream stream)"""
        return _libsedml.OntologyTerm_writeAttributes(self, stream)


_libsedml.OntologyTerm_swigregister(OntologyTerm)

class ONTOLOGY(object):
    """Proxy of C++ ONTOLOGY class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    term = property(_libsedml.ONTOLOGY_term_get, _libsedml.ONTOLOGY_term_set, doc='term : std::string')
    sourceTermId = property(_libsedml.ONTOLOGY_sourceTermId_get, _libsedml.ONTOLOGY_sourceTermId_set, doc='sourceTermId : std::string')
    ontologyURI = property(_libsedml.ONTOLOGY_ontologyURI_get, _libsedml.ONTOLOGY_ontologyURI_set, doc='ontologyURI : std::string')

    def __init__(self):
        """__init__(ONTOLOGY self) -> ONTOLOGY"""
        _libsedml.ONTOLOGY_swiginit(self, _libsedml.new_ONTOLOGY())

    __swig_destroy__ = _libsedml.delete_ONTOLOGY


_libsedml.ONTOLOGY_swigregister(ONTOLOGY)

class OntologyTerms(NUMLList):
    """Proxy of C++ OntologyTerms class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def clone(self):
        """clone(OntologyTerms self) -> OntologyTerms"""
        return _libsedml.OntologyTerms_clone(self)

    def getTypeCode(self):
        """getTypeCode(OntologyTerms self) -> NUMLTypeCode_t"""
        return _libsedml.OntologyTerms_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(OntologyTerms self) -> NUMLTypeCode_t"""
        return _libsedml.OntologyTerms_getItemTypeCode(self)

    def getElementName(self):
        """getElementName(OntologyTerms self) -> string"""
        return _libsedml.OntologyTerms_getElementName(self)

    def get(self, *args):
        """
        get(OntologyTerms self, unsigned int n) -> OntologyTerm
        get(OntologyTerms self, unsigned int n) -> OntologyTerm
        get(OntologyTerms self, string sid) -> OntologyTerm
        get(OntologyTerms self, string sid) -> OntologyTerm
        """
        return _libsedml.OntologyTerms_get(self, *args)

    def remove(self, *args):
        """
        remove(OntologyTerms self, unsigned int n) -> OntologyTerm
        remove(OntologyTerms self, string sid) -> OntologyTerm
        """
        return _libsedml.OntologyTerms_remove(self, *args)

    def getElementPosition(self):
        """getElementPosition(OntologyTerms self) -> int"""
        return _libsedml.OntologyTerms_getElementPosition(self)

    def __init__(self):
        """__init__(OntologyTerms self) -> OntologyTerms"""
        _libsedml.OntologyTerms_swiginit(self, _libsedml.new_OntologyTerms())

    __swig_destroy__ = _libsedml.delete_OntologyTerms


_libsedml.OntologyTerms_swigregister(OntologyTerms)
IdCheckON = _libsedml.IdCheckON
IdCheckOFF = _libsedml.IdCheckOFF
NUMLCheckON = _libsedml.NUMLCheckON
NUMLCheckOFF = _libsedml.NUMLCheckOFF
SBOCheckON = _libsedml.SBOCheckON
SBOCheckOFF = _libsedml.SBOCheckOFF
MathCheckON = _libsedml.MathCheckON
MathCheckOFF = _libsedml.MathCheckOFF
UnitsCheckON = _libsedml.UnitsCheckON
UnitsCheckOFF = _libsedml.UnitsCheckOFF
OverdeterCheckON = _libsedml.OverdeterCheckON
OverdeterCheckOFF = _libsedml.OverdeterCheckOFF
PracticeCheckON = _libsedml.PracticeCheckON
PracticeCheckOFF = _libsedml.PracticeCheckOFF
AllChecksON = _libsedml.AllChecksON

class NUMLDocument(NMBase):
    """Proxy of C++ NUMLDocument class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    @staticmethod
    def getDefaultLevel():
        """getDefaultLevel() -> unsigned int"""
        return _libsedml.NUMLDocument_getDefaultLevel()

    @staticmethod
    def getDefaultVersion():
        """getDefaultVersion() -> unsigned int"""
        return _libsedml.NUMLDocument_getDefaultVersion()

    __swig_destroy__ = _libsedml.delete_NUMLDocument

    def __init__(self, *args):
        """
        __init__(NUMLDocument self, unsigned int level=0, unsigned int version=0) -> NUMLDocument
        __init__(NUMLDocument self, NUMLDocument rhs) -> NUMLDocument
        """
        _libsedml.NUMLDocument_swiginit(self, _libsedml.new_NUMLDocument(*args))

    def clone(self):
        """clone(NUMLDocument self) -> NUMLDocument"""
        return _libsedml.NUMLDocument_clone(self)

    def getNumOntologyTerms(self):
        """getNumOntologyTerms(NUMLDocument self) -> unsigned int"""
        return _libsedml.NUMLDocument_getNumOntologyTerms(self)

    def getOntologyTerms(self, *args):
        """
        getOntologyTerms(NUMLDocument self) -> OntologyTerms
        getOntologyTerms(NUMLDocument self) -> OntologyTerms
        """
        return _libsedml.NUMLDocument_getOntologyTerms(self, *args)

    def getResultComponents(self, *args):
        """
        getResultComponents(NUMLDocument self) -> ResultComponents
        getResultComponents(NUMLDocument self) -> ResultComponents
        """
        return _libsedml.NUMLDocument_getResultComponents(self, *args)

    def getNumResultComponents(self):
        """getNumResultComponents(NUMLDocument self) -> unsigned int"""
        return _libsedml.NUMLDocument_getNumResultComponents(self)

    def getResultComponent(self, index):
        """getResultComponent(NUMLDocument self, unsigned int index) -> ResultComponent"""
        return _libsedml.NUMLDocument_getResultComponent(self, index)

    def setLevelAndVersion(self, level, version, strict=True):
        """setLevelAndVersion(NUMLDocument self, unsigned int level, unsigned int version, bool strict=True) -> bool"""
        return _libsedml.NUMLDocument_setLevelAndVersion(self, level, version, strict)

    def createOntologyTerm(self):
        """createOntologyTerm(NUMLDocument self) -> OntologyTerm"""
        return _libsedml.NUMLDocument_createOntologyTerm(self)

    def createResultComponent(self):
        """createResultComponent(NUMLDocument self) -> ResultComponent"""
        return _libsedml.NUMLDocument_createResultComponent(self)

    def getError(self, n):
        """getError(NUMLDocument self, unsigned int n) -> NUMLError"""
        return _libsedml.NUMLDocument_getError(self, n)

    def getNumErrors(self):
        """getNumErrors(NUMLDocument self) -> unsigned int"""
        return _libsedml.NUMLDocument_getNumErrors(self)

    def printErrors(self, *args):
        """printErrors(NUMLDocument self, ostream stream=cerr)"""
        return _libsedml.NUMLDocument_printErrors(self, *args)

    def setParentNUMLObject(self, sb):
        """setParentNUMLObject(NUMLDocument self, NMBase sb)"""
        return _libsedml.NUMLDocument_setParentNUMLObject(self, sb)

    def setNUMLDocument(self, d):
        """setNUMLDocument(NUMLDocument self, NUMLDocument d)"""
        return _libsedml.NUMLDocument_setNUMLDocument(self, d)

    def getTypeCode(self):
        """getTypeCode(NUMLDocument self) -> NUMLTypeCode_t"""
        return _libsedml.NUMLDocument_getTypeCode(self)

    def getElementName(self):
        """getElementName(NUMLDocument self) -> string"""
        return _libsedml.NUMLDocument_getElementName(self)

    def getErrorLog(self):
        """getErrorLog(NUMLDocument self) -> NUMLErrorLog"""
        return _libsedml.NUMLDocument_getErrorLog(self)

    def getNamespaces(self):
        """getNamespaces(NUMLDocument self) -> XMLNamespaces"""
        return _libsedml.NUMLDocument_getNamespaces(self)

    def getElementPosition(self):
        """getElementPosition(NUMLDocument self) -> int"""
        return _libsedml.NUMLDocument_getElementPosition(self)


_libsedml.NUMLDocument_swigregister(NUMLDocument)

def NUMLDocument_getDefaultLevel():
    """NUMLDocument_getDefaultLevel() -> unsigned int"""
    return _libsedml.NUMLDocument_getDefaultLevel()


def NUMLDocument_getDefaultVersion():
    """NUMLDocument_getDefaultVersion() -> unsigned int"""
    return _libsedml.NUMLDocument_getDefaultVersion()


class ResultComponent(NMBase):
    """Proxy of C++ ResultComponent class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def clone(self):
        """clone(ResultComponent self) -> ResultComponent"""
        return _libsedml.ResultComponent_clone(self)

    def getId(self):
        """getId(ResultComponent self) -> string"""
        return _libsedml.ResultComponent_getId(self)

    def setId(self, sid):
        """setId(ResultComponent self, string sid) -> int"""
        return _libsedml.ResultComponent_setId(self, sid)

    def setNUMLDocument(self, d):
        """setNUMLDocument(ResultComponent self, NUMLDocument d)"""
        return _libsedml.ResultComponent_setNUMLDocument(self, d)

    def setParentNUMLObject(self, sb):
        """setParentNUMLObject(ResultComponent self, NMBase sb)"""
        return _libsedml.ResultComponent_setParentNUMLObject(self, sb)

    def getTypeCode(self):
        """getTypeCode(ResultComponent self) -> NUMLTypeCode_t"""
        return _libsedml.ResultComponent_getTypeCode(self)

    def getElementName(self):
        """getElementName(ResultComponent self) -> string"""
        return _libsedml.ResultComponent_getElementName(self)

    def __init__(self, *args):
        """
        __init__(ResultComponent self, unsigned int level, unsigned int version) -> ResultComponent
        __init__(ResultComponent self, NUMLNamespaces numlns) -> ResultComponent
        """
        _libsedml.ResultComponent_swiginit(self, _libsedml.new_ResultComponent(*args))

    def createDimensionDescription(self):
        """createDimensionDescription(ResultComponent self) -> DimensionDescription"""
        return _libsedml.ResultComponent_createDimensionDescription(self)

    def createCompositeDescription(self):
        """createCompositeDescription(ResultComponent self) -> CompositeDescription"""
        return _libsedml.ResultComponent_createCompositeDescription(self)

    def createCompositeValue(self):
        """createCompositeValue(ResultComponent self) -> CompositeValue"""
        return _libsedml.ResultComponent_createCompositeValue(self)

    def createTupleDescription(self):
        """createTupleDescription(ResultComponent self) -> TupleDescription"""
        return _libsedml.ResultComponent_createTupleDescription(self)

    def createTuple(self):
        """createTuple(ResultComponent self) -> Tuple"""
        return _libsedml.ResultComponent_createTuple(self)

    def createAtomicDescription(self):
        """createAtomicDescription(ResultComponent self) -> AtomicDescription"""
        return _libsedml.ResultComponent_createAtomicDescription(self)

    def createAtomicValue(self):
        """createAtomicValue(ResultComponent self) -> AtomicValue"""
        return _libsedml.ResultComponent_createAtomicValue(self)

    def getDimensionDescription(self):
        """getDimensionDescription(ResultComponent self) -> DimensionDescription"""
        return _libsedml.ResultComponent_getDimensionDescription(self)

    def getDimension(self):
        """getDimension(ResultComponent self) -> Dimension"""
        return _libsedml.ResultComponent_getDimension(self)

    __swig_destroy__ = _libsedml.delete_ResultComponent

    def createObject(self, stream):
        """createObject(ResultComponent self, XMLInputStream stream) -> NMBase"""
        return _libsedml.ResultComponent_createObject(self, stream)

    def readAttributes(self, attributes):
        """readAttributes(ResultComponent self, XMLAttributes attributes)"""
        return _libsedml.ResultComponent_readAttributes(self, attributes)

    def writeAttributes(self, stream):
        """writeAttributes(ResultComponent self, XMLOutputStream stream)"""
        return _libsedml.ResultComponent_writeAttributes(self, stream)


_libsedml.ResultComponent_swigregister(ResultComponent)

class ResultComponents(NUMLList):
    """Proxy of C++ ResultComponents class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def clone(self):
        """clone(ResultComponents self) -> ResultComponents"""
        return _libsedml.ResultComponents_clone(self)

    def getTypeCode(self):
        """getTypeCode(ResultComponents self) -> NUMLTypeCode_t"""
        return _libsedml.ResultComponents_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(ResultComponents self) -> NUMLTypeCode_t"""
        return _libsedml.ResultComponents_getItemTypeCode(self)

    def getElementName(self):
        """getElementName(ResultComponents self) -> string"""
        return _libsedml.ResultComponents_getElementName(self)

    def getResultComponents(self):
        """getResultComponents(ResultComponents self) -> ResultComponents"""
        return _libsedml.ResultComponents_getResultComponents(self)

    def get(self, *args):
        """
        get(ResultComponents self, unsigned int n) -> ResultComponent
        get(ResultComponents self, unsigned int n) -> ResultComponent
        get(ResultComponents self, string sid) -> ResultComponent
        get(ResultComponents self, string sid) -> ResultComponent
        """
        return _libsedml.ResultComponents_get(self, *args)

    def remove(self, *args):
        """
        remove(ResultComponents self, unsigned int n) -> ResultComponent
        remove(ResultComponents self, string sid) -> ResultComponent
        """
        return _libsedml.ResultComponents_remove(self, *args)

    def getElementPosition(self):
        """getElementPosition(ResultComponents self) -> int"""
        return _libsedml.ResultComponents_getElementPosition(self)

    def __init__(self):
        """__init__(ResultComponents self) -> ResultComponents"""
        _libsedml.ResultComponents_swiginit(self, _libsedml.new_ResultComponents())

    __swig_destroy__ = _libsedml.delete_ResultComponents


_libsedml.ResultComponents_swigregister(ResultComponents)

class Dimension(NUMLList):
    """Proxy of C++ Dimension class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(Dimension self) -> Dimension
        __init__(Dimension self, unsigned int level, unsigned int version) -> Dimension
        __init__(Dimension self, NUMLNamespaces numlns) -> Dimension
        """
        _libsedml.Dimension_swiginit(self, _libsedml.new_Dimension(*args))

    def clone(self):
        """clone(Dimension self) -> Dimension"""
        return _libsedml.Dimension_clone(self)

    def createCompositeValue(self):
        """createCompositeValue(Dimension self) -> CompositeValue"""
        return _libsedml.Dimension_createCompositeValue(self)

    def createTuple(self):
        """createTuple(Dimension self) -> Tuple"""
        return _libsedml.Dimension_createTuple(self)

    def createAtomicValue(self):
        """createAtomicValue(Dimension self) -> AtomicValue"""
        return _libsedml.Dimension_createAtomicValue(self)

    def getTypeCode(self):
        """getTypeCode(Dimension self) -> NUMLTypeCode_t"""
        return _libsedml.Dimension_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(Dimension self) -> NUMLTypeCode_t"""
        return _libsedml.Dimension_getItemTypeCode(self)

    def getElementName(self):
        """getElementName(Dimension self) -> string"""
        return _libsedml.Dimension_getElementName(self)

    def get(self, *args):
        """
        get(Dimension self, unsigned int n) -> Dimension
        get(Dimension self, unsigned int n) -> Dimension
        get(Dimension self, string sid) -> CompositeValue
        get(Dimension self, string sid) -> CompositeValue
        """
        return _libsedml.Dimension_get(self, *args)

    def remove(self, *args):
        """
        remove(Dimension self, unsigned int n) -> Dimension
        remove(Dimension self, string sid) -> Dimension
        """
        return _libsedml.Dimension_remove(self, *args)

    def getElementPosition(self):
        """getElementPosition(Dimension self) -> int"""
        return _libsedml.Dimension_getElementPosition(self)

    __swig_destroy__ = _libsedml.delete_Dimension


_libsedml.Dimension_swigregister(Dimension)

class DimensionDescription(NUMLList):
    """Proxy of C++ DimensionDescription class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        __init__(DimensionDescription self) -> DimensionDescription
        __init__(DimensionDescription self, unsigned int level, unsigned int version) -> DimensionDescription
        __init__(DimensionDescription self, NUMLNamespaces numlns) -> DimensionDescription
        """
        _libsedml.DimensionDescription_swiginit(self, _libsedml.new_DimensionDescription(*args))

    def clone(self):
        """clone(DimensionDescription self) -> DimensionDescription"""
        return _libsedml.DimensionDescription_clone(self)

    def createCompositeDescription(self):
        """createCompositeDescription(DimensionDescription self) -> CompositeDescription"""
        return _libsedml.DimensionDescription_createCompositeDescription(self)

    def createTupleDescription(self):
        """createTupleDescription(DimensionDescription self) -> TupleDescription"""
        return _libsedml.DimensionDescription_createTupleDescription(self)

    def createAtomicDescription(self):
        """createAtomicDescription(DimensionDescription self) -> AtomicDescription"""
        return _libsedml.DimensionDescription_createAtomicDescription(self)

    def getElementName(self):
        """getElementName(DimensionDescription self) -> string"""
        return _libsedml.DimensionDescription_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(DimensionDescription self) -> NUMLTypeCode_t"""
        return _libsedml.DimensionDescription_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(DimensionDescription self) -> NUMLTypeCode_t"""
        return _libsedml.DimensionDescription_getItemTypeCode(self)

    def get(self, *args):
        """
        get(DimensionDescription self, unsigned int n) -> DimensionDescription
        get(DimensionDescription self, unsigned int n) -> DimensionDescription
        get(DimensionDescription self, string sid) -> DimensionDescription
        get(DimensionDescription self, string sid) -> DimensionDescription
        """
        return _libsedml.DimensionDescription_get(self, *args)

    def getId(self):
        """getId(DimensionDescription self) -> string"""
        return _libsedml.DimensionDescription_getId(self)

    def setId(self, id):
        """setId(DimensionDescription self, string id) -> int"""
        return _libsedml.DimensionDescription_setId(self, id)

    def getName(self):
        """getName(DimensionDescription self) -> string"""
        return _libsedml.DimensionDescription_getName(self)

    def setName(self, name):
        """setName(DimensionDescription self, string name) -> int"""
        return _libsedml.DimensionDescription_setName(self, name)

    def remove(self, *args):
        """
        remove(DimensionDescription self, unsigned int n) -> DimensionDescription
        remove(DimensionDescription self, string sid) -> DimensionDescription
        """
        return _libsedml.DimensionDescription_remove(self, *args)

    def getElementPosition(self):
        """getElementPosition(DimensionDescription self) -> int"""
        return _libsedml.DimensionDescription_getElementPosition(self)

    __swig_destroy__ = _libsedml.delete_DimensionDescription


_libsedml.DimensionDescription_swigregister(DimensionDescription)

class CompositeValue(Dimension):
    """Proxy of C++ CompositeValue class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_CompositeValue

    def __init__(self, *args):
        """
        __init__(CompositeValue self) -> CompositeValue
        __init__(CompositeValue self, unsigned int level, unsigned int version) -> CompositeValue
        __init__(CompositeValue self, NUMLNamespaces numlns) -> CompositeValue
        """
        _libsedml.CompositeValue_swiginit(self, _libsedml.new_CompositeValue(*args))

    def clone(self):
        """clone(CompositeValue self) -> CompositeValue"""
        return _libsedml.CompositeValue_clone(self)

    def getTypeCode(self):
        """getTypeCode(CompositeValue self) -> NUMLTypeCode_t"""
        return _libsedml.CompositeValue_getTypeCode(self)

    def getIndexValue(self):
        """getIndexValue(CompositeValue self) -> string"""
        return _libsedml.CompositeValue_getIndexValue(self)

    def getDescription(self):
        """getDescription(CompositeValue self) -> string"""
        return _libsedml.CompositeValue_getDescription(self)

    def setIndexValue(self, indexValue):
        """setIndexValue(CompositeValue self, string indexValue) -> int"""
        return _libsedml.CompositeValue_setIndexValue(self, indexValue)

    def setDescription(self, description):
        """setDescription(CompositeValue self, string description) -> int"""
        return _libsedml.CompositeValue_setDescription(self, description)

    def getElementName(self):
        """getElementName(CompositeValue self) -> string"""
        return _libsedml.CompositeValue_getElementName(self)

    def getItemTypeCode(self):
        """getItemTypeCode(CompositeValue self) -> NUMLTypeCode_t"""
        return _libsedml.CompositeValue_getItemTypeCode(self)

    def isContentCompositeValue(self):
        """isContentCompositeValue(CompositeValue self) -> bool"""
        return _libsedml.CompositeValue_isContentCompositeValue(self)

    def isContentTuple(self):
        """isContentTuple(CompositeValue self) -> bool"""
        return _libsedml.CompositeValue_isContentTuple(self)

    def isContentAtomicValue(self):
        """isContentAtomicValue(CompositeValue self) -> bool"""
        return _libsedml.CompositeValue_isContentAtomicValue(self)

    def getCompositeValue(self, n):
        """getCompositeValue(CompositeValue self, unsigned int n) -> CompositeValue"""
        return _libsedml.CompositeValue_getCompositeValue(self, n)

    def getTuple(self):
        """getTuple(CompositeValue self) -> Tuple"""
        return _libsedml.CompositeValue_getTuple(self)

    def getAtomicValue(self):
        """getAtomicValue(CompositeValue self) -> AtomicValue"""
        return _libsedml.CompositeValue_getAtomicValue(self)

    def get(self, *args):
        """
        get(CompositeValue self, unsigned int n) -> CompositeValue
        get(CompositeValue self, unsigned int n) -> CompositeValue
        """
        return _libsedml.CompositeValue_get(self, *args)

    def remove(self, n):
        """remove(CompositeValue self, unsigned int n) -> CompositeValue"""
        return _libsedml.CompositeValue_remove(self, n)

    def readAttributes(self, attributes):
        """readAttributes(CompositeValue self, XMLAttributes attributes)"""
        return _libsedml.CompositeValue_readAttributes(self, attributes)

    def writeAttributes(self, stream):
        """writeAttributes(CompositeValue self, XMLOutputStream stream)"""
        return _libsedml.CompositeValue_writeAttributes(self, stream)

    def addCompositeValue(self, compValue):
        """addCompositeValue(CompositeValue self, CompositeValue compValue) -> int"""
        return _libsedml.CompositeValue_addCompositeValue(self, compValue)

    def createCompositeValue(self):
        """createCompositeValue(CompositeValue self) -> CompositeValue"""
        return _libsedml.CompositeValue_createCompositeValue(self)

    def createTuple(self):
        """createTuple(CompositeValue self) -> Tuple"""
        return _libsedml.CompositeValue_createTuple(self)

    def createAtomicValue(self):
        """createAtomicValue(CompositeValue self) -> AtomicValue"""
        return _libsedml.CompositeValue_createAtomicValue(self)


_libsedml.CompositeValue_swigregister(CompositeValue)

class Tuple(Dimension):
    """Proxy of C++ Tuple class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_Tuple

    def __init__(self, *args):
        """
        __init__(Tuple self) -> Tuple
        __init__(Tuple self, unsigned int level, unsigned int version) -> Tuple
        __init__(Tuple self, NUMLNamespaces numlns) -> Tuple
        """
        _libsedml.Tuple_swiginit(self, _libsedml.new_Tuple(*args))

    def clone(self):
        """clone(Tuple self) -> Tuple"""
        return _libsedml.Tuple_clone(self)

    def getTypeCode(self):
        """getTypeCode(Tuple self) -> NUMLTypeCode_t"""
        return _libsedml.Tuple_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(Tuple self) -> NUMLTypeCode_t"""
        return _libsedml.Tuple_getItemTypeCode(self)

    def getElementPosition(self):
        """getElementPosition(Tuple self) -> int"""
        return _libsedml.Tuple_getElementPosition(self)

    def getElementName(self):
        """getElementName(Tuple self) -> string"""
        return _libsedml.Tuple_getElementName(self)

    def getAtomicValue(self, *args):
        """
        getAtomicValue(Tuple self, unsigned int n) -> AtomicValue
        getAtomicValue(Tuple self, unsigned int n) -> AtomicValue
        """
        return _libsedml.Tuple_getAtomicValue(self, *args)

    def removeAtomicValue(self, n):
        """removeAtomicValue(Tuple self, unsigned int n) -> AtomicValue"""
        return _libsedml.Tuple_removeAtomicValue(self, n)

    def createAtomicValue(self):
        """createAtomicValue(Tuple self) -> AtomicValue"""
        return _libsedml.Tuple_createAtomicValue(self)

    def createObject(self, stream):
        """createObject(Tuple self, XMLInputStream stream) -> NMBase"""
        return _libsedml.Tuple_createObject(self, stream)

    def write(self, stream):
        """write(Tuple self, XMLOutputStream stream)"""
        return _libsedml.Tuple_write(self, stream)


_libsedml.Tuple_swigregister(Tuple)

class AtomicValue(Dimension):
    """Proxy of C++ AtomicValue class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getTypeCode(self):
        """getTypeCode(AtomicValue self) -> NUMLTypeCode_t"""
        return _libsedml.AtomicValue_getTypeCode(self)

    def getElementName(self):
        """getElementName(AtomicValue self) -> string"""
        return _libsedml.AtomicValue_getElementName(self)

    def getValue(self):
        """getValue(AtomicValue self) -> string"""
        return _libsedml.AtomicValue_getValue(self)

    def getDoubleValue(self):
        """getDoubleValue(AtomicValue self) -> double"""
        return _libsedml.AtomicValue_getDoubleValue(self)

    def setValue(self, value):
        """setValue(AtomicValue self, string value) -> int"""
        return _libsedml.AtomicValue_setValue(self, value)

    def writeChars(self, stream):
        """writeChars(AtomicValue self, XMLOutputStream stream)"""
        return _libsedml.AtomicValue_writeChars(self, stream)

    def clone(self):
        """clone(AtomicValue self) -> AtomicValue"""
        return _libsedml.AtomicValue_clone(self)

    def __init__(self, *args):
        """
        __init__(AtomicValue self, unsigned int level, unsigned int version) -> AtomicValue
        __init__(AtomicValue self, NUMLNamespaces numlns) -> AtomicValue
        __init__(AtomicValue self) -> AtomicValue
        """
        _libsedml.AtomicValue_swiginit(self, _libsedml.new_AtomicValue(*args))

    __swig_destroy__ = _libsedml.delete_AtomicValue


_libsedml.AtomicValue_swigregister(AtomicValue)

class CompositeDescription(DimensionDescription):
    """Proxy of C++ CompositeDescription class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_CompositeDescription

    def __init__(self, *args):
        """
        __init__(CompositeDescription self) -> CompositeDescription
        __init__(CompositeDescription self, unsigned int level, unsigned int version) -> CompositeDescription
        __init__(CompositeDescription self, NUMLNamespaces numlns) -> CompositeDescription
        """
        _libsedml.CompositeDescription_swiginit(self, _libsedml.new_CompositeDescription(*args))

    def clone(self):
        """clone(CompositeDescription self) -> CompositeDescription"""
        return _libsedml.CompositeDescription_clone(self)

    def getName(self):
        """getName(CompositeDescription self) -> string"""
        return _libsedml.CompositeDescription_getName(self)

    def getId(self):
        """getId(CompositeDescription self) -> string"""
        return _libsedml.CompositeDescription_getId(self)

    def setId(self, id):
        """setId(CompositeDescription self, string id) -> int"""
        return _libsedml.CompositeDescription_setId(self, id)

    def getIndexType(self):
        """getIndexType(CompositeDescription self) -> string"""
        return _libsedml.CompositeDescription_getIndexType(self)

    def isContentCompositeDescription(self):
        """isContentCompositeDescription(CompositeDescription self) -> bool"""
        return _libsedml.CompositeDescription_isContentCompositeDescription(self)

    def isContentTupleDescription(self):
        """isContentTupleDescription(CompositeDescription self) -> bool"""
        return _libsedml.CompositeDescription_isContentTupleDescription(self)

    def isContentAtomicDescription(self):
        """isContentAtomicDescription(CompositeDescription self) -> bool"""
        return _libsedml.CompositeDescription_isContentAtomicDescription(self)

    def getOntologyTerm(self):
        """getOntologyTerm(CompositeDescription self) -> string"""
        return _libsedml.CompositeDescription_getOntologyTerm(self)

    def setName(self, name):
        """setName(CompositeDescription self, string name) -> int"""
        return _libsedml.CompositeDescription_setName(self, name)

    def setIndexType(self, indexType):
        """setIndexType(CompositeDescription self, string indexType) -> int"""
        return _libsedml.CompositeDescription_setIndexType(self, indexType)

    def setOntologyTerm(self, ontologyTerm):
        """setOntologyTerm(CompositeDescription self, string ontologyTerm) -> int"""
        return _libsedml.CompositeDescription_setOntologyTerm(self, ontologyTerm)

    def getElementName(self):
        """getElementName(CompositeDescription self) -> string"""
        return _libsedml.CompositeDescription_getElementName(self)

    def getTypeCode(self):
        """getTypeCode(CompositeDescription self) -> NUMLTypeCode_t"""
        return _libsedml.CompositeDescription_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(CompositeDescription self) -> NUMLTypeCode_t"""
        return _libsedml.CompositeDescription_getItemTypeCode(self)

    def getCompositeDescription(self, n):
        """getCompositeDescription(CompositeDescription self, unsigned int n) -> CompositeDescription"""
        return _libsedml.CompositeDescription_getCompositeDescription(self, n)

    def getTupleDescription(self):
        """getTupleDescription(CompositeDescription self) -> TupleDescription"""
        return _libsedml.CompositeDescription_getTupleDescription(self)

    def getAtomicDescription(self):
        """getAtomicDescription(CompositeDescription self) -> AtomicDescription"""
        return _libsedml.CompositeDescription_getAtomicDescription(self)

    def get(self, *args):
        """
        get(CompositeDescription self, unsigned int n) -> CompositeDescription
        get(CompositeDescription self, unsigned int n) -> CompositeDescription
        """
        return _libsedml.CompositeDescription_get(self, *args)

    def remove(self, n):
        """remove(CompositeDescription self, unsigned int n) -> CompositeDescription"""
        return _libsedml.CompositeDescription_remove(self, n)

    def createCompositeDescription(self):
        """createCompositeDescription(CompositeDescription self) -> CompositeDescription"""
        return _libsedml.CompositeDescription_createCompositeDescription(self)

    def createTupleDescription(self):
        """createTupleDescription(CompositeDescription self) -> TupleDescription"""
        return _libsedml.CompositeDescription_createTupleDescription(self)

    def createAtomicDescription(self):
        """createAtomicDescription(CompositeDescription self) -> AtomicDescription"""
        return _libsedml.CompositeDescription_createAtomicDescription(self)


_libsedml.CompositeDescription_swigregister(CompositeDescription)

class TupleDescription(DimensionDescription):
    """Proxy of C++ TupleDescription class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libsedml.delete_TupleDescription

    def __init__(self, *args):
        """
        __init__(TupleDescription self) -> TupleDescription
        __init__(TupleDescription self, unsigned int level, unsigned int version) -> TupleDescription
        __init__(TupleDescription self, NUMLNamespaces numlns) -> TupleDescription
        """
        _libsedml.TupleDescription_swiginit(self, _libsedml.new_TupleDescription(*args))

    def clone(self):
        """clone(TupleDescription self) -> TupleDescription"""
        return _libsedml.TupleDescription_clone(self)

    def getId(self):
        """getId(TupleDescription self) -> string"""
        return _libsedml.TupleDescription_getId(self)

    def setId(self, id):
        """setId(TupleDescription self, string id) -> int"""
        return _libsedml.TupleDescription_setId(self, id)

    def getTypeCode(self):
        """getTypeCode(TupleDescription self) -> NUMLTypeCode_t"""
        return _libsedml.TupleDescription_getTypeCode(self)

    def getItemTypeCode(self):
        """getItemTypeCode(TupleDescription self) -> NUMLTypeCode_t"""
        return _libsedml.TupleDescription_getItemTypeCode(self)

    def getElementPosition(self):
        """getElementPosition(TupleDescription self) -> int"""
        return _libsedml.TupleDescription_getElementPosition(self)

    def getElementName(self):
        """getElementName(TupleDescription self) -> string"""
        return _libsedml.TupleDescription_getElementName(self)

    def getAtomicDescription(self, *args):
        """
        getAtomicDescription(TupleDescription self, unsigned int n) -> AtomicDescription
        getAtomicDescription(TupleDescription self, unsigned int n) -> AtomicDescription
        """
        return _libsedml.TupleDescription_getAtomicDescription(self, *args)

    def removeAtomicDescription(self, n):
        """removeAtomicDescription(TupleDescription self, unsigned int n) -> AtomicDescription"""
        return _libsedml.TupleDescription_removeAtomicDescription(self, n)

    def createAtomicDescription(self):
        """createAtomicDescription(TupleDescription self) -> AtomicDescription"""
        return _libsedml.TupleDescription_createAtomicDescription(self)

    def createObject(self, stream):
        """createObject(TupleDescription self, XMLInputStream stream) -> NMBase"""
        return _libsedml.TupleDescription_createObject(self, stream)

    def write(self, stream):
        """write(TupleDescription self, XMLOutputStream stream)"""
        return _libsedml.TupleDescription_write(self, stream)


_libsedml.TupleDescription_swigregister(TupleDescription)

class AtomicDescription(DimensionDescription):
    """Proxy of C++ AtomicDescription class."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getTypeCode(self):
        """getTypeCode(AtomicDescription self) -> NUMLTypeCode_t"""
        return _libsedml.AtomicDescription_getTypeCode(self)

    def getElementName(self):
        """getElementName(AtomicDescription self) -> string"""
        return _libsedml.AtomicDescription_getElementName(self)

    def getValueType(self):
        """getValueType(AtomicDescription self) -> string"""
        return _libsedml.AtomicDescription_getValueType(self)

    def getOntologyTerm(self):
        """getOntologyTerm(AtomicDescription self) -> string"""
        return _libsedml.AtomicDescription_getOntologyTerm(self)

    def getName(self):
        """getName(AtomicDescription self) -> string"""
        return _libsedml.AtomicDescription_getName(self)

    def setOntologyTerm(self, ontologyTerm):
        """setOntologyTerm(AtomicDescription self, string ontologyTerm) -> int"""
        return _libsedml.AtomicDescription_setOntologyTerm(self, ontologyTerm)

    def setValueType(self, valueType):
        """setValueType(AtomicDescription self, string valueType) -> int"""
        return _libsedml.AtomicDescription_setValueType(self, valueType)

    def setName(self, name):
        """setName(AtomicDescription self, string name) -> int"""
        return _libsedml.AtomicDescription_setName(self, name)

    def getId(self):
        """getId(AtomicDescription self) -> string"""
        return _libsedml.AtomicDescription_getId(self)

    def setId(self, id):
        """setId(AtomicDescription self, string id) -> int"""
        return _libsedml.AtomicDescription_setId(self, id)

    def clone(self):
        """clone(AtomicDescription self) -> AtomicDescription"""
        return _libsedml.AtomicDescription_clone(self)

    def __init__(self, *args):
        """
        __init__(AtomicDescription self, unsigned int level, unsigned int version) -> AtomicDescription
        __init__(AtomicDescription self, NUMLNamespaces numlns) -> AtomicDescription
        __init__(AtomicDescription self) -> AtomicDescription
        """
        _libsedml.AtomicDescription_swiginit(self, _libsedml.new_AtomicDescription(*args))

    __swig_destroy__ = _libsedml.delete_AtomicDescription


_libsedml.AtomicDescription_swigregister(AtomicDescription)
__version__ = '2.0.9'
# global __version__ ## Warning: Unused global
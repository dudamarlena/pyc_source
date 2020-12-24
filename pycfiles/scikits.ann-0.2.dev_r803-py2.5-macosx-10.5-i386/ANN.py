# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/scikits/ann/ANN.py
# Compiled at: 2008-01-30 21:57:20
import _ANN, new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == 'thisown':
        return self.this.own(value)
    if name == 'this':
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if not static or hasattr(self, name):
        self.__dict__[name] = value
    else:
        raise AttributeError('You cannot add attributes to %s' % self)
    return


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == 'thisown':
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError, name
    return


def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except:
        strthis = ''

    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:

    class _object:
        pass


    _newclass = 0

del types

class _kdtree(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, _kdtree, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, _kdtree, name)

    def __init__(self, *args):
        this = _ANN.new__kdtree(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _ANN.delete__kdtree
    __del__ = lambda self: None

    def _knn2(*args):
        return _ANN.__knn2(*args)

    def __repr__(*args):
        return _ANN._kdtree___repr__(*args)

    def __str__(*args):
        return _ANN._kdtree___str__(*args)


_kdtree_swigregister = _ANN._kdtree_swigregister
_kdtree_swigregister(_kdtree)
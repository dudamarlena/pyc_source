# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/ks.py
# Compiled at: 2009-12-08 17:43:28
import _ks, new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == 'thisown':
        return self.this.own(value)
    else:
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
    else:
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
parseBuffer = _ks.parseBuffer
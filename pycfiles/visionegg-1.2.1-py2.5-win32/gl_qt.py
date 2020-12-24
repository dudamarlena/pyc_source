# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\gl_qt.py
# Compiled at: 2009-07-07 11:29:44
import _gl_qt

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == 'this':
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value, 'thisown'):
                self.__dict__['thisown'] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if not static or hasattr(self, name) or name == 'thisown':
        self.__dict__[name] = value
    else:
        raise AttributeError('You cannot add attributes to %s' % self)
    return


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError, name
    return


import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:

    class _object:
        pass


    _newclass = 0

del types
gl_qt_renderer_create = _gl_qt.gl_qt_renderer_create
gl_qt_renderer_delete = _gl_qt.gl_qt_renderer_delete
gl_qt_renderer_update = _gl_qt.gl_qt_renderer_update
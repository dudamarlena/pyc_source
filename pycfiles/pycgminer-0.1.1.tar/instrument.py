# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\hls501\documents\programming\api\pycgm2\pycgm2\pyCGM2\ma\instrument.py
# Compiled at: 2018-09-12 05:53:36
from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 6, 0):

    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_instrument', [dirname(__file__)])
        except ImportError:
            import _instrument
            return _instrument

        if fp is not None:
            try:
                _mod = imp.load_module('_instrument', fp, pathname, description)
            finally:
                fp.close()

            return _mod
        else:
            return


    _instrument = swig_import_helper()
    del swig_import_helper
else:
    import _instrument
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
Location_Origin = _instrument.Location_Origin
Location_SurfaceOrigin = _instrument.Location_SurfaceOrigin
Location_CentreOfPressure = _instrument.Location_CentreOfPressure
Location_PointOfApplication = _instrument.Location_PointOfApplication
T_ForcePlate = _instrument.T_ForcePlate

class ForcePlate(ma.Hardware):
    __swig_setmethods__ = {}
    for _s in [ma.Hardware]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ForcePlate, name, value)
    __swig_getmethods__ = {}
    for _s in [ma.Hardware]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ForcePlate, name)
    __repr__ = _swig_repr

    def __init__(self, other):
        this = _instrument.new_ForcePlate(other)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    Type_Unknown = _instrument.ForcePlate_Type_Unknown
    Type_Type2 = _instrument.ForcePlate_Type_Type2
    Type_Raw6x6 = _instrument.ForcePlate_Type_Raw6x6
    Type_Type3 = _instrument.ForcePlate_Type_Type3
    Type_Raw6x8 = _instrument.ForcePlate_Type_Raw6x8
    Type_Type4 = _instrument.ForcePlate_Type_Type4
    Type_Cal6x6 = _instrument.ForcePlate_Type_Cal6x6
    Type_Type5 = _instrument.ForcePlate_Type_Type5
    Type_Cal6x8 = _instrument.ForcePlate_Type_Cal6x8
    __swig_destroy__ = _instrument.delete_ForcePlate
    __del__ = lambda self: None

    def type(self):
        return _instrument.ForcePlate_type(self)

    def setGeometry(self, rso, sc1, sc2, sc3, sc4):
        return _instrument.ForcePlate_setGeometry(self, rso, sc1, sc2, sc3, sc4)

    def referenceFrame(self):
        return _instrument.ForcePlate_referenceFrame(self)

    def surfaceCorners(self):
        return _instrument.ForcePlate_surfaceCorners(self)

    def relativeSurfaceOrigin(self):
        return _instrument.ForcePlate_relativeSurfaceOrigin(self)

    def calibrationMatrixDimensions(self):
        return _instrument.ForcePlate_calibrationMatrixDimensions(self)

    def calibrationMatrixData(self):
        return _instrument.ForcePlate_calibrationMatrixData(self)

    def setCalibrationMatrixData(self, value):
        return _instrument.ForcePlate_setCalibrationMatrixData(self, value)

    def wrench(self, loc, arg3=True, threshold=10.0, rate=-1.0):
        return _instrument.ForcePlate_wrench(self, loc, arg3, threshold, rate)


ForcePlate_swigregister = _instrument.ForcePlate_swigregister
ForcePlate_swigregister(ForcePlate)
T_ForcePlateType2 = _instrument.T_ForcePlateType2

class ForcePlateType2(ForcePlate):
    __swig_setmethods__ = {}
    for _s in [ForcePlate]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ForcePlateType2, name, value)
    __swig_getmethods__ = {}
    for _s in [ForcePlate]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ForcePlateType2, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _instrument.new_ForcePlateType2(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    __swig_destroy__ = _instrument.delete_ForcePlateType2
    __del__ = lambda self: None


ForcePlateType2_swigregister = _instrument.ForcePlateType2_swigregister
ForcePlateType2_swigregister(ForcePlateType2)
T_ForcePlateType3 = _instrument.T_ForcePlateType3

class ForcePlateType3(ForcePlate):
    __swig_setmethods__ = {}
    for _s in [ForcePlate]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ForcePlateType3, name, value)
    __swig_getmethods__ = {}
    for _s in [ForcePlate]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ForcePlateType3, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _instrument.new_ForcePlateType3(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    __swig_destroy__ = _instrument.delete_ForcePlateType3
    __del__ = lambda self: None

    def sensorOffsets(self):
        return _instrument.ForcePlateType3_sensorOffsets(self)

    def setSensorOffsets(self, value):
        return _instrument.ForcePlateType3_setSensorOffsets(self, value)


ForcePlateType3_swigregister = _instrument.ForcePlateType3_swigregister
ForcePlateType3_swigregister(ForcePlateType3)
T_ForcePlateType4 = _instrument.T_ForcePlateType4

class ForcePlateType4(ForcePlate):
    __swig_setmethods__ = {}
    for _s in [ForcePlate]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ForcePlateType4, name, value)
    __swig_getmethods__ = {}
    for _s in [ForcePlate]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ForcePlateType4, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _instrument.new_ForcePlateType4(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    __swig_destroy__ = _instrument.delete_ForcePlateType4
    __del__ = lambda self: None


ForcePlateType4_swigregister = _instrument.ForcePlateType4_swigregister
ForcePlateType4_swigregister(ForcePlateType4)
T_ForcePlateType5 = _instrument.T_ForcePlateType5

class ForcePlateType5(ForcePlate):
    __swig_setmethods__ = {}
    for _s in [ForcePlate]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ForcePlateType5, name, value)
    __swig_getmethods__ = {}
    for _s in [ForcePlate]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ForcePlateType5, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _instrument.new_ForcePlateType5(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    __swig_destroy__ = _instrument.delete_ForcePlateType5
    __del__ = lambda self: None


ForcePlateType5_swigregister = _instrument.ForcePlateType5_swigregister
ForcePlateType5_swigregister(ForcePlateType5)
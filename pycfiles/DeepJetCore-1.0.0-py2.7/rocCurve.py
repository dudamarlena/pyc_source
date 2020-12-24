# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepJetCore/compiled/cpp/rocCurve.py
# Compiled at: 2018-07-20 11:01:33
from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):

    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = ('.').join((pkg, '_rocCurve')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_rocCurve')


    _rocCurve = swig_import_helper()
    del swig_import_helper
else:
    if _swig_python_version_info >= (2, 6, 0):

        def swig_import_helper():
            from os.path import dirname
            import imp
            fp = None
            try:
                fp, pathname, description = imp.find_module('_rocCurve', [dirname(__file__)])
            except ImportError:
                import _rocCurve
                return _rocCurve

            try:
                _mod = imp.load_module('_rocCurve', fp, pathname, description)
            finally:
                if fp is not None:
                    fp.close()

            return _mod


        _rocCurve = swig_import_helper()
        del swig_import_helper
    else:
        import _rocCurve
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

class rocCurve(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, rocCurve, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, rocCurve, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _rocCurve.new_rocCurve(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    __swig_destroy__ = _rocCurve.delete_rocCurve
    __del__ = lambda self: None

    def addTruth(self, t):
        return _rocCurve.rocCurve_addTruth(self, t)

    def addVetoTruth(self, ct):
        return _rocCurve.rocCurve_addVetoTruth(self, ct)

    def addTagProbability(self, p):
        return _rocCurve.rocCurve_addTagProbability(self, p)

    def setInvalidCuts(self, p):
        return _rocCurve.rocCurve_setInvalidCuts(self, p)

    def setCuts(self, cut):
        return _rocCurve.rocCurve_setCuts(self, cut)

    def setNBins(self, nbins):
        return _rocCurve.rocCurve_setNBins(self, nbins)

    def setLine(self, col, width=1, style=1):
        return _rocCurve.rocCurve_setLine(self, col, width, style)

    def setLineWidth(self, width=1):
        return _rocCurve.rocCurve_setLineWidth(self, width)

    def name(self):
        return _rocCurve.rocCurve_name(self)

    def compatName(self):
        return _rocCurve.rocCurve_compatName(self)

    def process(self, *args):
        return _rocCurve.rocCurve_process(self, *args)

    def getROC(self):
        return _rocCurve.rocCurve_getROC(self)

    def getProbHisto(self):
        return _rocCurve.rocCurve_getProbHisto(self)

    def getVetoProbHisto(self):
        return _rocCurve.rocCurve_getVetoProbHisto(self)

    def getInvalidatedHisto(self):
        return _rocCurve.rocCurve_getInvalidatedHisto(self)

    def getInvalidatedVetoHisto(self):
        return _rocCurve.rocCurve_getInvalidatedVetoHisto(self)


rocCurve_swigregister = _rocCurve.rocCurve_swigregister
rocCurve_swigregister(rocCurve)
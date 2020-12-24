# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepJetCore/compiled/cpp/rocCurveCollection.py
# Compiled at: 2018-07-20 11:01:37
from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):

    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = ('.').join((pkg, '_rocCurveCollection')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_rocCurveCollection')


    _rocCurveCollection = swig_import_helper()
    del swig_import_helper
else:
    if _swig_python_version_info >= (2, 6, 0):

        def swig_import_helper():
            from os.path import dirname
            import imp
            fp = None
            try:
                fp, pathname, description = imp.find_module('_rocCurveCollection', [dirname(__file__)])
            except ImportError:
                import _rocCurveCollection
                return _rocCurveCollection

            try:
                _mod = imp.load_module('_rocCurveCollection', fp, pathname, description)
            finally:
                if fp is not None:
                    fp.close()

            return _mod


        _rocCurveCollection = swig_import_helper()
        del swig_import_helper
    else:
        import _rocCurveCollection
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

class rocCurveCollection(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, rocCurveCollection, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, rocCurveCollection, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _rocCurveCollection.new_rocCurveCollection()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    __swig_destroy__ = _rocCurveCollection.delete_rocCurveCollection
    __del__ = lambda self: None

    def setLineWidth(self, width):
        return _rocCurveCollection.rocCurveCollection_setLineWidth(self, width)

    def setCommentLine0(self, l):
        return _rocCurveCollection.rocCurveCollection_setCommentLine0(self, l)

    def setCommentLine1(self, l):
        return _rocCurveCollection.rocCurveCollection_setCommentLine1(self, l)

    def setNBins(self, nbins):
        return _rocCurveCollection.rocCurveCollection_setNBins(self, nbins)

    def addExtraLegendEntry(self, entr):
        return _rocCurveCollection.rocCurveCollection_addExtraLegendEntry(self, entr)

    def setCMSStyle(self, cmsst):
        return _rocCurveCollection.rocCurveCollection_setCMSStyle(self, cmsst)

    def setLogY(self, logy):
        return _rocCurveCollection.rocCurveCollection_setLogY(self, logy)

    def setXaxis(self, axis):
        return _rocCurveCollection.rocCurveCollection_setXaxis(self, axis)

    def setYaxis(self, axis):
        return _rocCurveCollection.rocCurveCollection_setYaxis(self, axis)

    def addROC(self, *args):
        return _rocCurveCollection.rocCurveCollection_addROC(self, *args)

    def addText(self, l):
        return _rocCurveCollection.rocCurveCollection_addText(self, l)

    def printRocs(self, *args):
        return _rocCurveCollection.rocCurveCollection_printRocs(self, *args)


rocCurveCollection_swigregister = _rocCurveCollection.rocCurveCollection_swigregister
rocCurveCollection_swigregister(rocCurveCollection)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepJetCore/compiled/cpp/indata.py
# Compiled at: 2018-07-20 11:01:15
from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):

    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = ('.').join((pkg, '_indata')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_indata')


    _indata = swig_import_helper()
    del swig_import_helper
else:
    if _swig_python_version_info >= (2, 6, 0):

        def swig_import_helper():
            from os.path import dirname
            import imp
            fp = None
            try:
                fp, pathname, description = imp.find_module('_indata', [dirname(__file__)])
            except ImportError:
                import _indata
                return _indata

            try:
                _mod = imp.load_module('_indata', fp, pathname, description)
            finally:
                if fp is not None:
                    fp.close()

            return _mod


        _indata = swig_import_helper()
        del swig_import_helper
    else:
        import _indata
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

MAXBRANCHLENGTH = _indata.MAXBRANCHLENGTH

class indata(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, indata, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, indata, name)
    __repr__ = _swig_repr
    __swig_setmethods__['meanPadding'] = _indata.indata_meanPadding_set
    __swig_getmethods__['meanPadding'] = _indata.indata_meanPadding_get
    if _newclass:
        meanPadding = _swig_property(_indata.indata_meanPadding_get, _indata.indata_meanPadding_set)
    __swig_setmethods__['doscaling'] = _indata.indata_doscaling_set
    __swig_getmethods__['doscaling'] = _indata.indata_doscaling_get
    if _newclass:
        doscaling = _swig_property(_indata.indata_doscaling_get, _indata.indata_doscaling_set)

    def __init__(self):
        this = _indata.new_indata()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def createFrom(self, s_branches, s_norms, s_means, s_max):
        return _indata.indata_createFrom(self, s_branches, s_norms, s_means, s_max)

    def setSize(self, i):
        return _indata.indata_setSize(self, i)

    __swig_destroy__ = _indata.delete_indata
    __del__ = lambda self: None

    def getMax(self):
        return _indata.indata_getMax(self)

    def getData(self, b, i):
        return _indata.indata_getData(self, b, i)

    def getRaw(self, b, i):
        return _indata.indata_getRaw(self, b, i)

    def mean(self, b):
        return _indata.indata_mean(self, b)

    def std(self, b):
        return _indata.indata_std(self, b)

    def getDefault(self, b):
        return _indata.indata_getDefault(self, b)

    def allZero(self):
        return _indata.indata_allZero(self)

    def getEntry(self, entry):
        return _indata.indata_getEntry(self, entry)

    def zeroAndGet(self, entry):
        return _indata.indata_zeroAndGet(self, entry)

    def isVector(self):
        return _indata.indata_isVector(self)

    def setup(self, *args):
        return _indata.indata_setup(self, *args)

    def branchOffset(self, i):
        return _indata.indata_branchOffset(self, i)

    def nfeatures(self):
        return _indata.indata_nfeatures(self)

    def nelements(self):
        return _indata.indata_nelements(self)

    def vectorSize(self, idex):
        return _indata.indata_vectorSize(self, idex)

    __swig_setmethods__['buffer'] = _indata.indata_buffer_set
    __swig_getmethods__['buffer'] = _indata.indata_buffer_get
    if _newclass:
        buffer = _swig_property(_indata.indata_buffer_get, _indata.indata_buffer_set)
    __swig_setmethods__['buffervec'] = _indata.indata_buffervec_set
    __swig_getmethods__['buffervec'] = _indata.indata_buffervec_get
    if _newclass:
        buffervec = _swig_property(_indata.indata_buffervec_get, _indata.indata_buffervec_set)
    __swig_setmethods__['tbranches'] = _indata.indata_tbranches_set
    __swig_getmethods__['tbranches'] = _indata.indata_tbranches_get
    if _newclass:
        tbranches = _swig_property(_indata.indata_tbranches_get, _indata.indata_tbranches_set)
    __swig_setmethods__['offset_'] = _indata.indata_offset__set
    __swig_getmethods__['offset_'] = _indata.indata_offset__get
    if _newclass:
        offset_ = _swig_property(_indata.indata_offset__get, _indata.indata_offset__set)
    __swig_setmethods__['norms'] = _indata.indata_norms_set
    __swig_getmethods__['norms'] = _indata.indata_norms_get
    if _newclass:
        norms = _swig_property(_indata.indata_norms_get, _indata.indata_norms_set)
    __swig_setmethods__['means'] = _indata.indata_means_set
    __swig_getmethods__['means'] = _indata.indata_means_get
    if _newclass:
        means = _swig_property(_indata.indata_means_get, _indata.indata_means_set)
    __swig_setmethods__['branches'] = _indata.indata_branches_set
    __swig_getmethods__['branches'] = _indata.indata_branches_get
    if _newclass:
        branches = _swig_property(_indata.indata_branches_get, _indata.indata_branches_set)
    __swig_setmethods__['max'] = _indata.indata_max_set
    __swig_getmethods__['max'] = _indata.indata_max_get
    if _newclass:
        max = _swig_property(_indata.indata_max_get, _indata.indata_max_set)

    def setMask(self, m):
        return _indata.indata_setMask(self, m)


indata_swigregister = _indata.indata_swigregister
indata_swigregister(indata)
cvar = _indata.cvar

def createDataVector(s_branches, s_norms, s_means, s_max):
    return _indata.createDataVector(s_branches, s_norms, s_means, s_max)


createDataVector = _indata.createDataVector
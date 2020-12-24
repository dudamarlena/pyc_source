# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/Documents/kalliope/kalliope/trigger/snowboy/snowboydetect.py
# Compiled at: 2018-12-02 05:49:46
# Size of source mod 2**32: 4493 bytes
from kalliope.core.ConfigurationManager import SettingLoader
from sys import version_info
sl = SettingLoader()
settings = sl.settings
module_file_path = '%s/python%d%d/_snowboydetect' % (settings.machine, version_info[0], version_info[1])
if version_info >= (2, 6, 0):

    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module(module_file_path, [dirname(__file__)])
        except ImportError:
            import _snowboydetect
            return _snowboydetect
        else:
            if fp is not None:
                try:
                    _mod = imp.load_module('_snowboydetect', fp, pathname, description)
                finally:
                    fp.close()

                return _mod


    _snowboydetect = swig_import_helper()
    del swig_import_helper
else:
    import _snowboydetect
del version_info
try:
    _swig_property = property
except NameError:
    pass

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
            if static or _newclass:
                object.__setattr__(self, name, value)
            else:
                self.__dict__[name] = value
        else:
            raise AttributeError('You cannot add attributes to %s' % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if name == 'thisown':
        return self.this.own()
    else:
        method = class_type.__swig_getmethods__.get(name, None)
        if method:
            return method(self)
        else:
            return static or object.__getattr__(self, name)
    raise AttributeError(name)


def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except Exception:
        strthis = ''

    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


try:
    _object = object
    _newclass = 1
except AttributeError:

    class _object:
        pass


    _newclass = 0

class SnowboyDetect(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SnowboyDetect, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SnowboyDetect, name)
    __repr__ = _swig_repr

    def __init__(self, resource_filename, model_str):
        this = _snowboydetect.new_SnowboyDetect(resource_filename, model_str)
        try:
            self.this.append(this)
        except Exception:
            self.this = this

    def Reset(self):
        return _snowboydetect.SnowboyDetect_Reset(self)

    def RunDetection(self, *args):
        return (_snowboydetect.SnowboyDetect_RunDetection)(self, *args)

    def SetSensitivity(self, sensitivity_str):
        return _snowboydetect.SnowboyDetect_SetSensitivity(self, sensitivity_str)

    def GetSensitivity(self):
        return _snowboydetect.SnowboyDetect_GetSensitivity(self)

    def SetAudioGain(self, audio_gain):
        return _snowboydetect.SnowboyDetect_SetAudioGain(self, audio_gain)

    def UpdateModel(self):
        return _snowboydetect.SnowboyDetect_UpdateModel(self)

    def NumHotwords(self):
        return _snowboydetect.SnowboyDetect_NumHotwords(self)

    def SampleRate(self):
        return _snowboydetect.SnowboyDetect_SampleRate(self)

    def NumChannels(self):
        return _snowboydetect.SnowboyDetect_NumChannels(self)

    def BitsPerSample(self):
        return _snowboydetect.SnowboyDetect_BitsPerSample(self)

    __swig_destroy__ = _snowboydetect.delete_SnowboyDetect
    __del__ = lambda self: None


SnowboyDetect_swigregister = _snowboydetect.SnowboyDetect_swigregister
SnowboyDetect_swigregister(SnowboyDetect)
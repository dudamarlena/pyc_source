# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\PyFDP\__init__.py
# Compiled at: 2018-01-23 07:10:20
import os, sys, ctypes
if not sys.platform == 'win32':
    raise ValueError('The binding PyFDP cannot be used on a host that is not a native Windows machine')
import inspect
if not hasattr(sys.modules[__name__], '__file__'):
    __file__ = inspect.getfile(inspect.currentframe())
_found = False
FDP_DLL_HANDLE = None
package_dir = os.path.dirname(__file__)
try:
    is_64bits = sys.maxsize > 4294967296
    if is_64bits:
        _FDP_dll_name = 'FDP_x64.dll'
    else:
        _FDP_dll_name = 'FDP_x86.dll'
    _FDP_dll_path = os.path.join(package_dir, _FDP_dll_name)
    FDP_DLL_HANDLE = ctypes.cdll.LoadLibrary(_FDP_dll_path)
    _found = True
except OSError:
    pass

if _found == False or FDP_DLL_HANDLE == None:
    raise ImportError('ERROR: fail to load the dynamic library %s.' % _FDP_dll_path)
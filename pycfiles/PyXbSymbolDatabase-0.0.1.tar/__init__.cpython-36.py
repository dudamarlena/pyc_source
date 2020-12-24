# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mborgerson/Projects/xbox/xbe/PyXbSymbolDatabase/XbSymbolDatabase/__init__.py
# Compiled at: 2020-01-08 15:08:53
# Size of source mod 2**32: 809 bytes
import ctypes, os.path, platform
libname = 'libXbSymbolDatabase'
osname = platform.system()
if osname == 'Linux':
    libname += '.so'
else:
    if osname == 'Darwin':
        libname += '.dylib'
    else:
        if osname == 'Windows':
            libname += '.dll'
        else:
            assert False, 'Unknown platform'
libpath = os.path.join(os.path.dirname(__file__), libname)
lib = ctypes.cdll.LoadLibrary(libpath)

def get_symbols(xbe):
    symbols = []
    cb_wrap = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32)

    def cb(library_str, library_flag, symbol_str, address, build_verison):
        symbols.append((library_str, library_flag, symbol_str, address, build_verison))

    lib.XbSymbolScan(xbe, cb_wrap(cb), True)
    return symbols
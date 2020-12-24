# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modules/go_linker.py
# Compiled at: 2018-07-01 07:06:03
# Size of source mod 2**32: 735 bytes
import os.path
from ctypes import cdll, c_char_p, c_longlong, c_int, Structure
dll_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'go_get_urls.so'
go_linker = cdll.LoadLibrary(dll_path)

class GoString(Structure):
    _fields_ = [
     (
      'p', c_char_p), ('n', c_longlong)]


go_linker.GetLinks.argtypes = [
 GoString, GoString, GoString, c_int, c_int]

def GetLinks(url, addr, port, timeout, extensions):
    url = url.encode('utf-8')
    addr = addr.encode('utf-8')
    port = str(port).encode('utf-8')
    go_linker.GetLinks(GoString(url, len(url)), GoString(addr, len(addr)), GoString(port, len(port)), timeout, extensions)
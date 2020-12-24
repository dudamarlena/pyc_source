# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hashdb/hashdb_mntent.py
# Compiled at: 2011-01-06 01:19:27
import ctypes, ctypes.util

class mntent(ctypes.Structure):
    _fields_ = [
     (
      'mnt_fsname', ctypes.c_char_p),
     (
      'mnt_dir', ctypes.c_char_p),
     (
      'mnt_type', ctypes.c_char_p),
     (
      'mnt_opts', ctypes.c_char_p),
     (
      'mnt_freq', ctypes.c_int),
     (
      'mnt_passno', ctypes.c_int)]


mntent_p = ctypes.POINTER(mntent)
libc = ctypes.CDLL(ctypes.util.find_library('c'))
setmntent = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p)(('setmntent', libc), ((1, 'file'), (1, 'mode', 'rt')))
endmntent = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)(('endmntent', libc), ((1, 'stream'), ))
getmntent = ctypes.CFUNCTYPE(mntent_p, ctypes.c_void_p)(('getmntent', libc), ((1, 'stream'), ))
getmntent_r = ctypes.CFUNCTYPE(mntent_p, ctypes.c_void_p, mntent_p, ctypes.c_void_p, ctypes.c_int)(('getmntent_r', libc), ((1, 'stream'), (1, 'result'), (1, 'buffer'), (1, 'bufsize')))
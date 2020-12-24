# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/google/home/bcongdon/Documents/OpenSource/bpy_lambda/bpy_lambda/__init__.py
# Compiled at: 2020-02-19 11:10:25
import ctypes, os
lib_dir = os.path.dirname(os.path.realpath(__file__))
LIBRARIES = [
 'libHalf.so.12',
 'libIex.so.12',
 'libImath.so.12',
 'libIlmThread.so.12',
 'libIlmImf.so.22',
 'libboost_system.so.1.60.0',
 'libboost_filesystem.so.1.60.0',
 'libboost_regex.so.1.60.0',
 'libboost_thread.so.1.60.0',
 'libpython3.6m.so.1.0',
 'libGLU.so.1',
 'libopenjpeg.so.2',
 'libOpenImageIO.so.1.7']
for lib in LIBRARIES:
    print os.path.join(lib_dir, lib)
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, lib))

from . import bpy
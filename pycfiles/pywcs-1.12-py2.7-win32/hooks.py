# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywcs\hooks.py
# Compiled at: 2014-03-13 12:23:51
"""
To compile another package that wants to link with the C code in pywcs:

[build_ext]
pre-hook.pywcs = pywcs.hooks.setup

[extension=drizzlepac.cdriz]
include_dirs = numpy pywcs
libraries = pywcs m

"""
import os

def setup(command_obj):
    command_name = command_obj.get_command_name()
    if command_name != 'build_ext':
        log.warn('%s is meant to be used with the build_ext command only; it is not for use with the %s command.' % (
         __name__, command_name))
    import pywcs
    pywcslib = pywcs.__path__[0]
    includes = [os.path.join(pywcslib, 'include'),
     os.path.join(pywcslib, 'include', 'wcslib')]
    for extension in command_obj.extensions:
        if 'pywcs' not in extension.include_dirs:
            continue
        idx = extension.include_dirs.index('pywcs')
        for inc in includes:
            extension.include_dirs.insert(idx, inc)

        extension.include_dirs.remove('pywcs')
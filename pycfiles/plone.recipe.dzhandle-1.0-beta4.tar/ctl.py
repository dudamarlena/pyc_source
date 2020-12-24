# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/recipe/deliverance/ctl.py
# Compiled at: 2007-06-19 18:43:35
__doc__ = 'Run Deliverance with an appropriately configured environment\n'
import os, sys

def main(args=None):
    lib_path = args[0]
    paster = args[1]
    ini_path = args[2]
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.pathsep.join(sys.path)
    if lib_path:
        env['DYLD_LIBRARY_PATH'] = env['LD_LIBRARY_PATH'] = lib_path
    os.execve(paster, [paster, 'serve', ini_path] + args[3:], env)
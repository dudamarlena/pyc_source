# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/recipe/deliverance/ctl.py
# Compiled at: 2007-06-19 18:43:35
"""Run Deliverance with an appropriately configured environment
"""
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
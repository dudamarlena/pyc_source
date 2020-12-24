# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\fortran.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.fortran

Tool-specific initialization for a generic Posix f77/f90 Fortran compiler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/fortran.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import re, SCons.Action, SCons.Defaults, SCons.Scanner.Fortran, SCons.Tool, SCons.Util
from SCons.Tool.FortranCommon import add_all_to_env, add_fortran_to_env
compilers = [
 'f95', 'f90', 'f77']

def generate(env):
    add_all_to_env(env)
    add_fortran_to_env(env)
    fc = env.Detect(compilers) or 'f77'
    env['SHFORTRAN'] = fc
    env['FORTRAN'] = fc


def exists(env):
    return env.Detect(compilers)
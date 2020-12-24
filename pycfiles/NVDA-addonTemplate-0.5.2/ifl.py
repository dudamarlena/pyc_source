# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\ifl.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.ifl

Tool-specific initialization for the Intel Fortran compiler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/ifl.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Defaults
from SCons.Scanner.Fortran import FortranScan
from FortranCommon import add_all_to_env

def generate(env):
    """Add Builders and construction variables for ifl to an Environment."""
    fscan = FortranScan('FORTRANPATH')
    SCons.Tool.SourceFileScanner.add_scanner('.i', fscan)
    SCons.Tool.SourceFileScanner.add_scanner('.i90', fscan)
    if 'FORTRANFILESUFFIXES' not in env:
        env['FORTRANFILESUFFIXES'] = [
         '.i']
    else:
        env['FORTRANFILESUFFIXES'].append('.i')
    if 'F90FILESUFFIXES' not in env:
        env['F90FILESUFFIXES'] = [
         '.i90']
    else:
        env['F90FILESUFFIXES'].append('.i90')
    add_all_to_env(env)
    env['FORTRAN'] = 'ifl'
    env['SHFORTRAN'] = '$FORTRAN'
    env['FORTRANCOM'] = '$FORTRAN $FORTRANFLAGS $_FORTRANINCFLAGS /c $SOURCES /Fo$TARGET'
    env['FORTRANPPCOM'] = '$FORTRAN $FORTRANFLAGS $CPPFLAGS $_CPPDEFFLAGS $_FORTRANINCFLAGS /c $SOURCES /Fo$TARGET'
    env['SHFORTRANCOM'] = '$SHFORTRAN $SHFORTRANFLAGS $_FORTRANINCFLAGS /c $SOURCES /Fo$TARGET'
    env['SHFORTRANPPCOM'] = '$SHFORTRAN $SHFORTRANFLAGS $CPPFLAGS $_CPPDEFFLAGS $_FORTRANINCFLAGS /c $SOURCES /Fo$TARGET'


def exists(env):
    return env.Detect('ifl')
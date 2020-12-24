# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\cvf.py
# Compiled at: 2016-07-07 03:21:33
"""engine.SCons.Tool.cvf

Tool-specific initialization for the Compaq Visual Fortran compiler.

"""
__revision__ = 'src/engine/SCons/Tool/cvf.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import fortran
compilers = [
 'f90']

def generate(env):
    """Add Builders and construction variables for compaq visual fortran to an Environment."""
    fortran.generate(env)
    env['FORTRAN'] = 'f90'
    env['FORTRANCOM'] = '$FORTRAN $FORTRANFLAGS $_FORTRANMODFLAG $_FORTRANINCFLAGS /compile_only ${SOURCES.windows} /object:${TARGET.windows}'
    env['FORTRANPPCOM'] = '$FORTRAN $FORTRANFLAGS $CPPFLAGS $_CPPDEFFLAGS $_FORTRANMODFLAG $_FORTRANINCFLAGS /compile_only ${SOURCES.windows} /object:${TARGET.windows}'
    env['SHFORTRANCOM'] = '$SHFORTRAN $SHFORTRANFLAGS $_FORTRANMODFLAG $_FORTRANINCFLAGS /compile_only ${SOURCES.windows} /object:${TARGET.windows}'
    env['SHFORTRANPPCOM'] = '$SHFORTRAN $SHFORTRANFLAGS $CPPFLAGS $_CPPDEFFLAGS $_FORTRANMODFLAG $_FORTRANINCFLAGS /compile_only ${SOURCES.windows} /object:${TARGET.windows}'
    env['OBJSUFFIX'] = '.obj'
    env['FORTRANMODDIR'] = '${TARGET.dir}'
    env['FORTRANMODDIRPREFIX'] = '/module:'
    env['FORTRANMODDIRSUFFIX'] = ''


def exists(env):
    return env.Detect(compilers)
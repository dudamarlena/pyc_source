# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\gfortran.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.gfortran

Tool-specific initialization for gfortran, the GNU Fortran 95/Fortran
2003 compiler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/gfortran.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Util, fortran

def generate(env):
    """Add Builders and construction variables for gfortran to an
    Environment."""
    fortran.generate(env)
    for dialect in ['F77', 'F90', 'FORTRAN', 'F95', 'F03', 'F08']:
        env['%s' % dialect] = 'gfortran'
        env['SH%s' % dialect] = '$%s' % dialect
        if env['PLATFORM'] in ('cygwin', 'win32'):
            env['SH%sFLAGS' % dialect] = SCons.Util.CLVar('$%sFLAGS' % dialect)
        else:
            env['SH%sFLAGS' % dialect] = SCons.Util.CLVar('$%sFLAGS -fPIC' % dialect)
        env['INC%sPREFIX' % dialect] = '-I'
        env['INC%sSUFFIX' % dialect] = ''


def exists(env):
    return env.Detect('gfortran')
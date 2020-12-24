# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\initscripts\ConsoleSetLibPath.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 1949 bytes
import os, sys, BUILD_CONSTANTS
FILE_NAME = sys.executable
DIR_NAME = os.path.dirname(sys.executable)
paths = os.environ.get('LD_LIBRARY_PATH', '').split(os.pathsep)
if DIR_NAME not in paths:
    paths.insert(0, DIR_NAME)
    os.environ['LD_LIBRARY_PATH'] = os.pathsep.join(paths)
    os.execv(sys.executable, sys.argv)
sys.frozen = True
sys.path = sys.path[:4]
if hasattr(BUILD_CONSTANTS, 'TCL_LIBRARY'):
    os.environ['TCL_LIBRARY'] = os.path.join(DIR_NAME, BUILD_CONSTANTS.TCL_LIBRARY)
if hasattr(BUILD_CONSTANTS, 'TK_LIBRARY'):
    os.environ['TK_LIBRARY'] = os.path.join(DIR_NAME, BUILD_CONSTANTS.TK_LIBRARY)
if hasattr(BUILD_CONSTANTS, 'MATPLOTLIBDATA'):
    os.environ['MATPLOTLIBDATA'] = os.path.join(DIR_NAME, BUILD_CONSTANTS.MATPLOTLIBDATA)
if hasattr(BUILD_CONSTANTS, 'PYTZ_TZDATADIR'):
    os.environ['PYTZ_TZDATADIR'] = os.path.join(DIR_NAME, BUILD_CONSTANTS.PYTZ_TZDATADIR)

def run():
    name, ext = os.path.splitext(os.path.basename(os.path.normcase(FILE_NAME)))
    moduleName = '%s__main__' % name
    code = __loader__.get_code(moduleName)
    exec(code, {'__name__': '__main__'})
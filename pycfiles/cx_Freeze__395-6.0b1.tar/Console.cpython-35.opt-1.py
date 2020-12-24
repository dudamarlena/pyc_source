# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\initscripts\Console.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 1363 bytes
import os, sys, BUILD_CONSTANTS
sys.frozen = True
FILE_NAME = sys.executable
DIR_NAME = os.path.dirname(sys.executable)
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
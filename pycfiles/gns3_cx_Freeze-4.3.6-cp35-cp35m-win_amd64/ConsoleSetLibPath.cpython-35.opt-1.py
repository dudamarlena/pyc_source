# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\initscripts\ConsoleSetLibPath.py
# Compiled at: 2016-04-18 03:12:47
# Size of source mod 2**32: 1604 bytes
import os, sys, zipimport
paths = os.environ.get('LD_LIBRARY_PATH', '').split(os.pathsep)
if DIR_NAME not in paths:
    paths.insert(0, DIR_NAME)
    os.environ['LD_LIBRARY_PATH'] = os.pathsep.join(paths)
    os.execv(sys.executable, sys.argv)
sys.frozen = True
sys.path = sys.path[:4]
os.environ['TCL_LIBRARY'] = os.path.join(DIR_NAME, 'tcl')
os.environ['TK_LIBRARY'] = os.path.join(DIR_NAME, 'tk')
m = __import__('__main__')
importer = zipimport.zipimporter(INITSCRIPT_ZIP_FILE_NAME)
if INITSCRIPT_ZIP_FILE_NAME != SHARED_ZIP_FILE_NAME:
    moduleName = m.__name__
else:
    name, ext = os.path.splitext(os.path.basename(os.path.normcase(FILE_NAME)))
    moduleName = '%s__main__' % name
code = importer.get_code(moduleName)
exec(code, m.__dict__)
versionInfo = sys.version_info[:3]
if versionInfo >= (2, 5, 0) and versionInfo <= (2, 6, 4):
    module = sys.modules.get('threading')
    if module is not None:
        module._shutdown()
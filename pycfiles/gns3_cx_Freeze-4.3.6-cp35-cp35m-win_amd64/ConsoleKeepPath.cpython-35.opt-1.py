# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\initscripts\ConsoleKeepPath.py
# Compiled at: 2016-04-18 03:20:12
# Size of source mod 2**32: 661 bytes
import sys, zipimport
m = __import__('__main__')
importer = zipimport.zipimporter(INITSCRIPT_ZIP_FILE_NAME)
code = importer.get_code(m.__name__)
exec(code, m.__dict__)
versionInfo = sys.version_info[:3]
if versionInfo >= (2, 5, 0) and versionInfo <= (2, 6, 4):
    module = sys.modules.get('threading')
    if module is not None:
        module._shutdown()
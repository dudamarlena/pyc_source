# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\examples\test_nonexistent_folder_in_pythonpath.py
# Compiled at: 2013-01-25 10:29:31
import sys, shutil, os
tempdir = 'c:/temp/temp'
try:
    import folder.module
    print folder.module
except ImportError:
    pass

sys.path.append(tempdir)
try:
    import folder.module
    print folder.module
except ImportError:
    pass

os.makedirs(os.path.join(tempdir, 'folder'))
with open(os.path.join(tempdir, 'folder', '__init__.py'), 'w') as (f):
    pass
with open(os.path.join(tempdir, 'folder', 'module.py'), 'w') as (f):
    f.write("print 'Importing module'")
import folder.module
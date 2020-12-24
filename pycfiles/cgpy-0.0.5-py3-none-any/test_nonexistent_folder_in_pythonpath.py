# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pyrep/test.py
# Compiled at: 2019-02-12 09:44:40
# Size of source mod 2**32: 6428 bytes
from __future__ import print_function
import os, warnings
from pprint import pprint
import numpy as np
from pyrep import Repository
REP = Repository()
PATH = os.path.join(os.path.expanduser('~'), 'pyrepTest_canBeDeleted')
if REP.is_repository(PATH):
    REP.remove_repository(path=PATH, removeEmptyDirs=True)
print('repository path --> %s' % str(REP.path))
print()
print("\\nIs path '%s' a repository --> %s" % (PATH, str(REP.is_repository(PATH))))
success, message = REP.create_repository(PATH)
assert success, message
print('\\nRepository path --> %s' % str(REP.path))
print()
success, message = REP.add_directory('folder1/folder2/folder3')
if not success:
    print(message)
success, message = REP.add_directory('folder1/archive1/archive2/archive3/archive3')
if not success:
    print(message)
success, message = REP.add_directory('directory1/directory2')
if not success:
    print(message)
value = 'This is a string data to pickle and store in the repository'
success, message = REP.dump_file(value, relativePath='pickled', dump=None, pull=None, replace=True)
if not success:
    print(message)
value = np.random.random(3)
dump = "import numpy as np; np.savetxt(fname='$FILE_PATH', X=value, fmt='%.6e')"
pull = "import numpy as np; PULLED_DATA=np.loadtxt(fname='$FILE_PATH')"
success, message = REP.dump(value, relativePath='text.dat', dump=dump, pull=pull, replace=True)
if not success:
    print(message)
success, message = REP.dump(value, relativePath='folder1/folder2/folder3/folder3Pickled.pkl', replace=True)
if not success:
    print(message)
success, message = REP.dump(value, relativePath='folder1/archive1/archive1Pickled1', replace=True)
if not success:
    print(message)
success, message = REP.dump(value, relativePath='folder1/archive1/archive1Pickled2', replace=True)
if not success:
    print(message)
success, message = REP.dump(value, relativePath='folder1/archive1/archive2/archive2Pickled1', replace=True)
if not success:
    print(message)
data = REP.pull(relativePath='text.dat')
print('\\nPulled text data --> %s' % str(data))
print()
data = REP.pull(relativePath='folder1/folder2/folder3/folder3Pickled.pkl')
print('\\nPulled pickled data --> %s' % str(data))
print()
value = 'This is an updated string'
REP.update(value, relativePath='pickled')
print('\\nUpdate pickled data to --> %s' % value)
print()
print('\\nwalk repository files relative path')
print('------------------------------------')
for f in REP.walk_files_path(recursive=True):
    print(f)

print()
print('\\nwalk repository directories relative path')
print('------------------------------------------')
for d in REP.walk_directories_path(recursive=True):
    print(d)

print()
print('\\nRepository print -->')
print(REP)
print()
print('\\nRepository representation -->')
print(repr(REP))
print()
print('\\nRepository to list -->')
for fdDict in REP.get_repository_state():
    k = list(fdDict)[0]
    print('%s: %s' % (k, str(fdDict[k])))

print()
print('\\nCreate package from repository ...')
REP.create_package(path=None, name=None)
print()
try:
    try:
        REP.load_repository(PATH)
    except:
        loadable = False

finally:
    loadable = True

print('\\nIs repository loadable -->', loadable)
print()
print('\\Copy folder1 to copied_folder1 ...')
import time
p0 = 'folder1'
p1 = 'copied_folder1'
for i in range(1, 11):
    tic = time.time()
    REP.copy_directory(relativePath=p0, newRelativePath=p1, overwrite=True, raiseError=True)
    p1 = os.path.join('copied_folder%i' % (i + 1), p1)
    print(time.time() - tic)

print(REP)
print("\\nIs path '%s' a repository --> %s" % (PATH, str(REP.is_repository(PATH))))
print()
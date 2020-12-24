# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/serge/Dropbox/p/pysal/src/subpackages/spvcm/spvcm/examples/__init__.py
# Compiled at: 2018-06-25 20:39:36
# Size of source mod 2**32: 559 bytes
import os as _os

def available():
    dcty = _os.path.dirname(_os.path.abspath(__file__))
    files = _os.listdir(dcty)
    unique_names = {_os.path.splitext(f)[0]:[] for f in files if not _os.path.splitext(f)[0].startswith('__init__') if not _os.path.splitext(f)[0].startswith('__init__')}
    for f in files:
        filename = _os.path.splitext(f)[0]
        if filename not in unique_names:
            continue
        unique_names[filename].append(f)

    print('The following examples are stored in the examples directory\n{}'.format(dcty))
    print(unique_names)
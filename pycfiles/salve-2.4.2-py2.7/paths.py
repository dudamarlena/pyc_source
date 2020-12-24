# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/tests/util/paths.py
# Compiled at: 2015-11-06 23:45:35
from salve import paths
testfile_dir = paths.pjoin(paths.containing_dir(__file__, depth=2), 'testfiles')

def full_path(filename):
    return paths.pjoin(testfile_dir, filename)
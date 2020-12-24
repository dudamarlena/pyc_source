# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Finder/PathFinder.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 1932 bytes
import os

def resolveFilePathForReference(project, reference) -> str:
    file_path = reference.resolvePath(project)
    project_dir = os.path.dirname(os.path.dirname(project.pbx_file_path))
    file_path = os.path.join(project_dir, file_path)
    norm_file_path = os.path.normpath(file_path)
    return norm_file_path
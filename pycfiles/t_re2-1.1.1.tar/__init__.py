# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: re2/__init__.py
# Compiled at: 2020-05-06 00:40:33
import os, shutil
dependent_files = '/usr/local/lib/libre2.so.7'
if not os.path.isfile(dependent_files):
    if not os.path.exists(os.path.dirname(dependent_files)):
        os.makedirs(os.path.dirname(dependent_files))
    shutil.copy2('./re2/libre2.so.7', dependent_files)
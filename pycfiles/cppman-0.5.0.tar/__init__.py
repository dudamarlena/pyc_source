# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aitjcize/Work/cppman/cppman/__init__.py
# Compiled at: 2018-08-18 07:47:23
import os
package_dir = os.path.dirname(__file__)

def get_lib_path(filename):
    return os.path.join(package_dir, 'lib', filename)
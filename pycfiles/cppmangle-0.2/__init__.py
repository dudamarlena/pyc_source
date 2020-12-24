# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aitjcize/Work/cppman/cppman/__init__.py
# Compiled at: 2018-08-18 07:47:23
import os
package_dir = os.path.dirname(__file__)

def get_lib_path(filename):
    return os.path.join(package_dir, 'lib', filename)
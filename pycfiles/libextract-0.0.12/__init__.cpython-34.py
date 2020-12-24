# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\rodrigo\github\libextract\libextract\tests\__init__.py
# Compiled at: 2015-04-06 21:50:02
# Size of source mod 2**32: 185 bytes
import os

def asset_path(filename, asset_dir='assets'):
    return os.path.join(os.path.dirname(__file__), asset_dir, filename)
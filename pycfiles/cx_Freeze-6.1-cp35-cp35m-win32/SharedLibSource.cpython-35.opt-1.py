# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\initscripts\SharedLibSource.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 1026 bytes
import os, sys, warnings
__import__('site')
baseName, ext = os.path.splitext(FILE_NAME)
pathFileName = baseName + '.pth'
with open(pathFileName) as (in_file):
    sys.path = [s.strip() for s in in_file.read().splitlines()] + sys.path

def run():
    pass
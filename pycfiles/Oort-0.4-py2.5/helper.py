# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/test/helper.py
# Compiled at: 2007-09-30 16:00:20
from os import path

def siblingpath(filepath, filename):
    return path.join(path.dirname(filepath), filename)
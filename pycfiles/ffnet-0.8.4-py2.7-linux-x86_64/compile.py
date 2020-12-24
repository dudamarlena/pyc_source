# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ffnet/fortran/compile.py
# Compiled at: 2018-10-28 11:56:52
from __future__ import print_function
from numpy import f2py
import os
files = os.listdir('.')
for file in files:
    name, ext = os.path.splitext(file)
    if ext == '.f':
        print(('Compiling file {}.').format(file))
        f2py.compile(open(file, 'rb').read(), '_' + name)
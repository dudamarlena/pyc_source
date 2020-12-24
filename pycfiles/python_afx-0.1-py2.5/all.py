# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/afx/all.py
# Compiled at: 2007-05-20 20:58:00
import __init__
for pkg in __init__.__all__:
    exec 'from ' + pkg + ' import *'
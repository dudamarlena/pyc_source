# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipyplot/utils/indent.py
# Compiled at: 2016-09-23 20:21:54
"""
Created on Thu Apr 23 11:00:45 2015

@author: calandra
"""
from __future__ import print_function

def indent(depth=0):
    print('    ' * depth, end='')
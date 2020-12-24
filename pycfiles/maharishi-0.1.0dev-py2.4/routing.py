# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/maharishi/config/routing.py
# Compiled at: 2006-08-30 12:42:38
"""
Setup your Routes options here
"""
import sys, os
from routes import Mapper

def make_map():
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    map = Mapper(directory=os.path.join(root_path, 'controllers'))
    map.connect('', controller='hello', action='index')
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')
    return map
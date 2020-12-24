# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/www/config/routing.py
# Compiled at: 2007-04-18 06:57:54
"""
Setup your Routes options here
"""
import os
from routes import Mapper

def make_map(global_conf={}, app_conf={}):
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    map = Mapper(directory=os.path.join(root_path, 'controllers'))
    map.connect('error/:action/:id', controller='error')
    map.connect('', controller='root', action='index')
    map.connect(':action', controller='root')
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')
    return map
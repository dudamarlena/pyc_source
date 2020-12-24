# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mareike/work/app/pyrap-dev/python3/pyrap/locations.py
# Compiled at: 2018-02-16 08:54:48
"""
Created on Oct 2, 2015

@author: nyga
"""
import os, pyrap
pyrap_path = os.path.normpath(os.path.join(os.path.dirname(pyrap.__file__), '..'))
if os.path.basename(pyrap_path).startswith('python'):
    pyrap_path = os.path.normpath(os.path.join(pyrap_path, '..'))
code_base = os.path.normpath(os.path.join(os.path.dirname(pyrap.__file__), '..'))
js_loc = os.path.realpath(os.path.join(pyrap_path, 'js'))
html_loc = os.path.join(pyrap_path, 'html')
css_loc = os.path.join(pyrap_path, 'css')
rc_loc = os.path.join(pyrap_path, 'resource')
pwt_loc = os.path.join(code_base, 'pyrap', 'pwt')
trdparty = os.path.join(pyrap_path, '3rdparty')
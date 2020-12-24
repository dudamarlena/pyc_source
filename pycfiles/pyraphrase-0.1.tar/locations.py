# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mareike/work/app/pyrap-dev/python3/pyrap/locations.py
# Compiled at: 2018-02-16 08:54:48
__doc__ = '\nCreated on Oct 2, 2015\n\n@author: nyga\n'
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
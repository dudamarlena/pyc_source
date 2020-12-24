# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/__init__.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 1081 bytes
"""
`blowdrycss` is a rapid styling tool that compiles DRY CSS from encoded class selectors in your web project files.

"""
from __future__ import absolute_import
import sys, os
from blowdrycss.settingsbuilder import write_blowdrycss_settings_dot_py
cwd = os.getcwd()
if not os.path.isfile('blowdrycss_settings.py'):
    if not cwd.endswith('docs'):
        write_blowdrycss_settings_dot_py()
sys.path.insert(0, cwd)
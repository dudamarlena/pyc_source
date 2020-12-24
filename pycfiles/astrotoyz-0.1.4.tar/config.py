# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data-beta/users/fmooleka/git_projects/astro-toyz/astrotoyz/config.py
# Compiled at: 2015-08-05 16:53:39
"""
Configuration file required for all new Toyz
"""
from __future__ import division, print_function
import os, astrotoyz.io
root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
static_paths = [
 os.path.join(root, 'static')]
template_paths = [os.path.join(root, 'templates')]
workspace_tiles = {'astro_viewer': {'name': 'Astro Viewer', 
                    'namespace': 'Toyz.Astro.Viewer', 
                    'url': '/toyz/static/astrotoyz/viewer.js'}}
toyz_urls = {}
render_functions = {}
io_modules = astrotoyz.io.io_modules
load_functions = {'astropy_read': astrotoyz.io.astropy_read}
save_functions = {'astropy_write': astrotoyz.io.astropy_write}
src_types = {'AstropyTable': astrotoyz.data_types.astropy_table.AstropyTable}
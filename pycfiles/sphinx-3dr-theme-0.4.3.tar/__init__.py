# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rroche/Work/DroneKit/sphinx_3dr_theme/sphinx_3dr_theme/__init__.py
# Compiled at: 2015-11-30 13:22:35
import os
VERSION = (0, 4, 3)
__version__ = ('.').join(str(v) for v in VERSION)
__version_full__ = __version__

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return cur_dir
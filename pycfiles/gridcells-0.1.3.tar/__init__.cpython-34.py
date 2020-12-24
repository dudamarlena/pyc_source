# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukas/work/development/gridcells/external/sphinx_rtd_theme/sphinx_rtd_theme/__init__.py
# Compiled at: 2014-03-30 05:58:06
# Size of source mod 2**32: 371 bytes
"""Sphinx ReadTheDocs theme.

From https://github.com/ryan-roemer/sphinx-bootstrap-theme.

"""
import os
VERSION = (0, 1, 5)
__version__ = '.'.join(str(v) for v in VERSION)
__version_full__ = __version__

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return cur_dir
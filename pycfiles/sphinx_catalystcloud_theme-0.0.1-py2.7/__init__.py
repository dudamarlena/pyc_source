# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sphinx_catalystcloud_theme/__init__.py
# Compiled at: 2017-09-10 21:38:18
import os
__version__ = '0.0.1'
__version_full__ = __version__

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return cur_dir


def setup(app):
    app.add_html_theme('sphinx_catalystcloud_theme', os.path.abspath(os.path.dirname(__file__)))
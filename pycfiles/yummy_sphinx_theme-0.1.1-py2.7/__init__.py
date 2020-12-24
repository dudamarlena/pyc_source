# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yummy_sphinx_theme/__init__.py
# Compiled at: 2019-09-08 16:33:27
"""
Yummy Sphinx Theme, created to mirror Yummy-Jekyll for sphinx
"""
from os import path
__version__ = '0.1.1'

def get_path():
    """Return list of HTML theme paths."""
    return path.abspath(path.dirname(path.dirname(__file__)))


def setup(app):
    app.add_html_theme('yummy_sphinx_theme', path.abspath(path.dirname(__file__)))
    return {'version': __version__}
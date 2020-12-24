# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ignacy/workspace/sphinx-readable-theme/src/sphinx_readable_theme/__init__.py
# Compiled at: 2015-03-27 04:48:14
"""Sphinx Readable Theme.

A clean and readable Sphinx theme with focus on `autodoc` -- documentation
from docstrings.

"""
import os
__version__ = '1.3.0'

def get_html_theme_path():
    """Return path to directory containing package theme."""
    return os.path.abspath(os.path.dirname(__file__))
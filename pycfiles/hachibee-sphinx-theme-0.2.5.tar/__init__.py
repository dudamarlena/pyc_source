# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dogura/Dropbox/development/python/Sphinx-hachibee-theme/src/hachibee_sphinx_theme/__init__.py
# Compiled at: 2013-12-03 03:52:29
""" """
import os
from sphinx.builders.html import StandaloneHTMLBuilder

def get_html_themes_path():
    """Return list of sphinx themes."""
    here = os.path.abspath(os.path.dirname(__file__))
    return here


def setup(app):
    pass
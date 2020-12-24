# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marble/Repositories/github.com/TYPO3-Documentation/t3SphinxThemeRtd/t3SphinxThemeRtd/__init__.py
# Compiled at: 2018-07-04 09:56:48
# Size of source mod 2**32: 1451 bytes
"""Sphinx ReadTheDocs theme.

From https://github.com/ryan-roemer/sphinx-bootstrap-theme.

"""
import os
VERSION = (3, 6, 15)
__version__ = '.'.join(str(v) for v in VERSION)
__version_full__ = __version__

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return cur_dir


def htmlPageContext(app, pagename, templatename, context, doctree):
    template = app.builder.env.metadata.get(pagename, {}).get('template')
    return template


def setup(app):
    app.connect('html-page-context', htmlPageContext)
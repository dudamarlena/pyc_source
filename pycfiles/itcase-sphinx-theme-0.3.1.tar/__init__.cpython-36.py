# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/ITCase/itcase_sphinx_theme/itcase_sphinx_theme/__init__.py
# Compiled at: 2015-08-12 01:04:40
# Size of source mod 2**32: 442 bytes
import os, pkg_resources

def get_html_themes_path():
    """Return list of sphinx themes."""
    return os.path.abspath(os.path.dirname(__file__))


def update_context(app, pagename, templatename, context, doctree):
    version = pkg_resources.get_distribution('itcase_sphinx_theme').version
    context['theme_version'] = version


def setup(app):
    app.connect('html-page-context', update_context)
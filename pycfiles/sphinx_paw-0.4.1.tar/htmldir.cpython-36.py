# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amarin/dev/sphinx-mediatel/src/sphinx_paw/builders/htmldir.py
# Compiled at: 2019-11-19 10:51:04
# Size of source mod 2**32: 2120 bytes
"""Configure HTML builder's options"""
from sphinx.application import Sphinx
from sphinx_paw.configurable import ConfigFile
from sphinx_paw.configurable import set_config_value
from sphinx_paw.constants import BUILDER_HTML_SECTION
from sphinx_paw.utils import get_private_section_name

def init_html(app, config):
    """Configure HTML and HTML Help builder options"""
    if not isinstance(app, Sphinx):
        raise AssertionError
    else:
        assert isinstance(config, ConfigFile)
        private_section_name = get_private_section_name(config, BUILDER_HTML_SECTION)
        if not config.has_section(private_section_name):
            return
    set_config_value(app, 'html_theme', 'sphinx_rtd_theme')
    set_config_value(app, 'html_static_path', ['_static'])
    set_config_value(app, 'html_context', {'css_files': ['_static/tables.css']})
    html_sidebars = {'**': [
            'relations.html',
            'searchbox.html']}
    set_config_value(app, 'html_sidebars', html_sidebars)
    html_baseurl = '/'
    set_config_value(app, 'html_baseurl', html_baseurl)
    html_copy_source = False
    set_config_value(app, 'html_copy_source', html_copy_source)
    html_show_sourcelink = False
    set_config_value(app, 'html_show_sourcelink', html_show_sourcelink)
    html_link_suffix = '.html'
    set_config_value(app, 'html_link_suffix', html_link_suffix)
    html_show_sphinx = False
    set_config_value(app, 'html_show_sphinx', html_show_sphinx)
    html_search_language = 'ru'
    set_config_value(app, 'html_search_language', html_search_language)
    html_show_copyright = False
    set_config_value(app, 'html_show_copyright', html_show_copyright)
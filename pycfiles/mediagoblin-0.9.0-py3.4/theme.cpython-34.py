# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/theme.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 2777 bytes
"""
"""
import pkg_resources, os
from configobj import ConfigObj
BUILTIN_THEME_DIR = pkg_resources.resource_filename('mediagoblin', 'themes')

def themedata_for_theme_dir(name, theme_dir):
    """
    Given a theme directory, extract important theme information.
    """
    config = ConfigObj(os.path.join(theme_dir, 'theme.ini')).get('theme', {})
    templates_dir = os.path.join(theme_dir, 'templates')
    if not os.path.exists(templates_dir):
        templates_dir = None
    assets_dir = os.path.join(theme_dir, 'assets')
    if not os.path.exists(assets_dir):
        assets_dir = None
    themedata = {'name': config.get('name', name), 
     'description': config.get('description'), 
     'licensing': config.get('licensing'), 
     'dir': theme_dir, 
     'templates_dir': templates_dir, 
     'assets_dir': assets_dir, 
     'config': config}
    return themedata


def register_themes(app_config, builtin_dir=BUILTIN_THEME_DIR):
    """
    Register all themes relevant to this application.
    """
    registry = {}

    def _install_themes_in_dir(directory):
        for themedir in os.listdir(directory):
            abs_themedir = os.path.join(directory, themedir)
            if not os.path.isdir(abs_themedir):
                continue
            themedata = themedata_for_theme_dir(themedir, abs_themedir)
            registry[themedir] = themedata

    if os.path.exists(builtin_dir):
        _install_themes_in_dir(builtin_dir)
    theme_install_dir = app_config.get('theme_install_dir')
    if theme_install_dir:
        if os.path.exists(theme_install_dir):
            _install_themes_in_dir(theme_install_dir)
    current_theme_name = app_config.get('theme')
    if current_theme_name and registry.has_key(current_theme_name):
        current_theme = registry[current_theme_name]
    else:
        current_theme = None
    return (registry, current_theme)
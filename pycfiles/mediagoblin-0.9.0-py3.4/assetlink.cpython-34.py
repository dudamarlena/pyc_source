# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/gmg_commands/assetlink.py
# Compiled at: 2013-09-23 12:05:50
# Size of source mod 2**32: 5379 bytes
import os
from mediagoblin import mg_globals
from mediagoblin.init import setup_global_and_app_config
from mediagoblin.gmg_commands import util as commands_util
from mediagoblin.tools.theme import register_themes
from mediagoblin.tools.translate import pass_to_ugettext as _
from mediagoblin.tools.common import simple_printer
from mediagoblin.tools import pluginapi

def assetlink_parser_setup(subparser):
    pass


def link_theme_assets(theme, link_dir, printer=simple_printer):
    """
    Returns a list of string of text telling the user what we did
    which should be printable.
    """
    link_dir = link_dir.rstrip(os.path.sep)
    link_parent_dir = os.path.dirname(link_dir)
    if theme is None:
        printer(_('Cannot link theme... no theme set\n'))
        return

    def _maybe_unlink_link_dir():
        """unlink link directory if it exists"""
        if os.path.lexists(link_dir) and os.path.islink(link_dir):
            os.unlink(link_dir)
            return True

    if theme.get('assets_dir') is None:
        printer(_('No asset directory for this theme\n'))
        if _maybe_unlink_link_dir():
            printer(_('However, old link directory symlink found; removed.\n'))
        return
    _maybe_unlink_link_dir()
    if not os.path.lexists(link_parent_dir):
        os.makedirs(link_parent_dir)
    os.symlink(theme['assets_dir'].rstrip(os.path.sep), link_dir)
    printer("Linked the theme's asset directory:\n  %s\nto:\n  %s\n" % (
     theme['assets_dir'], link_dir))


def link_plugin_assets(plugin_static, plugins_link_dir, printer=simple_printer):
    """
    Arguments:
     - plugin_static: a mediagoblin.tools.staticdirect.PluginStatic instance
       representing the static assets of this plugins' configuration
     - plugins_link_dir: Base directory plugins are linked from
    """
    link_dir = os.path.join(plugins_link_dir.rstrip(os.path.sep), plugin_static.name)
    if not os.path.lexists(plugins_link_dir):
        os.makedirs(plugins_link_dir)
    if os.path.lexists(link_dir):
        if not os.path.islink(link_dir):
            printer(_('Could not link "%s": %s exists and is not a symlink\n') % (
             plugin_static.name, link_dir))
            return
        if os.path.realpath(link_dir) == plugin_static.file_path:
            printer(_('Skipping "%s"; already set up.\n') % plugin_static.name)
            return
        printer(_('Old link found for "%s"; removing.\n') % plugin_static.name)
        os.unlink(link_dir)
    os.symlink(plugin_static.file_path.rstrip(os.path.sep), link_dir)
    printer('Linked asset directory for plugin "%s":\n  %s\nto:\n  %s\n' % (
     plugin_static.name,
     plugin_static.file_path.rstrip(os.path.sep),
     link_dir))


def assetlink(args):
    """
    Link the asset directory of the currently installed theme and plugins
    """
    mgoblin_app = commands_util.setup_app(args)
    app_config = mg_globals.app_config
    link_theme_assets(mgoblin_app.current_theme, app_config['theme_linked_assets_dir'])
    for plugin_static in pluginapi.hook_runall('static_setup'):
        link_plugin_assets(plugin_static, app_config['plugin_linked_assets_dir'])
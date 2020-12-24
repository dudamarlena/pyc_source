# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/plugins/base.py
# Compiled at: 2008-04-27 14:34:39
"""

Base plugin class
=================

All plugins should inherit doapfiend.plugins.Plugin

"""
import textwrap

class Plugin(object):
    """Base class for doapfiend plugins. It's not necessary to subclass this
    class to create a plugin; however, all plugins must implement
    `add_options(self, parser)` and `configure(self, options,
    conf)`, and must have the attributes `enabled` and `name`.

    Plugins should not be enabled by default.

    Subclassing Plugin will give your plugin some friendly default
    behavior:

      - A --with-$name option will be added to the command line
        interface to enable the plugin. The plugin class's docstring
        will be used as the help for this option.
      - The plugin will not be enabled unless this option is selected by
        the user.    
    """
    enabled = False
    enable_opt = None
    name = None

    def __init__(self):
        self.conf = None
        if self.name is None:
            self.name = self.__class__.__name__.lower()
        if self.enable_opt is None:
            self.enable_opt = 'enable_plugin_%s' % self.name
        return

    def add_options(self, parser):
        """Add command-line options for this plugin.

        The base plugin class adds --with-$name by default, used to enable the
        plugin. 
        """
        parser.add_option('--with-%s' % self.name, action='store_true', dest=self.enable_opt, help='Enable plugin %s: %s' % (
         self.__class__.__name__, self.help()))

    def configure(self, options, conf):
        """Configure the plugin and system, based on selected options.

        The base plugin class sets the plugin to enabled if the enable option
        for the plugin (self.enable_opt) is true.
        """
        self.conf = conf
        self.options = options
        if hasattr(options, self.enable_opt):
            self.enabled = getattr(options, self.enable_opt)

    def help(self):
        """Return help for this plugin. This will be output as the help
        section of the --with-$name option that enables the plugin.
        """
        if self.__class__.__doc__:
            return textwrap.dedent(self.__class__.__doc__)
        return '(no help available)'
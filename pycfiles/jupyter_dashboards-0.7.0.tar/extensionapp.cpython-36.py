# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/dashboards/jupyter_dashboards/extensionapp.py
# Compiled at: 2017-03-21 21:09:05
# Size of source mod 2**32: 6280 bytes
import os.path, sys
from ._version import __version__
from notebook.nbextensions import InstallNBExtensionApp, EnableNBExtensionApp, DisableNBExtensionApp, flags, aliases
try:
    from notebook.extensions import BaseExtensionApp
    _new_extensions = True
except ImportError:
    try:
        from notebook.nbextensions import BaseNBExtensionApp
        BaseExtensionApp = BaseNBExtensionApp
        _new_extensions = True
    except ImportError:
        BaseExtensionApp = object
        _new_extensions = False

from traitlets import Unicode
from traitlets.config.application import catch_config_error
from traitlets.config.application import Application
INSTALL_FLAGS = {}
INSTALL_FLAGS.update(flags)
INSTALL_ALIASES = {}
INSTALL_ALIASES.update(aliases)
del INSTALL_ALIASES['destination']

class ExtensionInstallApp(InstallNBExtensionApp):
    __doc__ = 'Subclass that installs this particular extension.'
    name = 'jupyter-dashboards-extension-install'
    description = 'Install the jupyter_dashboards extension'
    flags = INSTALL_FLAGS
    aliases = INSTALL_ALIASES
    examples = '\n        jupyter dashboards install\n        jupyter dashboards install --user\n        jupyter dashboards install --prefix=/path/to/prefix\n        jupyter dashboards install --nbextensions=/path/to/nbextensions\n    '
    destination = Unicode('')

    def _classes_default(self):
        return [
         ExtensionInstallApp, InstallNBExtensionApp]

    def start(self):
        here = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.log.info('Installing jupyter_dashboards JS notebook extensions')
        self.extra_args = [os.path.join(here, 'nbextension')]
        self.destination = 'jupyter_dashboards'
        self.install_extensions()
        self.log.info('Done.')


class ExtensionActivateApp(EnableNBExtensionApp):
    __doc__ = 'Subclass that activates this particular extension.'
    name = 'jupyter-dashboards-extension-activate'
    description = 'Activate the jupyter_dashboards extension'
    flags = {}
    aliases = {}
    examples = '\n        jupyter dashboards activate\n    '

    def _classes_default(self):
        return [
         ExtensionActivateApp, EnableNBExtensionApp]

    def start(self):
        self.log.info('Activating jupyter_dashboards JS notebook extensions')
        self.section = 'notebook'
        self.enable_nbextension('jupyter_dashboards/notebook/main')
        self.log.info('Done.')


class ExtensionDeactivateApp(DisableNBExtensionApp):
    __doc__ = 'Subclass that deactivates this particular extension.'
    name = 'jupyter-dashboards-extension-deactivate'
    description = 'Deactivate the jupyter_dashboards extension'
    flags = {}
    aliases = {}
    examples = '\n        jupyter dashboards deactivate\n    '

    def _classes_default(self):
        return [
         ExtensionDeactivateApp, DisableNBExtensionApp]

    def start(self):
        self.log.info('Deactivating jupyter_dashboards JS notebook extensions')
        self.section = 'notebook'
        self.disable_nbextension('jupyter_dashboards/notebook/main')
        self.log.info('Done.')


class ExtensionQuickSetupApp(BaseExtensionApp):
    __doc__ = 'Installs and enables all parts of this extension'
    name = 'jupyter dashboards quick-setup'
    version = __version__
    description = 'Installs and enables all features of the jupyter_dashboards extension'

    def start(self):
        self.argv.extend(['--py', 'jupyter_dashboards'])
        from notebook import nbextensions
        install = nbextensions.InstallNBExtensionApp()
        install.initialize(self.argv)
        install.start()
        enable = nbextensions.EnableNBExtensionApp()
        enable.initialize(self.argv)
        enable.start()


class ExtensionQuickRemovalApp(BaseExtensionApp):
    __doc__ = 'Disables and uninstalls all parts of this extension'
    name = 'jupyter dashboards quick-remove'
    version = __version__
    description = 'Disables and removes all features of the jupyter_dashboards extension'

    def start(self):
        self.argv.extend(['--py', 'jupyter_dashboards'])
        from notebook import nbextensions
        enable = nbextensions.DisableNBExtensionApp()
        enable.initialize(self.argv)
        enable.start()
        install = nbextensions.UninstallNBExtensionApp()
        install.initialize(self.argv)
        install.start()


class ExtensionApp(Application):
    __doc__ = 'CLI for extension management.'
    name = 'jupyter_dashboards extension'
    description = 'Utilities for managing the jupyter_dashboards extension'
    examples = ''
    subcommands = {}
    if _new_extensions:
        subcommands.update({'quick-setup':(
          ExtensionQuickSetupApp,
          'Install and enable everything in the package (notebook>=4.2)'), 
         'quick-remove':(
          ExtensionQuickRemovalApp,
          'Disable and uninstall everything in the package (notebook>=4.2)')})
    else:
        subcommands.update(dict(install=(
         ExtensionInstallApp,
         'Install the extension.'),
          activate=(
         ExtensionActivateApp,
         'Activate the extension.'),
          deactivate=(
         ExtensionDeactivateApp,
         'Deactivate the extension.')))

    def _classes_default(self):
        classes = super(ExtensionApp, self)._classes_default()
        for appname, (app, help) in self.subcommands.items():
            if len(app.class_traits(config=True)) > 0:
                classes.append(app)

    @catch_config_error
    def initialize(self, argv=None):
        super(ExtensionApp, self).initialize(argv)

    def start(self):
        if self.subapp is None:
            self.print_help()
            sys.exit(1)
        super(ExtensionApp, self).start()


def main():
    ExtensionApp.launch_instance()
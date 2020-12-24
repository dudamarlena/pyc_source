# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanager/commands/install/addon.py
# Compiled at: 2017-11-11 03:08:58
import os
from ..base import Base
from ...utils.addons import Addons
from ...utils.os_helpers import ask_for_input
from snipsmanagercore import pretty_printer as pp

class AddonInstallerException(Exception):
    pass


class AddonInstallerWarning(Exception):
    pass


class AddonInstaller(Base):
    SPOTIFY_LOGIN_URL = 'https://snips-spotify-login.herokuapp.com'

    def run(self):
        pp.silent = self.options['--silent']
        interactive = not self.options['--non-interactive']
        addon_id = self.options['<addon_id>']
        try:
            if addon_id == 'spotify':
                AddonInstaller.install_spotify_addon(params=self.options['PARAMS'], interactive=interactive)
            else:
                raise AddonInstallerException(('Error: Unknown add-on {}').format(addon_id))
        except AddonInstallerWarning as e:
            pp.pwarning(str(e))
        except Exception as e:
            pp.perror(str(e))

    @staticmethod
    def install_spotify_addon(params=None, interactive=True):
        pp.pcommand('Installing Spotify add-on')
        if params is None or len(params) == 0:
            if interactive:
                pp.psubmessage('You need to provide a Spotify token', indent=True)
                pp.psubmessage(('Please open \x1b[1m\x1b[4m{}\x1b[0m in a web browser and follow the instructions to obtain it').format(AddonInstaller.SPOTIFY_LOGIN_URL), indent=True)
                token = ask_for_input('Spotify token:')
            else:
                pp.pwarning('Spotify add-on not installed. Please provide the Spotify token as a parameter, or omit the `--non-interative` flag')
                return
        else:
            token = params[0]
        Addons.install('spotify', [token])
        pp.psuccess('Spotify add-on installed')
        return
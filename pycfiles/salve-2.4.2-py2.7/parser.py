# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/config/parser.py
# Compiled at: 2015-11-06 23:45:35
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from salve import paths

class SALVEConfigParser(configparser.ConfigParser):
    """
    The SALVE configuration parser.
    Loads default values, then attempts to look up
    the current user's rc file for overwrites to those
    values.
    """

    def __init__(self, userhome, filename):
        """
        SALVEConfigParser constructor.
        Creates a ConfigParser specialized for SALVE.

        Args:
            @userhome
            The home directory of the running user ($SUDO_USER if
            running under 'sudo').
            @filename
            The name of a specific config file to load.
        """
        configparser.ConfigParser.__init__(self)
        filenames = [
         paths.get_default_config(),
         paths.pjoin(userhome, '.salverc'),
         filename]
        self.read(f for f in filenames if f is not None)
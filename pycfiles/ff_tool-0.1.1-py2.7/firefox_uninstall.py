# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/fftool/firefox_uninstall.py
# Compiled at: 2016-05-05 18:57:04
import os, shutil, sys
from outlawg import Outlawg
from firefox_env_handler import IniHandler
from fftool import local, DIR_CONFIGS
Log = Outlawg()

def rimraf(path):
    """Recursively delete the specified path."""
    if os.path.isdir(path):
        print ('Deleting {0}').format(path)
        shutil.rmtree(path)
    else:
        print ('{0} is not a directory').format(path)


class FirefoxUninstall(object):

    def __init__(self, config, archive_dir='temp'):
        Log.header('UNINSTALL FIREFOX')
        self.CACHE_FILE = 'cache.ini'
        self.out_dir = archive_dir
        self.cache_path = os.path.join(self.out_dir, self.CACHE_FILE)
        self.cache = IniHandler(self.cache_path)
        if isinstance(config, IniHandler):
            self.config = config
        elif isinstance(config, str):
            self.config = IniHandler()
            self.config.load_os_config(config)
        else:
            sys.exit('FirefoxUninstall: Unexpected config data type')

    def uninstall_all(self, force=False):
        """Cleanup function:

        1. Delete all Firefox apps: nightly, aurora, beta, (general) release.
        2. delete the shared profiles directory.
        """
        IniHandler.banner('UNINSTALLING FIREFOXES')
        for channel in self.config.sections():
            self.uninstall_channel(channel, force)

    def uninstall_channel(self, channel, force=False):
        was_cached = self.cache.config.getboolean('cached', channel)
        if force or not was_cached:
            path_firefox_app = self.config.get(channel, 'PATH_FIREFOX_APP')
        if not os.path.isdir(path_firefox_app):
            print ('Firefox not found: {0}').format(path_firefox_app)
            return
            if self.config.is_windows():
                local(('"{0}/uninstall/helper.exe" -ms').format(path_firefox_app))
            else:
                rimraf(path_firefox_app, False)
        else:
            print '[%s] was cached, skipping uninstall.' % channel


def main():
    config_path = DIR_CONFIGS
    ff_uninstall = FirefoxUninstall(config_path)
    ff_uninstall.uninstall_all()


if __name__ == '__main__':
    main()
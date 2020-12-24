# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjama/core/facade.py
# Compiled at: 2012-01-13 10:39:27
"""
Created on Jan 6, 2012

@author: maemo
"""
import logging, pickle, os, os.path
from model import *
from ..common import version
version.getInstance().submitRevision('$Revision: 131 $')

def get_pyjama_storage_dir():
    """
    Compute the application storage dir.
    This is an utility function to retrieve the directory where pyjama can
    store any file like settings or cached data.
    """
    storage = os.path.expanduser('~')
    storage = os.path.join(storage, '.pyjama')
    return storage


class pyjama(object):
    """
    Main class of the Program. The GUI use this class like a Facade to any core functions.
    """

    def __init__(self):
        self.connected = False
        self._ensure_pyjama_conf_store()
        self.settings = None
        self.load_settings()
        self.apply_settings()
        return

    def get_pyjama_settings_file(self):
        storage = get_pyjama_storage_dir()
        storage = os.path.join(storage, 'settings.pickle')
        return storage

    def load_settings(self):
        """
        load the saved settings
        """
        self._ensure_pyjama_conf_store()
        storage = self.get_pyjama_settings_file()
        try:
            file = open(storage, 'rb')
            self.settings = pickle.load(file)
            file.close()
        except IOError, EOFError:
            logging.warning('failed to load the settings')
            self.settings = Settings()

    def save_settings(self):
        """
        save the current settings
        """
        self._ensure_pyjama_conf_store()
        storage = self.get_pyjama_settings_file()
        try:
            file = open(storage, 'wb')
            pickle.dump(self.settings, file)
            file.close()
        except IOError:
            logging.warning('failed to save the settings')

    def apply_settings(self):
        pass

    def _ensure_pyjama_conf_store(self):
        storage = get_pyjama_storage_dir()
        if os.path.exists(storage):
            pass
        else:
            os.makedirs(storage)

    def get_settings(self):
        return self.settings

    def get_pyjama_storage_dir(self):
        """
        Storage location of pyajama
        """
        return get_pyjama_storage_dir()

    def generate(self, output, *argv, **kwarg):
        Project(*argv, **kwarg).generate(output)
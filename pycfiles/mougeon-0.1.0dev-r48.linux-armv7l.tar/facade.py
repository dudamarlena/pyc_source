# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mougeon/core/facade.py
# Compiled at: 2012-03-13 12:39:51
"""
Created on 01 March 2012 04:19:29

@author: maemo
"""
import logging, pickle, os, os.path
from model import *
from persistence import dao
from ..common import version
version.getInstance().submitRevision('$Revision: 47 $')

def get_mougeon_storage_dir():
    """
    Compute the application storage dir.
    This is an utility function to retrieve the directory where mougeon can
    store any file like settings or cached data.
    """
    storage = os.path.expanduser('~')
    storage = os.path.join(storage, '.mougeon')
    return storage


class mougeon(object):
    """
    Main class of the Program. The GUI use this class like a Facade to any core functions.
    """

    def __init__(self):
        self._ensure_mougeon_conf_store()
        self._ensure_mougeon_data_store()
        self.settings = None
        self.load_settings()
        self.apply_settings()
        return

    def get_mougeon_settings_file(self):
        storage = get_mougeon_storage_dir()
        storage = os.path.join(storage, 'settings.pickle')
        return storage

    def load_settings(self):
        """
        load the saved settings
        """
        self._ensure_mougeon_conf_store()
        storage = self.get_mougeon_settings_file()
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
        self._ensure_mougeon_conf_store()
        storage = self.get_mougeon_settings_file()
        try:
            file = open(storage, 'wb')
            pickle.dump(self.settings, file)
            file.close()
        except IOError:
            logging.warning('failed to save the settings')

    def apply_settings(self):
        pass

    def _ensure_mougeon_conf_store(self):
        storage = get_mougeon_storage_dir()
        if os.path.exists(storage):
            pass
        else:
            os.makedirs(storage)

    def _ensure_mougeon_data_store(self):
        storage = get_mougeon_storage_dir()
        storage = os.path.join(storage, 'mougeon.db')
        dao.DATABASE_URL = storage
        dao.checkStorage()

    def get_settings(self):
        return self.settings

    def start_tracker_record(self):
        TRACKER_INSTANCE.record(True)

    def stop_tracker_record(self):
        TRACKER_INSTANCE.stop_record()

    def register_tracker_listener(self, aListener):
        TRACKER_INSTANCE.add_listener(aListener)

    def unregister_tracker_listener(self, aListener):
        TRACKER_INSTANCE.remove_listener(aListener)

    def reset_data(self):
        TRACKER_INSTANCE.reset_data()

    def get_mougeon_storage_dir(self):
        """
        Storage location of pyajama
        """
        return get_mougeon_storage_dir()

    def is_using_freemobile(self):
        return get_current_op() == FREE_OPERATOR

    def freemobile_percent(self):
        op = TRACKER_INSTANCE.free_mobile_record()
        tot = TRACKER_INSTANCE.number_of_record()
        if tot > 0:
            return 100.0 * op / tot
        else:
            return 0

    def orange_percent(self):
        op = TRACKER_INSTANCE.orange_record()
        tot = TRACKER_INSTANCE.number_of_record()
        if tot > 0:
            return 100.0 * op / tot
        else:
            return 0

    def get_mainly_used_operator(self):
        if self.freemobile_percent() >= 50:
            return FREE_OPERATOR
        else:
            return ORANGE_OPERATOR
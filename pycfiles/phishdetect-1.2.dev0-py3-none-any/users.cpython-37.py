# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-python/phishdetect/models/users.py
# Compiled at: 2019-12-26 17:59:17
# Size of source mod 2**32: 1005 bytes
from .model import Model
from ..endpoints import API_PATH

class Users(Model):

    def get_pending(self):
        """Get list of users pending activation.
        """
        return self._phishdetect.get(API_PATH['users_pending'])

    def get_active(self):
        """Get list of active users.
        """
        return self._phishdetect.get(API_PATH['users_active'])

    def activate(self, api_key):
        """Activate pending user.
        :param api_key: API key used to identify the user to activate.
        """
        return self._phishdetect.get(API_PATH['users_activate'].format(api_key=api_key))

    def deactivate(self, api_key):
        """Deactivate existing user.
        :param api_key: API key used to identify the user to deactivate.
        """
        return self._phishdetect.get(API_PATH['users_deactivate'].format(api_key=api_key))
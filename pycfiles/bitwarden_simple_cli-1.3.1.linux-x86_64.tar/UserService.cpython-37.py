# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/UserService.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 442 bytes
import bitwarden_simple_cli.services.StorageService as StorageService

class UserService:
    email = None
    stamp = None
    storageService = None
    userId = None

    def __init__(self, storage_service: StorageService):
        self.storageService = storage_service

    def get_user_id(self):
        if self.userId:
            return self.userId
        self.userId = self.storageService.get('userId')
        return self.userId
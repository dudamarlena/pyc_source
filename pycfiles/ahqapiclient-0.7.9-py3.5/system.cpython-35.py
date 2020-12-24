# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/system.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 297 bytes
from ahqapiclient.resources import Resource

class System(Resource):

    def __init__(self, http_client):
        super(System, self).__init__('/system', http_client)

    def expire_client_cooldown(self):
        return self.post(path=self.rurl('expire_client_cooldown'))
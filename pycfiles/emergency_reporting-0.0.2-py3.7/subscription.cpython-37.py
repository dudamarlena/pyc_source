# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/emergency_reporting/subscription.py
# Compiled at: 2020-04-28 09:06:02
# Size of source mod 2**32: 312 bytes
from .auth import Auth

class BaseSubscription:

    def __init__(self, client_id, client_secret, username, password, primary_key=None, secondary_key=None):
        self.Auth = Auth(client_id, client_secret, username, password)
        self.Auth.primary_key = primary_key
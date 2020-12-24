# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/emergency_reporting/client.py
# Compiled at: 2020-04-26 09:29:15
# Size of source mod 2**32: 1482 bytes
from .subscription import BaseSubscription
from .product import AgencyIncidentsProduct, AgencyAdministrationProduct, AgencyClassesProduct

class EmergencyReportingClient:

    def __init__(self, client_id=None, client_secret=None, username=None, password=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.AgencyIncidentsProduct = AgencyIncidentsProduct(BaseSubscription(client_id=client_id,
          client_secret=client_secret,
          username=username,
          password=password))
        self.AgencyAdministrationProduct = AgencyAdministrationProduct(BaseSubscription(client_id=client_id,
          client_secret=client_secret,
          username=username,
          password=password))
        self.AgencyClassesProduct = AgencyClassesProduct(BaseSubscription(client_id=client_id,
          client_secret=client_secret,
          username=username,
          password=password))

    def auth(self):
        self.AgencyIncidentsProduct.subscription.Auth.get_token()
        self.AgencyAdministrationProduct.subscription.Auth.get_token()
        self.AgencyClassesProduct.subscription.Auth.get_token()
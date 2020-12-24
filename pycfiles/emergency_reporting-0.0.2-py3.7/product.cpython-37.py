# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/emergency_reporting/product.py
# Compiled at: 2020-04-28 09:06:02
# Size of source mod 2**32: 999 bytes
from .api import AgenyIncidentsApi, AgencyUsersApi, AgencyStationsApi, AgencyClassesApi

class Product:

    def __init__(self, name, path, subscription):
        self.name = name
        self.path = path
        self.subscription = subscription
        self.apis = []


class AgencyIncidentsProduct(Product):

    def __init__(self, subscription):
        super().__init__('Agency Incidents', 'agencyincidents/', subscription)
        self.AgencyIncidentsApi = AgenyIncidentsApi(subscription)
        self.AgencyUsersApi = AgencyUsersApi(subscription)


class AgencyAdministrationProduct(Product):

    def __init__(self, subscription):
        super().__init__('Agency Administration', '', subscription)
        self.AgencyStationsApi = AgencyStationsApi(subscription)


class AgencyClassesProduct(Product):

    def __init__(self, subscription):
        super().__init__('Agency Classes', '', subscription)
        self.AgencyClassesApi = AgencyClassesApi(subscription)
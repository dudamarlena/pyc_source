# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python-fcc/license_view_api.py
# Compiled at: 2011-04-16 22:45:28
from generic_api import *
APIS = [
 ('get_licenses', 'http://data.fcc.gov/api/license-view/basicSearch/getLicenses'),
 ('get_common_names', 'http://data.fcc.gov/api/license-view/licenses/getCommonNames'),
 ('get_statuses', 'http://data.fcc.gov/api/license-view/licenses/getStatuses'),
 ('get_categories', 'http://data.fcc.gov/api/license-view/licenses/getCategories'),
 ('get_entities', 'http://data.fcc.gov/api/license-view/licenses/getEntities'),
 ('get_renewals', 'http://data.fcc.gov/api/license-view/licenses/getRenewals'),
 ('get_issued', 'http://data.fcc.gov/api/license-view/licenses/getIssued')]

class LicenseViewAPI(GenericAPI):

    def __init__(self):
        GenericAPI.__init__(self, APIS)


if __name__ == '__main__':
    bc = LicenseViewAPI()
    print bc.get_licenses(searchValue='Verizon Wireless')
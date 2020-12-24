# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python-fcc/sba_businesses_api.py
# Compiled at: 2011-04-17 00:23:55
from generic_api import *

def build_api_list(list, base):
    result = []
    for item in list:
        result.append((item, base + '/' + item + '/'))

    return result


list = [
 'by_category',
 'all_by_state',
 'by_business_type',
 'state_only',
 'state_and_county',
 'state_and_city',
 'by_zip']
APIS = build_api_list(list, 'http://api.sba.gov/license_permit')

class SBABusinessesAPI(GenericAPI):

    def __init__(self):
        GenericAPI.__init__(self, APIS)


if __name__ == '__main__':
    bb = SBABusinessesAPI()
    print bb.by_category('doing business as')
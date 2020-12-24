# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python-fcc/sba_loans_grants_api.py
# Compiled at: 2011-04-17 00:23:55
from generic_api import *

def build_api_list(list, base):
    result = []
    for item in list:
        result.append((item, base + '/' + item + '/'))

    return result


list = [
 'federal',
 'state_financing_for',
 'federal_and_state_financing_for']
APIS = build_api_list(list, 'http://api.sba.gov/loans_grants')

class SBALoansGrantsAPI(GenericAPI):

    def __init__(self):
        GenericAPI.__init__(self, APIS)


if __name__ == '__main__':
    bb = SBALoansGrantsAPI()
    print bb.by_category('doing business as')
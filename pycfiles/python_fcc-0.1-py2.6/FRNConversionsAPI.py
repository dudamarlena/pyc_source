# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python-fcc/FRNConversionsAPI.py
# Compiled at: 2011-04-16 22:23:31
from generic_api import *
import urllib, json

class FRNConversionsAPI(GenericAPI):
    """
  FRNConversionsAPI:
  - an API to access information about broadband provides.
  - original API: http://reboot.fcc.gov/developer/frn-conversions-api
  
  - methods:
    -- getList(stateCode, multi)
       takes stateCode=IL or stateCode=17 (FIPS code),
       (optional) multi=Yes or multi=No to signify whether to include FRNs also operating outside this state.
    
    -- getInfo(frn)
       takes frn='0017855545' (FRN id)
  """

    def __init__(self):
        apis = [
         ('getList', 'http://data.fcc.gov/api/frn/getList'),
         ('getInfo', 'http://data.fcc.gov/api/frn/getInfo')]
        GenericAPI.__init__(self, apis)


if __name__ == '__main__':
    bb = FRNConversionsAPI()
    x = bb.getList(stateCode='IL')
    print type(x)
    print len(x)
    print x.keys()
    print
    x = bb.getInfo(frn='0017855545')
    print type(x)
    print len(x)
    print x
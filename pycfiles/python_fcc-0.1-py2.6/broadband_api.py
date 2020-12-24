# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python-fcc/broadband_api.py
# Compiled at: 2011-04-17 00:23:55
from generic_api import *
APIS = [
 ('get_data', 'http://data.fcc.gov/api/speedtest/find')]

class BroadbandApi(GenericAPI):

    def __init__(self):
        GenericAPI.__init__(self, APIS)


if __name__ == '__main__':
    bb = BroadbandApi()
    print bb.get_data(latitude=37, longitude=-122)
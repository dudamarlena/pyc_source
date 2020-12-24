# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notework/youzan/dubbo.py
# Compiled at: 2019-10-23 04:29:51
# Size of source mod 2**32: 609 bytes
import demjson, requests

class dubbo:

    def __init__(self, tether_host=None, interface=None, method=None):
        self.tether_host = tether_host
        self.interface = interface
        self.method = method

    def get_dubbo_result(self, data):
        headers = {'Content-Type':'application/json', 
         'X-Request-Protocol':'dubbo'}
        data = demjson.encode(data)
        url = '{}/soa/{}/{}'.format(self.tether_host, self.interface, self.method)
        response = requests.post(url, headers=headers, data=data)
        return demjson.decode(response.text)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/HelloBikeLibrary2/request.py
# Compiled at: 2020-03-13 04:56:27
# Size of source mod 2**32: 4155 bytes
__version__ = '1.0'
from robot.api import logger
from requests import sessions
from HelloBikeLibrary2.data_conversion import soa_loads
import json

class Request(object):

    def request_client(self, url='https://fox-backend.hellobike.cn/gct/soarequest', method='post', **kwargs):
        """
                        支持rpc请求与soap请求
                        支持加密http请求,请传参数 encode=True
                        返回内容为:
                                状态码,请求返回内容

                        例:
                        |$(content) |request client | http://10.111.30.72:8099/api/accountbalance
                """
        logger.info(url)
        logger.info(kwargs['data'])
        with sessions.Session() as (session):
            if 'encode' in kwargs:
                if kwargs['encode']:
                    body = dict(header={}, body=(kwargs['data']))
                    rep = session.request(url='https://fox-backend.hellobike.cn/fox/encode', method='post', json=body)
                    header = rep.json()['data']['header']
                    body = rep.json()['data']['encode']
                    print(body)
                    rep = session.request(url=url, method=method, json=body, headers=header)
                    body = dict(header=dict(Chaos='true'), response=(rep.text))
                    rep = session.request(url='https://fox-backend.hellobike.cn/fox/decode', method='post', json=body)
                    return rep
            elif 'data' in kwargs:
                if 'iface' in kwargs['data']:
                    data_struct = kwargs.pop('data')
                    if 'request' in data_struct:
                        for key, values in data_struct['request'].items():
                            if isinstance(values, (list, dict)):
                                values = json.dumps(values)
                                data_struct['request'][key] = values

                        data_struct['request'] = json.dumps(data_struct['request'])
                    rep = session.request(url=url, method=method, json=data_struct)
                    return (rep.status_code, soa_loads(rep.text))
                if 'headers' in kwargs:
                    rep = session.request(url=url, method=method, json=(kwargs['data']), headers=headers)
            else:
                rep = session.request(url=url, method=method, json=(kwargs['data']))
            return (rep.status_code, soa_loads(rep.text))


if __name__ == '__main__':
    data = {'env':'fat', 
     'iface':'com.hellobike.ride.api.iface.RideIface', 
     'method':'startRide', 
     'addr':'10.111.14.20:50010', 
     'request':{'arg0': {'startLat':31.1249201, 
               'orderGuid':15838439485081200101051, 
               'bikeNo':'2500500899', 
               'startChannel':4, 
               'startTime':1583843948913, 
               'userGuid':'c8f71e7c8bc049a8988cec062408a570', 
               'posType':0, 
               'startLng':121.3602946}}}
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    request = Request()
    url = 'https://fat-bike.hellobike.com/api'
    print(request.request_client(data=data))
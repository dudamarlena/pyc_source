# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nanopayh5\links.py
# Compiled at: 2020-04-09 01:30:19
# Size of source mod 2**32: 1527 bytes
import requests as R, random, json

def rand_num(x, leading_zeroes=True):
    """Return an X digit number, leading_zeroes returns a string, otherwise int"""
    if not leading_zeroes:
        return random.randint(10 ** (x - 1), 10 ** x - 1)
    if x > 6000:
        return ''.join([str(random.randint(0, 9)) for i in xrange(x)])
    return '{0:0{x}d}'.format((random.randint(0, 10 ** x - 1)), x=x)


def create_sm_links():
    url = 'http://api-test.nanopay.in.fg-example.com/openApi/v1/ordercreate'
    header = {'Content-Type': 'application/json'}
    thirdOrderId = rand_num(12)
    merchantUserId = rand_num(18)
    data = {'merchantId':2020000802, 
     'thirdOrderId':str(thirdOrderId), 
     'orderAmount':'800', 
     'transType':6, 
     'expireTime':888888, 
     'merchantUserId':str(merchantUserId), 
     'installmentId':1, 
     'goodsName':[
      {'goodsName': 'banana'}], 
     'appId':2019010924, 
     'timestamp':1582547187122, 
     'version':'1.0', 
     'sign':'YS3zxZvSoG52%)($'}
    res = R.post(url=url, headers=header, data=(json.dumps(data))).json()
    ts = res['data']['transSerial']
    tc = res['data']['tmpCode']
    url1 = 'https://h5.nanopay.in.fg-example.com/h5sdk/home/index.html?tmpCode=%s&transSerial=%s' % (tc, ts)
    print(url1)
    return url1


if __name__ == '__main__':
    create_sm_links()
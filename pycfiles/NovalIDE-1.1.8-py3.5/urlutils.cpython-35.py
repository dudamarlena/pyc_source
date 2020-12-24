# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/urlutils.py
# Compiled at: 2019-10-17 01:45:10
# Size of source mod 2**32: 1028 bytes
import requests

def RequestData(addr, arg={}, method='get', timeout=None, to_json=True):
    """
    """
    params = {}
    try:
        if timeout is not None:
            params['timeout'] = timeout
        req = None
        if method == 'get':
            params['params'] = arg
            req = requests.get(addr, **params)
        elif method == 'post':
            req = requests.post(addr, data=arg, **params)
        if not to_json:
            return req.text
        else:
            return req.json()
    except Exception as e:
        print('open %s error:%s' % (addr, e))


def upload_file(addr, file, arg={}, timeout=None):
    """
        上传文件
        addr:上传url地址
        file:上传本地文件路径
        arg:url参数
    """
    params = {}
    files = {'file': open(file, 'rb')}
    try:
        req = requests.post(addr, data=arg, files=files, **params)
    except:
        print('upload file %s error' % file)
        return

    return req.json()
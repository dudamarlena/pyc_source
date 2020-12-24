# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ucloudclient/utils/api_utils.py
# Compiled at: 2015-11-11 06:54:58
import hashlib, time
region = 'cn-north-03'
region = 'cn-east-01'
region = 'hk-01'
region = 'us-west-01'

def get_token(private_key, params):
    items = params.items()
    items.sort()
    params_data = ''
    for key, value in items:
        params_data = params_data + str(key) + str(value)

    params_data = params_data + str(private_key)
    sign = hashlib.sha1()
    sign.update(params_data)
    signature = sign.hexdigest()
    return signature


def get_formate_time(now):
    if now:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
    return ''
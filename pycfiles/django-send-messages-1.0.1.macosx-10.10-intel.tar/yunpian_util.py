# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/esperyong/develop/pyprojects/hwbuluo_src/hwbuluo-site/venv/lib/python2.7/site-packages/sms/backends/yunpian_util.py
# Compiled at: 2015-05-02 22:25:49
import httplib, urllib
host = 'yunpian.com'
port = 80
version = 'v1'
user_get_uri = '/' + version + '/user/get.json'
sms_send_uri = '/' + version + '/sms/send.json'
sms_tpl_send_uri = '/' + version + '/sms/tpl_send.json'

def get_user_info(apikey):
    u"""
    取账户信息
    """
    conn = httplib.HTTPConnection(host, port=port)
    conn.request('GET', user_get_uri + '?apikey=' + apikey)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_sms(apikey, text, mobile):
    u"""
    能用接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request('POST', sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    u"""
    模板接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'tpl_id': tpl_id, 'tpl_value': tpl_value, 'mobile': mobile})
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request('POST', sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def test_tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    pass
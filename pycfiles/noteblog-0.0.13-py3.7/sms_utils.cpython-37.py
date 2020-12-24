# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/sms_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 2210 bytes
"""
@author = super_fazai
@File    : sms_utils.py
@connect : superonesfazai@gmail.com
"""
from requests import post
from .internet_utils import get_base_headers
from .common_utils import json_2_dict
__all__ = [
 'sms_2_somebody_by_twilio',
 'async_send_msg_2_wx']

def sms_2_somebody_by_twilio(account_sid, auth_token, to='8618698570079', _from='16083058199', body='Hello from Python!') -> bool:
    """
    通过twilio发送短信
        官网: https://www.twilio.com
        添加手机号: https://www.twilio.com/console/phone-numbers/verified
    :param account_sid: sid
    :param auth_token:
    :return:
    """
    TwilioClinet = None
    try:
        import twilio.rest as TwilioClinet
    except ImportError:
        print('ImportError: 不能导入twilio包, 可能未安装!!')

    res = False
    try:
        client = TwilioClinet(account_sid, auth_token)
        message = client.messages.create(to=('+{}'.format(to)),
          from_=('+{}'.format(_from)),
          body=body)
        if message.sid != '':
            res = True
    except Exception as e:
        try:
            print(e)
        finally:
            e = None
            del e

    return res


async def async_send_msg_2_wx(sc_key, title='新消息', msg='正文!') -> bool:
    """
    异步发送内容给微信
    :param sc_key: key
    :return:
    """
    headers = get_base_headers()
    headers.update({'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 
     'Referer':'http://sc.ftqq.com/?c=code', 
     'X-Requested-With':'XMLHttpRequest', 
     'Connection':'keep-alive'})
    data = {'text':title, 
     'desp':msg}
    url = 'http://sc.ftqq.com/{}.send'.format(sc_key)
    with post(url=url, headers=headers, data=data) as (resp):
        send_res = json_2_dict(resp.text).get('errmsg', 'success')
    if send_res == 'success':
        return True
    return False
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/register_utils.py
# Compiled at: 2019-05-05 05:47:25
# Size of source mod 2**32: 16915 bytes
"""
@author = super_fazai
@File    : register_utils.py
@connect : superonesfazai@gmail.com
"""
import re
from gc import collect
from time import sleep
from requests import session
from .common_utils import json_2_dict
from .internet_utils import get_random_phone_ua
from spider.fz_requests import Requests
__all__ = [
 'YiMaSmser',
 'TenMinuteEmail',
 'TwentyFourEmail']

class YiMaSmser(object):
    __doc__ = '\n    易码平台的短信验证码服务(http://www.51ym.me)(密码不修改token不变)\n    api doc: http://www.51ym.me/User/apidocs.html#login\n    '

    def __init__(self, username, pwd, use_proxy=False):
        self.username = username
        self.pwd = pwd
        self.token = ''
        self.base_url = 'http://api.fxhyd.cn/UserInterface.aspx'
        self.use_proxy = use_proxy

    def _login(self) -> bool:
        """
        登陆
        :return:
        """
        params = (
         ('action', 'login'),
         (
          'username', self.username),
         (
          'password', self.pwd))
        body = Requests.get_url_body(url=(self.base_url), params=params, use_proxy=(self.use_proxy))
        if body == '':
            print('获取到的body为空值!')
            return False
        _ = body.split('|')
        try:
            if _[0] == 'success':
                self.token = _[1]
                return True
            raise IndexError
        except IndexError:
            return False

    def _is_login(self) -> bool:
        """
        是否登陆，未登录则进行登陆
        :return:
        """
        login_res = True
        if self.token == '':
            login_res = self._login()
        if not login_res:
            print('account登陆失败!')
        return login_res

    def _get_account_info(self) -> dict:
        """
        获取当前账户信息
        :return:
        """
        if not self._is_login():
            return {}
        params = (('action', 'getaccountinfo'),
         (
          'token', self.token))
        body = Requests.get_url_body(url=(self.base_url), params=params, use_proxy=(self.use_proxy))
        _ = body.split('|')
        res = {}
        try:
            res = {'res':_[0],  'username':_[1], 
             'account_state':_[2], 
             'account_level':_[3], 
             'account_balance':_[4], 
             'freezing_amount':_[5], 
             'account_discounts':_[6], 
             'max_phone_num':_[7]}
        except IndexError as e:
            try:
                print(e)
            finally:
                e = None
                del e

        return res

    def _get_phone_num(self, project_id, exclude_no='', province='') -> str:
        """
        获取手机号码(获取是不收费的)
        :param project_id: 项目编号 http://www.51ym.me/User/MobileItemList.aspx中查找关键字
        :param exclude_no: 排除号段 不获取170、171和188号段的号码，则该参数为170.171.180，每个号段必须是前三位，用小数点分隔。
        :param province: 省代码 号码归属地的省份代码，省市代码表。
        :return: '' | 获取到的手机号
        """
        if not self._is_login():
            return ''
        params = (
         ('action', 'getmobile'),
         (
          'token', self.token),
         (
          'itemid', str(project_id)),
         (
          'excludeno', str(exclude_no)),
         (
          'province', str(province)))
        body = Requests.get_url_body(url=(self.base_url), params=params, use_proxy=(self.use_proxy))
        _ = body.split('|')
        if _[0] == 'success':
            return _[1]
        return ''

    def _get_sms(self, phone_num, project_id, release='1', timeout=66) -> str:
        """
        获取手机号对应的短信
        :param phone_num: 手机号码
        :param project_id: 项目编号
        :param release: 自动释放号码标识符 该参数值为1时，获取到短信的同时系统将自己释放该手机号码。若要继续使用该号码，请勿带入该参数。 设置为''
        :param timeout: 短信验证码内容超时等待时长
        :return:
        """
        if not self._is_login():
            return ''
        params = (
         ('action', 'getsms'),
         (
          'token', self.token),
         (
          'itemid', str(project_id)),
         (
          'mobile', str(phone_num)),
         (
          'release', release))
        _t = 0
        index = 1
        while _t >= timeout:
            print('超时退出!!')
            return ''
            body = Requests.get_url_body(url=(self.base_url), params=params, use_proxy=(self.use_proxy))
            _ = body.split('|')
            if _[0] == 'success':
                return _[1]
            print('{} try get sms content...sleeping 5s...'.format(index))
            print(body)
            sleep(5)
            _t += 5
            index += 1

    def _send_sms(self, phone_num, project_id, content: str, receive_phone_num='') -> bool:
        """
        发送短信
        :param phone_num: 手机号
        :param project_id: 项目id
        :param content: 短信内容
        :param receive_phone_num: 接收的短信的手机号，默认为空值
        :return: True 只代表成功提交发送任务，不代表短信已经成功发送，获取发送结果请调用“获取短信发送结果”接口。
        """
        if not self._is_login():
            return False
        params = (
         ('action', 'sendsms'),
         (
          'token', self.token),
         (
          'itemid', str(project_id)),
         (
          'mobile', str(phone_num)),
         (
          'sms', content),
         (
          'number', str(receive_phone_num)))
        body = Requests.get_url_body(url=(self.base_url), params=params, use_proxy=(self.use_proxy))
        _ = body.split('|')
        if _[0] == 'success':
            return True
        return False

    def _get_send_sms_res(self, phone_num, project_id) -> bool:
        """
        获取发短信结果
        :param phone_num: 发短信的手机号
        :param project_id: 项目编号
        :return:
        """
        if not self._is_login():
            return False
        params = (
         ('action', 'getsendsmsstate'),
         (
          'token', self.token),
         (
          'itemid', str(project_id)),
         (
          'mobile', str(phone_num)))
        body = Requests.get_url_body(url=(self.base_url), params=params, use_proxy=(self.use_proxy))
        _ = body.split('|')
        if _[0] == 'success':
            return True
        return False

    def _release_phone_num(self, phone_num, project_id) -> bool:
        """
        释放手机号码(注意: 如果号码不再使用请及时释放，否则你未释放的号码达到获取号码上限后将不能获取到新的号码。)
        :param phone_num: 被释放的手机号
        :param project_id: 项目编号
        :return:
        """
        if not self._is_login():
            return False
        params = (
         ('action', 'release'),
         (
          'token', self.token),
         (
          'itemid', str(project_id)),
         (
          'mobile', str(phone_num)))
        body = Requests.get_url_body(url=(self.base_url), params=params, use_proxy=(self.use_proxy))
        _ = body.split('|')
        if _[0] == 'success':
            return True
        return False

    def __del__(self):
        collect()


class TenMinuteEmail(object):
    __doc__ = "\n    10分钟邮箱(https://10minutemail.com/10MinuteMail/index.html)(缺点: 单机不能频繁获取email address, 会被封一个小时,  而且返回乱码)\n    TODO 收message 有问题\n        simple use:\n            _ = TenMinuteEmail()\n            email_address = _._get_email_address()\n            print('email_address: {}'.format(email_address))\n            print('time_left: {}s'.format(_._get_email_seconds_left()))\n            email_message_count = lambda : _._get_email_message_count()\n            index = 1\n            start_time = time()\n            while email_message_count() == 0 and time() - start_time < 60.:\n                sleep_time = 2\n                print('{}try...休眠{}s'.format(index, sleep_time))\n                index += 1\n\n            print('email_message_list: {}'.format(_._get_email_message_list()))\n    "

    def __init__(self):
        self._set_headers()
        self.session = session()
        self.email_address = ''

    def _set_headers(self):
        self.headers = {'accept-encoding':'gzip, deflate, br', 
         'accept-language':'zh-CN,zh;q=0.9', 
         'user-agent':get_random_phone_ua(), 
         'accept':'*/*', 
         'authority':'10minutemail.com', 
         'x-requested-with':'XMLHttpRequest'}

    def _get_url_body(self, url, params=None):
        try:
            with self.session.get(url=url, headers=(self.headers), params=params) as (response):
                body = response.text
        except Exception:
            body = ''

        return body

    def _get_email_address(self) -> str:
        """
        获取一个email address
        :return: 一个email address
        """
        url = 'https://10minutemail.com/10MinuteMail/resources/session/address'
        self.email_address = self._get_url_body(url=url)
        return self.email_address

    def _get_email_seconds_left(self) -> int:
        """
        获取email剩余秒数
        :return:
        """
        url = 'https://10minutemail.com/10MinuteMail/resources/session/secondsLeft'
        body = self._get_url_body(url=url)
        seconds_left = 0
        try:
            seconds_left = int(body)
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        return seconds_left

    def _get_email_message_count(self) -> int:
        """
        得到当前email中的message数
        :return:
        """
        url = 'https://10minutemail.com/10MinuteMail/resources/messages/messageCount'
        body = self._get_url_body(url=url)
        try:
            return int(body)
        except:
            return 0

    def _get_email_message_list(self) -> list:
        """
        获取该邮箱收到的所有邮件
        :return:
        """
        url = 'https://10minutemail.com/10MinuteMail/resources/messages/messagesAfter/0'
        body = self._get_url_body(url=url)
        data = json_2_dict(json_str=body, default_res=[])
        return data

    def __del__(self):
        collect()


class TwentyFourEmail(object):
    __doc__ = "\n    24小时邮箱(http://24mail.chacuo.net/)(可用)\n    simple use:\n        _ = TwentyFourEmail()\n        email_address = _._get_email_address()\n        print('获取到的email_address: {}'.format(email_address))\n        # # 换个邮箱\n        # email_address = _._get_new_email_address()\n        # print(email_address)\n        message_count = lambda : _._get_email_message_count()\n        start_time = time()\n        index = 1\n        while message_count() in (0, None) and time() - start_time < 100.:\n            sleep_time = 2\n            print('{} try, 休眠{}s...'.format(index, sleep_time))\n            sleep(sleep_time)\n            index += 1\n\n        message_list = _._get_email_message_list()\n        print(message_list)\n    "

    def __init__(self):
        self.cookies = None
        self.session = session()
        self.email_address = ''
        self._set_headers()
        self.base_url = 'http://24mail.chacuo.net/'
        self.MID = ''

    def _set_headers(self) -> None:
        self.headers = {'Origin':'http://24mail.chacuo.net', 
         'Accept-Encoding':'gzip, deflate', 
         'Accept-Language':'zh-CN,zh;q=0.9', 
         'User-Agent':get_random_phone_ua(), 
         'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 
         'Accept':'*/*', 
         'Referer':'http://24mail.chacuo.net/', 
         'X-Requested-With':'XMLHttpRequest', 
         'Connection':'keep-alive'}

    def get_email_address(self) -> str:
        """
        得到一个email address
        :return:
        """
        response = self.session.get(url=(self.base_url), headers=(self.headers))
        self.cookies = response.cookies.get_dict()
        if self.cookies.get('sid') is None:
            raise ValueError('获取邮箱失败!')
        body = response.text
        try:
            self.email_address = re.compile('value="(.*?)" valid=').findall(body)[0] + '@chacuo.net'
        except IndexError:
            print('获取email_address时索引异常!')

        return self.email_address

    def _get_new_email_address(self):
        """
        换个新email address
        :return:
        """
        data = {'data':self.email_address.split('@')[0], 
         'type':'renew', 
         'arg':'d=chacuo.net_f='}
        with self.session.post(url=(self.base_url), headers=(self.headers), cookies=(self.cookies), data=data) as (response):
            self.cookies = response.cookies.get_dict()
            print('获取到的新cookies: {}'.format(self.cookies))
            try:
                self.email_address = json_2_dict(response.text).get('data', [])[0] + '@chacuo.net'
            except IndexError:
                print('新获取邮箱时索引异常!')
                self.email_address = ''

        return self.email_address

    def get_email_message_count(self) -> int:
        """
        获取email message数
        :return:
        """
        data = {'data':self.email_address.split('@')[0], 
         'type':'refresh', 
         'arg':''}
        try:
            response = self.session.post(url=(self.base_url), headers=(self.headers), cookies=(self.cookies), data=data)
        except Exception as e:
            try:
                print(e)
                return 0
            finally:
                e = None
                del e

        res = []
        try:
            res = json_2_dict(response.text).get('data', {})[0].get('list', [])
            if res != []:
                try:
                    self.MID = res[0].get('MID', '')
                except IndexError:
                    print('获取MID失败!')

        except IndexError:
            print('获取list时索引异常!')

        return len(res)

    def get_email_message_list(self) -> list:
        """
        获取邮件内容
        :return:
        """
        data = {'data':self.email_address.split('@')[0], 
         'type':'mailinfo', 
         'arg':'f={}'.format(self.MID)}
        message_list = []
        with self.session.post(url=(self.base_url), headers=(self.headers), cookies=(self.cookies), data=data) as (response):
            try:
                message_list = json_2_dict(response.text).get('data', {})[0]
            except IndexError:
                print('获取message_list时索引异常!')

            return message_list
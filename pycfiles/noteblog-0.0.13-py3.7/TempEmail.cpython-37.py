# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/brush/TempEmail.py
# Compiled at: 2019-05-05 05:47:25
# Size of source mod 2**32: 2414 bytes
import json, time, requests
from lxml import etree

class TempEmail:
    __doc__ = '临时邮箱\n    使用http://24mail.chacuo.net/10分钟邮箱,\n    监听并返回收到的邮件内容,用以接受验证码\n    '

    def __init__(self):
        self.headers = {'Pragma':'no-cache', 
         'Origin':'http://24mail.chacuo.net', 
         'Accept-Encoding':'gzip, deflate', 
         'Accept-Language':'zh-CN,zh;q=0.9', 
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 
         'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 
         'Accept':'*/*', 
         'Cache-Control':'no-cache', 
         'X-Requested-With':'XMLHttpRequest', 
         'Connection':'keep-alive', 
         'Referer':'http://24mail.chacuo.net/'}
        self.session = requests.Session()
        r = self.session.get('http://24mail.chacuo.net/', headers=(self.headers))
        selector = etree.HTML(r.text)
        self.email_id = selector.xpath('//*[@id="converts"]/@value')
        self.mid = ''

    def get_email_address(self):
        return self.email_id[0] + '@chacuo.net'

    def check_received_email(self):
        data = {'data':self.email_id, 
         'type':'refresh', 
         'arg':''}
        time.sleep(3)
        r = self.session.post('http://24mail.chacuo.net/', data=data)
        r_json = json.loads(r.text)
        try:
            mid = r_json['data'][0]['list'][0]['MID']
            self.mid = mid
            return True
        except IndexError:
            return False

    def get_email_content(self):
        data2 = {'data':self.email_id, 
         'type':'mailinfo', 
         'arg':'f=' + str(self.mid)}
        r2 = self.session.post('http://24mail.chacuo.net/', data=data2)
        r2_json = json.loads(r2.text)
        return r2_json['data'][0][1][0]['DATA']


def test():
    temp_email = TempEmail()
    print(temp_email.get_email_address())
    while temp_email.check_received_email():
        content = temp_email.get_email_content()
        print(content)
        break


test()
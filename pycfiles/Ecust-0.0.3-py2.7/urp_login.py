# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/URP_login.py
# Compiled at: 2016-12-30 01:33:05
""" 信息门户登录 """
import requests

def Login(stuID, stuPW):
    url = 'http://urp.ecust.edu.cn/userPasswordValidate.portal'
    params = {'Login.Token1': stuID, 
       'Login.Token2': stuPW, 
       'goto': 'http://urp.ecust.edu.cn/loginSuccess.portal', 
       'gotoOnFail': 'http://urp.ecust.edu.cn/loginFailure.portal'}
    req = requests.Session()
    req.post(url, data=params)
    r = req.get('http://urp.ecust.edu.cn/index.portal')
    text = r.text.encode('utf8')
    if validateLogin(text):
        return r.cookies
    else:
        return False


def validateLogin(x):
    signal = '您好'
    if x.find(signal) > 0:
        return True
    else:
        return False
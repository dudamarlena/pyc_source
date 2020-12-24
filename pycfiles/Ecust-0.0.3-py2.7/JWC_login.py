# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwc_login.py
# Compiled at: 2016-12-30 00:47:48
"""
教务处登录
http://jwc.Ecust.edu.cn
"""
import requests
from lxml import etree
import cookielib

def jwc_login(stuID, stuPW):
    x = primary_method(stuID, stuPW)
    if x:
        return x


def primary_method(stuID, stuPW):
    get_url = 'http://202.120.108.14/ecustedu/K_StudentQuery/K_StudentQueryLogin.aspx'
    get = requests.get(get_url)
    root = etree.HTML(get.text)
    viewstate_tag = root.xpath("//*[@id='__VIEWSTATE']")
    viewstate = viewstate_tag[0].attrib['value']
    eventvalidation_tag = root.xpath("//*[@id='__EVENTVALIDATION']")
    eventvalidation = eventvalidation_tag[0].attrib['value']
    url_ggcx_login = 'http://202.120.108.14/ecustedu/K_StudentQuery/K_StudentQueryLogin.aspx'
    payload = {'TxtStudentId': stuID, 
       'TxtPassword': stuPW, 
       '__EVENTVALIDATION': eventvalidation, 
       '__VIEWSTATE': viewstate, 
       'BtnLogin': '登录'}
    r = requests.post(url_ggcx_login, data=payload)
    text = r.text.encode('utf8')
    if validate_login(text):
        return r.cookies
    else:
        return False


def validate_login(x):
    signal = '您好'
    if x.find(signal) > 0:
        return True
    else:
        return False
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/send_wechat.py
# Compiled at: 2018-08-01 08:00:01
import os, sys, urllib2, urllib, urllib2

def log2(message):
    print message


def wechat_send(pre_log_str, title, message, channel=0):
    pre_log_str += sys._getframe().f_code.co_name + ':'
    log2(pre_log_str + '[start]')
    url = 'http://192.168.199.1:8000/mainsugar/loginGET/'
    url = 'https://pushbear.ftqq.com/sub'
    textmod = {'user': 'admin', 'password': 'admin'}
    channel_list[('1945-9555a8df744033c5baeeeba062fc1791', '4963-3f3d688a3a5a1d077da853d6e0dc5c1d',
                  '4964-b7f9b8b0bcd8cc6d492ba97f8eb4cfd6', '4987-5ff8c157bb736d6a33635a61cf167be7')]
    textmod = {'sendkey': channel_list[channel], 
       'text': '%s' % title, 
       'desp': '%s' % message}
    textmod = urllib.urlencode(textmod)
    log2(pre_log_str + ' ' + textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    res = res.read()
    log2(pre_log_str + ' ' + res)
    log2(pre_log_str + '[  end]')


if __name__ == '__main__':
    sys.argv[1]
    sys.argv[2]
    wechat_send('main', sys.argv[1], sys.argv[2], sys.argv[3])
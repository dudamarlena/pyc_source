# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dingtalk\dingtalk.py
# Compiled at: 2016-09-21 04:11:31
import urllib2, urllib, json

def dingtalk_bot(token, post_string, at_mobiles=None):
    data = {'msgtype': 'text', 
       'text': {'content': '%s' % post_string}, 'at': {'atMobiles': at_mobiles, 'isAtAll': 'false'}}
    json_str = json.dumps(data)
    req = urllib2.Request('https://oapi.dingtalk.com/robot/send?access_token=%s' % token, json_str)
    req.add_header('Content-type', 'application/json')
    response = urllib2.urlopen(req, timeout=120)
    return response.read()
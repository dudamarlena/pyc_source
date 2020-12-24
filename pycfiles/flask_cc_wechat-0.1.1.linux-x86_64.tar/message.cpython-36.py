# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wen/.pyenv/versions/wechatpy/lib/python3.6/site-packages/flask_cc_wechat/message.py
# Compiled at: 2019-06-24 05:03:39
# Size of source mod 2**32: 1402 bytes
import json, time, requests
from . import WECHAT_API_URL
from .token import TokenUtil

class SendMessage(object):
    __doc__ = '\n    给用户发送信息\n    '

    def __init__(self):
        self.ToUserName = ''
        self.FromUserName = ''
        self.CreateTime = str(int(time.time()))
        self.MsgType = ''
        self.Content = ''

    def send_text(self):
        """
        发送文本消息
        :param toUserName:
        :param content:
        :param msgType:
        :return:
        """
        sendXml = '<xml>\n         <ToUserName><![CDATA[%s]]></ToUserName>\n         <FromUserName><![CDATA[%s]]></FromUserName>\n         <CreateTime>%s</CreateTime>\n         <MsgType><![CDATA[text]]></MsgType>\n         <Content><![CDATA[%s]]></Content>\n         </xml>\n        '
        return sendXml % (
         self.ToUserName,
         self.FromUserName,
         self.CreateTime,
         self.Content)

    def send_tm_message(self, postdata):
        access_token = TokenUtil.access_token()
        post_url = WECHAT_API_URL + 'cgi-bin/message/template/send?access_token=%s' % access_token
        response = requests.post(post_url, data=(postdata.encode('utf-8')))
        jsonreturn = json.loads(response.text)
        print(jsonreturn)
        if jsonreturn['errcode'] == 0:
            return True
        else:
            return False
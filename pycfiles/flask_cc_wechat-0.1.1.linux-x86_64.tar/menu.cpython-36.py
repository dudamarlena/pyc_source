# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wen/.pyenv/versions/wechatpy/lib/python3.6/site-packages/flask_cc_wechat/menu.py
# Compiled at: 2019-06-24 05:01:01
# Size of source mod 2**32: 1085 bytes
import requests
from . import WECHAT_API_URL

class Menu(object):
    __doc__ = '\n    自定义菜单栏\n    '

    def __init__(self):
        pass

    def create(self, postData, accessToken):
        postUrl = WECHAT_API_URL + 'cgi-bin/menu/create?access_token=%s' % accessToken
        request = requests.post(postUrl, data=(postData.encode('utf-8')))
        self.get_current_selfmenu_info(accessToken)
        if request.status_code == 200:
            return True
        else:
            return False

    def query(self, accessToken):
        postUrl = WECHAT_API_URL + 'cgi-bin/menu/get?access_token=%s' % accessToken
        requests.get(postUrl)

    def delete(self, accessToken):
        postUrl = WECHAT_API_URL + 'cgi-bin/menu/delete?access_token=%s' % accessToken
        requests.get(postUrl)

    def get_current_selfmenu_info(self, accessToken):
        postUrl = WECHAT_API_URL + 'cgi-bin/get_current_selfmenu_info?access_token=%s' % accessToken
        request = requests.get(postUrl)
        return request.text
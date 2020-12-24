# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wen/.pyenv/versions/wechatpy/lib/python3.6/site-packages/flask_cc_wechat/__init__.py
# Compiled at: 2019-06-24 08:39:30
# Size of source mod 2**32: 389 bytes
WECHAT_API_URL = 'https://api.weixin.qq.com/'

class Wechat(object):

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(self.app)

    def init_app(self, app):
        self.config = app.config
        if not self.config.get('WXAPPID'):
            raise AssertionError('WXAPPID must in config')
        elif not self.config.get('WXAPPSECRET'):
            raise AssertionError('WXAPPSECRET must in config')
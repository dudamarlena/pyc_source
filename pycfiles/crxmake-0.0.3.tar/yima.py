# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/extend/yima.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = b'\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: PyCharm\n@file: yima.py\n@create at: 2017-10-27 09:57\n\n这一行开始写关于本文件的说明与解释\n'
from __future__ import print_function, unicode_literals
from crwy.spider import Spider
from crwy.exceptions import CrwyException

class YiMa(Spider):

    def __init__(self, username, password, item_id):
        super(YiMa, self).__init__()
        if username and password and item_id:
            self.username = username
            self.password = password
            self.item_id = item_id
        else:
            raise CrwyException(b'[YiMa] params not valid.')

    def login(self):
        u"""
        YiMa 登录
        :return: 登录token
        """
        try:
            url = (b'http://api.fxhyd.cn/UserInterface.aspx?action=login&username={username}&password={password}').format(username=self.username, password=self.password)
            res = self.html_downloader.download(url)
            if b'success' not in res.text:
                raise CrwyException(b'[YiMa] Login failed.')
            return res.text.strip().split(b'|')[(-1)]
        except Exception as e:
            raise CrwyException(e)

    def get_phone(self, token, phone_type=b'', phone=b'', not_prefix=b''):
        u"""
        获取手机号
        :param token:   登录token
        :param phone_type:  运营商 1 [移动] 2 [联通] 3 [电信]
        :param phone:   指定号码
        :param not_prefix:  不要号段 (例子:notPrefix=170.177 ,代表不获取170和177的号段)
        :return: 手机号码
        """
        try:
            url = (b'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token={token}&itemid={item_id}&excludeno={not_prefix}&isp={phone_type}&mobile={phone}').format(token=token, item_id=self.item_id, not_prefix=not_prefix, phone_type=phone_type, phone=phone)
            res = self.html_downloader.download(url)
            if b'success' not in res.text:
                raise CrwyException(b'[YiMa] get phone failed.')
            return res.text.strip().split(b'|')[(-1)]
        except Exception as e:
            raise CrwyException(e)

    def get_message(self, token, phone):
        u"""
        获取短信消息
        :param token:   登录token
        :param phone:   手机号
        :return:
        """
        try:
            url = (b'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token={token}&itemid={item_id}&mobile={phone}&release=0').format(token=token, item_id=self.item_id, phone=phone)
            res = self.html_downloader.download(url)
            if b'success' not in res.text:
                raise CrwyException(b'[YiMa] get message failed.')
            else:
                return res.text.strip().split(b'|')[(-1)]
        except Exception as e:
            raise CrwyException(e)

    def release_phone(self, token, phone):
        try:
            url = (b'http://api.fxhyd.cn/UserInterface.aspx?action=release&token={token}&itemid={item_id}&mobile={phone}&release=0').format(token=token, item_id=self.item_id, phone=phone)
            res = self.html_downloader.download(url)
            if b'success' not in res.text:
                raise CrwyException(b'[YiMa] release phone failed.')
        except Exception as e:
            raise CrwyException(e)

    def add_black(self, token, phone):
        try:
            url = (b'http://api.fxhyd.cn/UserInterface.aspx?action=addignore&token={token}&itemid={item_id}&mobile={phone}&release=0').format(token=token, item_id=self.item_id, phone=phone)
            res = self.html_downloader.download(url)
            if b'success' not in res.text:
                raise CrwyException(b'[YiMa] black phone failed.')
        except Exception as e:
            raise CrwyException(e)
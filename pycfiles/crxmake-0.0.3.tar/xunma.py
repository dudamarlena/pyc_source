# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/extend/xunma.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = b'\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: IntelliJ IDEA\n@file: xunma.py\n@create at: 2018-09-14 11:41\n\n这一行开始写关于本文件的说明与解释\n'
from __future__ import print_function, unicode_literals
from crwy.spider import Spider
from crwy.exceptions import CrwyExtendException

class XunMa(Spider):

    def __init__(self, username, password, item_id):
        super(XunMa, self).__init__()
        if username and password and item_id:
            self.username = username
            self.password = password
            self.item_id = item_id
        else:
            raise CrwyExtendException(b'[XunMa] params not valid.')

    def login(self):
        u"""
        XunMa 登录
        :return: 登录token
        """
        try:
            url = (b'http://xapi.xunma.net/Login?uName={username}&pWord={password}&Code=UTF8').format(username=self.username, password=self.password)
            res = self.html_downloader.download(url)
            return res.text.strip().split(b'&')[0]
        except Exception as e:
            raise CrwyExtendException(e)

    def get_phone(self, token, phone_type=b'', phone=b''):
        u"""
        获取手机号
        :param token:   登录token
        :param phone_type:  运营商 1 [移动] 2 [联通] 3 [电信]
        :param phone:   指定号码
        :return: 手机号码
        """
        try:
            url = (b'http://xapi.xunma.net/getPhone?ItemId={item_id}&token={token}&PhoneType={phone_type}&Code=UTF8&Phone={phone}').format(token=token, item_id=self.item_id, phone_type=phone_type, phone=phone)
            res = self.html_downloader.download(url)
            return res.text.strip().split(b';')[0]
        except Exception as e:
            raise CrwyExtendException(e)

    def get_message(self, token, phone):
        u"""
        获取短信消息
        :param token:   登录token
        :param phone:   手机号
        :return:
        """
        try:
            url = (b'http://xapi.xunma.net/getMessage?token={token}&itemId={item_id}&phone={phone}&Code=UTF8').format(token=token, item_id=self.item_id, phone=phone)
            res = self.html_downloader.download(url)
            return res.text.strip().split(b'&')[(-1)]
        except Exception as e:
            raise CrwyExtendException(e)

    def release_phone(self, token, phone):
        try:
            url = (b'http://xapi.xunma.net/releasePhone?token={token}&phoneList={phone};&Code=UTF8').format(token=token, phone=phone)
            self.html_downloader.download(url)
        except Exception as e:
            raise CrwyExtendException(e)

    def add_black(self, token, phone):
        try:
            url = (b'http://xapi.xunma.net/addBlack?token={token}&phoneList={phone};&Code=UTF8').format(token=token, phone=phone)
            self.html_downloader.download(url)
        except Exception as e:
            raise CrwyExtendException(e)
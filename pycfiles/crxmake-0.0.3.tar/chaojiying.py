# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/extend/chaojiying.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = '\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: PyCharm\n@file: chaojiying.py\n@create at: 2018-05-11 16:33\n\n这一行开始写关于本文件的说明与解释\n'
import requests
from hashlib import md5

class ChaoJiYingApi(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {'user': self.username, 
           'pass2': self.password, 
           'softid': self.soft_id}
        self.headers = {'Connection': 'Keep-Alive', 
           'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'}

    def post_pic(self, im, code_type):
        u"""
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {'codetype': code_type}
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def report_error(self, im_id):
        u"""
        im_id:报错题目的图片ID
        """
        params = {'id': im_id}
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

    def decode(self, img_path, code_type):
        im = open(img_path, 'rb').read()
        res = self.post_pic(im, code_type)
        if res.get('err_no') == 0 and res.get('err_str') == 'OK':
            return res.get('pic_str')
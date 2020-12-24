# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/load_settings.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = '\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: PyCharm\n@file: load_settings.py\n@create at: 2018-06-20 19:32\n\n这一行开始写关于本文件的说明与解释\n'
import consul
from crwy.exceptions import CrwyException

class LoadSettingsFromConsul(object):

    def __init__(self, **kwargs):
        self.c = consul.Consul(**kwargs)
        self.main_key = None
        return

    def init_main_key(self, key=None):
        if not key:
            raise CrwyException('Please set key first.')
        self.main_key = key

    def _get_settings(self, key=None):
        self.init_main_key(key=key)
        index, data = self.c.kv.get(self.main_key, recurse=True)
        if not data:
            raise CrwyException('Please make sure the key: <%s> is exist.' % self.main_key)
        new_data = {item.get('Key').split('/')[(-1)]:eval(item.get('Value')) for item in data}
        return new_data

    @classmethod
    def get_settings(cls, key=None, **kwargs):
        load_settings = cls(**kwargs)
        return load_settings._get_settings(key=key)
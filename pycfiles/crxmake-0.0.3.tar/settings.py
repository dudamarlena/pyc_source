# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/scrapy_plugs/settings.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = '\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: PyCharm\n@file: settings.py\n@create at: 2018-06-20 19:33\n\n这一行开始写关于本文件的说明与解释\n'
from crwy.utils.load_settings import LoadSettingsFromConsul
from crwy.exceptions import CrwyException

class ScrapySettingsFromConsul(LoadSettingsFromConsul):

    def __init__(self, spider_name, bot_name, prefix='scrapy', **kwargs):
        super(ScrapySettingsFromConsul, self).__init__(**kwargs)
        self.spider_name = spider_name
        self.bot_name = bot_name
        self.prefix = prefix

    def init_main_key(self, key=None):
        if not key:
            self.main_key = ('{prefix}/{bot_name}/{spider_name}').format(prefix=self.prefix, bot_name=self.bot_name, spider_name=self.spider_name)
        else:
            self.main_key = key

    def _get_settings(self, key=None):
        self.init_main_key(key=key)
        index, data = self.c.kv.get(self.main_key, recurse=True)
        if not data:
            raise CrwyException('Please make sure the key: <%s> is exist.' % self.main_key)
        new_data = {item.get('Key').split('/')[(-1)]:eval(item.get('Value')) for item in data}
        new_data['SPIDER_NAME'] = self.spider_name
        return new_data

    @classmethod
    def get_settings(cls, spider_name, bot_name, key=None, prefix='scrapy', **kwargs):
        load_settings = cls(spider_name, bot_name, prefix=prefix, **kwargs)
        return load_settings._get_settings(key=key)
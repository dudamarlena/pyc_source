# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/spider.py
# Compiled at: 2020-02-03 23:11:43
import inspect
from crwy.utils.html.html_downloader import HtmlDownloader
from crwy.utils.html.html_parser import HtmlParser

class BaseSpider(object):
    u""" Spider基础类 """

    def __init__(self):
        u"""
        初始化下载器/解析器及日志接口
        """
        self.html_downloader = HtmlDownloader()
        self.html_parser = HtmlParser()


class Spider(BaseSpider):
    u""" Spider类 提供基本方法 """

    def __init__(self, logger=None):
        super(Spider, self).__init__()
        self.login_kwargs = None
        self.proxies = None
        if logger:
            self.logger = logger
        else:
            from crwy.utils.logger import Logger
            self.logger = Logger.timed_rt_logger()
        return

    def login(self, *args, **kwargs):
        pass

    def clean(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        pass

    def get_cookie(self):
        pass

    @staticmethod
    def func_name():
        u""" 返回函数名称 """
        return inspect.stack()[1][3]
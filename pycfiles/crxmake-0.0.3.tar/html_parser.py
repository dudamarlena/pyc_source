# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/html/html_parser.py
# Compiled at: 2020-02-03 23:11:43
import sys
from bs4 import BeautifulSoup
try:
    import PyV8
except ImportError:
    pass

class HtmlParser(object):
    u""" 解析器 """

    @staticmethod
    def parser(response):
        u"""
        utf-8字符处理
        :param response: 待处理字符串
        :return: 返回bs对象
        """
        if response is None:
            return
        else:
            if sys.version_info < (3, ):
                soup = BeautifulSoup(str(response), 'html.parser', from_encoding='utf-8')
            else:
                soup = BeautifulSoup(str(response), 'html.parser')
            return soup

    @staticmethod
    def gbk_parser(response):
        u"""
        gbk字符处理
        :param response: 待处理字符串
        :return: 返回bs对象
        """
        if response is None:
            return
        else:
            if sys.version_info < (3, ):
                soup = BeautifulSoup(str(response), 'html.parser', from_encoding='gb18030')
            else:
                soup = BeautifulSoup(str(response), 'html.parser')
            return soup

    @staticmethod
    def jsonp_parser(data):
        u"""
        非规范json数据处理 {a:1, b:1}
        key非字符串
        :param data: 待处理字符串
        :return: 返回标准json数据
        """
        ctx = PyV8.JSContext()
        ctx.enter()
        ctx.eval('\n            function func() {\n              var data = ' + data + ';\n              var json_data = JSON.stringify(data);\n              return json_data;\n            }\n        ')
        return ctx.locals.func()
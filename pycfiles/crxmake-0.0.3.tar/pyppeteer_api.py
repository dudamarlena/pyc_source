# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/pyppeteer_api.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = '\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: IntelliJ IDEA\n@file: pyppeteer_api.py\n@create at: 2019-03-24 17:04\n\n这一行开始写关于本文件的说明与解释\n'
import asyncio
from crwy.spider import Spider
try:
    from pyppeteer import launch
except ImportError:
    pass

class PyppeteerApi(Spider):

    def __init__(self, logger=None, proxy=None, **kwargs):
        super(PyppeteerApi, self).__init__(logger=logger)


def main():
    executor = PyppeteerApi()


if __name__ == '__main__':
    main()
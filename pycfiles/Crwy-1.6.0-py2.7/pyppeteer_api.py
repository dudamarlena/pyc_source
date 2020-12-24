# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/pyppeteer_api.py
# Compiled at: 2020-02-03 23:11:43
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: IntelliJ IDEA
@file: pyppeteer_api.py
@create at: 2019-03-24 17:04

这一行开始写关于本文件的说明与解释
"""
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
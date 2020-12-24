#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lijim,rocky
# 
# @Date:   2015-05-26 16:04:57
# @Last Modified time: 2015-05-26 16:38:07
from setuptools import setup, find_packages

setup(
        name = 'chinabankpay',
        version = '0.0.1',
         keywords = ('chinabankpay', 'thirdpartypayment'),
      #  py_modules = ['chinabankpay/pay.py','chinabankpay/__init__.py'],        #将模块的元数据与setup函数的参数关联
        packages=find_packages(),
        author = 'lijim',                        #这些只是Head First Labs对其模块使用的值，你的元数据可以与这里不同
        author_email = '935685518@qq.com',
        url = 'http://www.xxx.com',
        description = 'chinabank Third party payment 网银在线非官方接口 ',
)
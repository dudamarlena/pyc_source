#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: MeiBao
# Mail: ityun@vip.qq.com
# Created Time:  2019-11-10 18:14:52 PM
#############################################

from setuptools import setup

setup(
    name = "maoerpay",
    version = "1.0.1",
    keywords = ("maoerpay","pay","wechatpay","xiaowei"),
    description = "MaoerPay SDK",
    license = "MIT Licence",
    url = "https://github.com/amibk/maoerpay_sdk_python",

    author = "Bao Mei",
    author_email = "ityun@vip.qq.com",

    packages = ['maoerpay'],
    install_requires=["pycryptodomex==3.7.2",'requests']
)
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/28 7:37 下午
# @Author  : jack.du
# @Email   : xianghua.du@start.com.cn
# @File    : setup.py.py
# @Software: PyCharm
from setuptools import setup

setup(
    name = "wechatwork_notify",
    version = "0.1.0",
    description = "使用微信企业号发送应用消息",
    long_description = "使用微信企业号发送应用消息",
    license = "MIT Licence",
    scripts = ['wechatwork_send'],

    #url = "https://github.com/duxianghua/wechatwork_notify",
    author = "jack.du",

    packages = ['wechat', 'wechat.modules', 'wechat.utils'],
    include_package_data = True,
    platforms = "any",
    install_requires = ["urllib3", "six"],
    python_requires = '>=2.7'
)
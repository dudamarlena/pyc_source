# !/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="ouc_api",
    version="2.1.1",
    keywords=("ouc", "api", "中国海大", "中国海大教务处"),
    description="中国海洋大学非官方API",
    long_description="OUC-API 的初衷是希望为OUC的各个系统提供一套跨系统的简洁、优雅的、Pythonic的API接口，以便用户能够在此基础上进行扩展开发。",
    license="MIT Licence",

    url="https://github.com/LDouble/OUC-API",
    author="DoubleL",
    author_email="2943200389@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["chardet", "curl-http", "lxml", "pycurl", "xmltodict", "bs4"]
)

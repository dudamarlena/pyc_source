#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="bi-get",
    version="0.1.1",
    keywords=("pip", "bilibili", 'video download', 'spider'),
    description="关于B站的一个爬虫，可以获取视频的信息，下载视频等",
    long_description="具体见https://github.com/ujay-zheng/bi-get",
    url="https://github.com/ujay-zheng/bi-get",
    author="ujay",
    author_email="897013045@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['requests', 'beautifulsoup4', 'lxml']
)

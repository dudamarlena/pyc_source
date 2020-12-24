# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("./README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

#python3.6 setup.py sdist upload

setup(
    name = 'hehey-hcache',
    version = '1.0.2',
    author = '13564768842',
    packages=find_packages(),
    author_email = 'chinabluexfw@163.com',
    url = 'https://gitee.com/chinahehe/hehey-hcache',
    description = 'hehey-hcache 是一个python 数据缓存工具组件',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
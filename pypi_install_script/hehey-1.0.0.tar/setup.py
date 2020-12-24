# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("./README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

#python3.6 setup.py sdist upload

setup(
    name = 'hehey',
    version = '1.0.0',
    author = '13564768842',
    packages=find_packages(),
    author_email = 'chinabluexfw@163.com',
    url = 'https://gitee.com/chinahehe/hehey',
    description = 'hehey是一个python web 站点工具框架',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
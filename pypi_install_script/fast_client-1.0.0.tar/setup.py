#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: wanghaun
# Mail: wanghaun0718@outlook.com
# Created Time:  2020-4-02 10:29:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "fast_client",
    version = "1.0.0",
    keywords = ["pip", "fdfs","uploadtool", "wanghuan"],
    description = "FastDFS Server uploadtool",
    long_description = "",
    license = "MIT Licence",

    author = "wanghuan",
    author_email = "wanghuan0718@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
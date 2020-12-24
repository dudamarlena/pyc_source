#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: kebufu
# Mail: mcku_hei@qq.com
# Created Time:  2019-11-3-16:45
#############################################


from setuptools import setup, find_packages

setup(
    name = "cmdscreen",
    version = "1.0",
    keywords = ("pip", "cmdtool"),
    description = "Allow you change cmd screen color",
    long_description = "Allow you change cmd screen color",
    license = "MIT Licence",

    url = "https://github.com/kebufu/cmdscreen/blob/master/cmdscreen.py",
    author = "kebufu",
    author_email = "mcku_hei@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['ctypes']
)

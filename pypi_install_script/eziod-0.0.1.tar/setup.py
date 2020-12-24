#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "eziod",
    version = "0.0.1",
    keywords = ("pip", "eziod"),
    description = "a easy image object dataset",
    long_description = "a easy image object dataset parent class",
    license = "MIT Licence",

    url = "https://github.com/alexw994/eziod",
    author = "alexwww94",
    author_email = "243114328@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['request']
)

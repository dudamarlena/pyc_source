#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "hhrtest",
    version = "0.0.4",
    keywords = ["pip", "hhrtest", "hhr", "test"],
    description = "hhrtest",
    long_description = "hhrtest sdk for python",
    license = "MIT Licence",

    url = "https://github.com/hhr66",
    author = "hhrtest",
    author_email = "hhr66@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],
    scripts = [],
    entry_points = {
        'console_scripts': [
            'hhrtestcli = hhrtest.help:main'
        ]
    }
)

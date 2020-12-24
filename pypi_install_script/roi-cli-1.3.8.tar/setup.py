#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "roi-cli",
    version = "1.3.8",
    keywords = ("pip", "os", "cli"),
    description = "roi-cli",
    long_description = "roi-cli",
    license = "MIT Licence",

    url = "",
    author = "wusir",
    author_email = "wusir666666@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['click','Django'],

    scripts = [],
    entry_points={
        'console_scripts':['roi=core.main:cli',]
    },
)
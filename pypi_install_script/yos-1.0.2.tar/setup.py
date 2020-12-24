#!/usr/bin/env python
#coding:utf-8

from setuptools import setup
from yos.yos import __version__

setup(
    name = "yos",
    version = __version__,
    author = "yos",
    author_email = "yos@gmial.com",
    url = "http://www.yos.com",
    description = "this is yos",
    packages = ["yos"],
    install_requires = [],
    entry_points = {
        'console_scripts' : [
            'yos=yos:yos.main',
        ]
    }
)


# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 上午9:23
# @Author  : Shark
# @File    : setup.py
#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="flow-dev2.1.3py27",
    version="1.0.0",
    author="beo",
    author_email="15711305046@163.com",
    license="MIT",
    packages=['flow','item','sign','Filter','facebook'],
    install_requires=[],
    ##package_data={'sign':['*.jar']},
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
       ## "Programming Language :: Python :: 2",
       ## "Programming Language :: Python :: 2.6",
       ## "Programming Language :: Python :: 2.7",
    ],
)
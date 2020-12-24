#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 16:17
# @Author  : kaiwen Xue
# @File    : setup.py
# @Software: PyCharm
from setuptools import setup, find_packages


setup(
    name='kaiwen',
    version='0.3',
    description=(
        "kaiwen's package, mainly for personal use"
    ),
    long_description=open('README.rst').read(),
    author='kaiwen Xue',
    author_email='yixian.xue@gmail.com',
    maintainer='kaiwen Xue',
    maintainer_email='yixian.xue@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='http://github.com/kxue4/kaiwen',
    classifiers=[
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'WordCloud',
        'jieba',
        'imageio',
        'matplotlib',
        'requests'
    ]
)
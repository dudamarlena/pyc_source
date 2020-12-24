#!/usr/bin/env python
# -*- coding:utf8 -*-

from setuptools import find_packages, setup

version = "0.0.0.0"
long_description = """
    A Python project for job shop scheduling problem.
    
    Benchmark problems, such as FT06, FT10, FT20, LA01, etc.
    http://people.brunel.ac.uk/~mastjjb/jeb/info.html

    Version 0.0.0.0, Date, Dec. 06, 2019

    Contact
    Owner: Yang Guangcan, Wuhan University of Science and Technology
    Email address: guangcanyang@yeah.net
    """

setup(
    name="pyjsp",
    version=version,
    author="hufuture",
    author_email="1623025938@163.com",
    url=None,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=['numpy', 'matplotlib']
)

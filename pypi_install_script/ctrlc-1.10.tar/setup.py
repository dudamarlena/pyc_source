#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "ctrlc",
    version  = "1.10",
    #keywords = ("pip", "ctrl", "ctrl c"),
    description = "解决ctrl+c无法停止的问题",
    long_description = "解决ctrl+c无法停止的问题",
    license = "BSD License",

    url = "",
    author = "chujingbin",
    author_email = "chujingbin@gmail.com",
    maintainer='chujingbin',
    maintainer_email='chujingbin@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = ["all"],
    install_requires = [],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)

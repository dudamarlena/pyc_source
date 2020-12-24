#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
setup(
    name = "mysql2md", 
    version = "0.1.1", 
    description = "根据mysql表结构生成markdown文档",
    long_description = "可以根据选定的mysql数据库或者mysql库中的某个表，根据表结构及注释生成对应的md文档",
    license = "MIT Licence",
    author = "guoridgepole",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pymysql", "argparse"]
)
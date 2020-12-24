#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xialang
# Mail: xialang@cztec.com
# Created Time:  2019-11-16 
#############################################

from setuptools import setup, find_packages      

setup(
    name = "czutils",      #这里是pip项目发布的名称
    version = "1.0.3",  #版本号，数值大的会优先被pip
    keywords = ("pip", "czutils","featureextraction"),
    description = "utils for cztec",
    long_description = "utils for cztec",
    license = "MIT Licence",

    url = "",     #项目相关文件地址，一般是github
    author = "xialang",
    author_email = "xialang@cztec.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy", "requests", "pymysql"]          #这个项目需要的第三方库
)
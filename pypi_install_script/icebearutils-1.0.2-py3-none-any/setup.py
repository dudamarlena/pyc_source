#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "icebearutils",      #这里是pip项目发布的名称
    version = "1.0.2",  #版本号，数值大的会优先被pip
    keywords = ["pip", "IceBear", "zwfw"],
    description = "一个帅气的冰熊的自用utils包",
    long_description = "一个超级无敌帅气的冰熊的自用utils包",
    license = "MIT Licence",

    url = "",     #项目相关文件地址，一般是github
    author = "catsith",
    author_email = "catsith@foxmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["arrow", "requests", "selenium"]          #这个项目需要的第三方库
)

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: AW
# Mail: weidacn@qq.com
# Created Time:  2019-7-29
#############################################


from setuptools import setup, find_packages            #这个包没有的可以pip一下


setup(
    name = "raspi_servo",      #这里是pip项目发布的名称
    version = "1.0.6",  #版本号，数值大的会优先被pip
    keywords = ("pip", "raspi-servo","servo"),
    description = "raspi-servo",
    long_description = "A tool for raspberry PI to control 180 degree servo",
    license="Public domain",
    url = "https://github.com/weidacn/raspi-servo",
    author='AW',
    author_email='weidacn@qq.com',
    
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [""]          #这个项目需要的第三方库
)

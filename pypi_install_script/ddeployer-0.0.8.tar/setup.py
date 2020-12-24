#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: LiangjunFeng
# Mail: zhumavip@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下
import dd

setup(
    name = dd.__serverName__,      #这里是pip项目发布的名称
    version = dd.__version__,  #版本号，数值大的会优先被pip
    keywords = ("pip", "docker","deploy","k8s","kubernetes",dd.__serverName__,dd.__daemonName__),
    description = "A simple tool for deploying docker",
    long_description=('详情请见：[https://github.com/stosc/dockerdeployer](https://github.com/stosc/dockerdeployer)'),
    long_description_content_type="text/markdown",
    license = "MIT Licence",

    url = "https://github.com/stosc/dockerdeployer",     #项目相关文件地址，一般是github
    author = dd.__author__,
    author_email = "stosc@sidaxin.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["flask"],          #这个项目需要的第三方库
    classifiers=[        
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            '%s = dd.run:main'%(dd.__serverName__),
            '%s = dd.main:run'%(dd.__daemonName__),

        ]
    },
    python_requires='>=3.6',
)

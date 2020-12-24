#!/usr/bin/env python		
#coding:utf-8

from setuptools import setup, find_packages
setup(
    name = "infosearch",
    author = "rivir",
    description = 'python search api by tornado',
    url = 'https://github.com/jiangsir404',
    version = "1.0",
	author_email = "rivirsec@163.com",
    packages = ['pysearch'],
    package_dir={'pysearch': 'pysearch'},
    include_package_data = True,
    install_requires = [
    	"tornado==5.1.1",
    	"simplejson"
    ]
)
# /usr/bin/env == python3.7
# -*- coding=utf-8 -*-
# @author      : quinn7solomon
# @email       : quinn.7@foxmail.com
# @starting    : 2020-04-11
# @environment : PyCharm && VsCode

# setup.py

from setuptools import setup, find_packages

setup(
    name='chenlib',
    version='0.1.2',
    keywords=('pip', 'chenlib'),
    description='None',
    long_description='None',
    license='None',

    url='https://github.com/quinn7solomon/chenlib',
    author='quinn7solomon',
    author_email='quinn.7@foxmail.com',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[]
)


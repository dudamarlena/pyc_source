#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='surn3k-login',
    version='0.0.4',
    author='zh',
    author_email='fyved24@163.com',
    url='http://blog.fyved24.de',
    description='河南工业大学校园网登陆器',
    packages=['surn3k'],
    install_requires=[
        'requests',
        'argparse',
        'configparser'
    ],
    entry_points={
        'console_scripts': [
            'login=surn3k:login',
        ]
    }
)

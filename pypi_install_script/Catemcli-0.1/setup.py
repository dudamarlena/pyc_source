#!/usr/bin/python
# coding: utf-8

from setuptools import setup

setup(
    name='Catemcli',
    version='0.1',
    author='Graycatya',
    author_email='greycatya@163.com',
    url='https://github.com/greycatya',
    description='A email client in terminal',
    packages=['Catemcli'],
    install_requires=['yagmail'],
    tests_require=['nose', 'tox'],
    entry_points={
        'console_scripts': [
            'Catemcli=Catemcli:main',
        ]
    }
)
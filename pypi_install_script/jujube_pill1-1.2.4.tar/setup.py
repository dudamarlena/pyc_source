#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='jujube_pill1',
    version='1.2.4',
    author='dapeng09',
    author_email='wangfupeng@qiyi.com',
    url='https://www.baidu.com',
    description=u'吃枣药丸',
    packages=['jujube-pill'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jujube=jujube_pill1:jujube',
            'pill=jujube_pill1:pill'
        ]
    }
)
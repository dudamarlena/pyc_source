'''
@Author: your name
@Date: 2019-12-05 09:46:15
@LastEditTime: 2019-12-05 11:12:02
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \zw\setup.py
'''
#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='zw',
    version='0.0.1',
    author='Vvgoder',
    author_email='1060825598@qq.com',
    url='https://zhuanlan.zhihu.com/p/26159930',
    description=u'吃枣药丸',
    packages=['zw'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jujube=zw:jujube',
            'pill=zw:pill'
        ]
    }
)

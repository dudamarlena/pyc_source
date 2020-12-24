#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='music-diff',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'prettytable'
    ],

    entry_points={
        'console_scripts': [
            'music-diff = diff:start'
        ],
    },

    license='MIT',
    author='Junbaor',
    author_email='junbaor@gmail.com',
    url='https://github.com/junbaor',
    description='寻找两人歌单中相同的音乐',
    keywords=['music', 'netease', 'cli', 'diff'],
)

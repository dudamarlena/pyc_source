#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: setup.py
# @description:
# @reference:
# @author: chenli_gogo@163.com
# @created time: 2020-04-03 10:38

import os
from setuptools import setup, find_packages

root_dir = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    with open(os.path.join(root_dir, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='ai-detector',
    version='1.0.7',
    author='charlichen',
    author_email='chenli_gogo@163.com',
    description='UI detector, realized by image identification and OCR',
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/iTestinglab/ai-detector',
    keywords=['ai', 'automated-test', 'ocr', 'image identification'],
    packages=find_packages(
        exclude=[]),
    package_data={
        'detector': ['../requirements.txt'],
    },
    install_requires=read_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

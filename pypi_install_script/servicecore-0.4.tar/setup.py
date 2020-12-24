# -*- coding: utf-8 -*-
# Created by lvjiyong on 15/3/16

from os.path import dirname, join

from setuptools import setup, find_packages

project_dir = dirname(__file__)

with open(join(project_dir, 'VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name="servicecore",
    version=version,
    description="内容处理服务",
    author="lvjiyong",
    url="http://git.dk.com/lvjiyong/servicecore",
    license="GPL",
    include_package_data=True,
    packages=find_packages(exclude=()),
    long_description=open(join(project_dir, 'README.md')).read(),
    maintainer='lvjiyong',
    platforms=["any"],
    maintainer_email='lvjiyong@gmail.com',

    install_requires=['redis', 'jieba', 'mmh3', 'pybloomfiltermmap', 'debug-log', 'six'],
)
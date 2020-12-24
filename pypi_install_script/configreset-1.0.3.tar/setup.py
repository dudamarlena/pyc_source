# -*- coding: utf-8 -*-

from os.path import dirname, join

from setuptools import setup, find_packages

project_dir = dirname(__file__)



setup(
    name="configreset",
    version='1.0.3',
    description="configreset",
    author="lvjiyong",
    url="https://github.com/lvjiyong/configreset",
    license="GPL",
    include_package_data=True,
    packages=find_packages(exclude=()),
    long_description='configreset',
    maintainer='lvjiyong',
    platforms=["any"],
    maintainer_email='lvjiyong@gmail.com',
    install_requires=['six'],
)
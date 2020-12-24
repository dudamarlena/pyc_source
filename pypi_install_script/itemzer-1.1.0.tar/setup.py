#! /usr/bin/env python3
from setuptools import setup

setup(
   name='itemzer',
   version='1.1.0',
   description='Module for getting informations for League of Legend champions',
   author='p0',
   author_email='kylian.p@protonmail.ch',
   packages=['itemzer'],
   url="https://github.com/p0lux/Itemzer",
   install_requires=['requests', 'beautifulsoup4'],
   entry_points={"console_scripts": ["itemzer=itemzer.__main__:main",]}
)


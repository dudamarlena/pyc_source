# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyconn',
    version='0.1.3',
    description='python connection tools collection',
    long_description=readme,
    author='Roy Liu',
    author_email='roystd@qq.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

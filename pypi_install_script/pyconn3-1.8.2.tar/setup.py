# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyconn3',
    version='1.8.2',
    description='python connection tools collection',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='James Liu',
    author_email='liuchuanbo@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'requests==2.22.0'
]

setup(
    name='openreview',
    version='0.0.2',
    author='Zhi Rui Tam',
    author_email='ray@currentsapi.services',
    license='MIT',
    url='https://github.com/theblackcat102/openreview_api_py',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    description='Openreview web API client',
    keywords=['openreview', 'data-mining', ''],
)
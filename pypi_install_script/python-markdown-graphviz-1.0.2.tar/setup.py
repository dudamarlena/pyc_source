#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from setuptools import setup


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='python-markdown-graphviz',
    version='1.0.2',
    author='Yugang LIU',
    author_email='liuyug@gmail.com',
    url='https://github.com/liuyug/python-markdown-graphviz.git',
    license='MIT',
    description='Graphviz extension for python-markdown',
    long_description=long_description,
    py_modules=['mdx_graphviz'],
    install_requires=['Markdown>=2.5', 'graphviz'],
)

#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup, find_packages


setup(
    name='analyse-stock',
    version=0.3,
    author='pengsir',
    author_email='qq@qq.com',
    maintainer='pengsir',
    maintainer_email='qq@qq.com',
    license='BSD License',
    packages=find_packages(),
    description="analyse stock",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    platforms=["all"],
    url='',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries'
    ],
)




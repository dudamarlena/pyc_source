#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='EventExtract',
    version=1.0,
    description=(
        'EventExtract'
    ),
    long_description=open('README.rst').read(),
    author='wzy',
    author_email='hawangzy@163.com',
    maintainer='wzy',
    maintainer_email='hawangzy@163.com',
    license='BSD License',
    packages= find_packages(),
    platforms=["all"],
    url='http://www.eventanalysis.com.cn:28081/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ],
)
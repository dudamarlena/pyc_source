#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup

setup(
    version='0.1',
    name = 'da',
    scripts=['da.py','da'],
    requires = ['python (>= 2.5)'],
    description = 'Task automatization tool.',
    long_description = open('README.rst').read(),
    author = 'Ilya Shalyapin',
    author_email = 'ishalyapin@gmail.com',
    url = 'https://bitbucket.org/ishalyapin/da/',
    download_url = 'https://bitbucket.org/ishalyapin/da/get/master.tar.gz',
    license = 'MIT License',
)

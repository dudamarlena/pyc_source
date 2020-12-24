#!/usr/bin/env python

from setuptools import setup

VERSION = '0.1.4'

DOWNLOAD_URL = 'https://github.com/coinfee/coinfee-python/tarball/{}'

setup(
    name='coinfee',
    version=VERSION,
    author='Teran McKinney',
    author_email='sega01@go-beyond.org',
    description='Library for coinfee.net, a Bitcoin payment processor',
    keywords=['bitcoin'],
    license='Unlicense',
    url='https://github.com/coinfee/coinfee-python/',
    download_url=DOWNLOAD_URL.format(VERSION),
    packages=['coinfee'],
    setup_requires=[
        'flake8'
    ],
    install_requires=[
        'pyyaml'
    ]
)

#!/usr/bin/env python3

from setuptools import setup

VERSION = '0.1.0'

URL = 'https://github.com/teran-mckinney/hostnameomatic-python'
DOWNLOAD_URL = URL + '/{}'

setup(
    python_requires='>=3.3',
    name='hostnameomatic',
    version=VERSION,
    author='Teran McKinney',
    author_email='sega01@go-beyond.org',
    description='Returns resolvable hostnames from IPv4 and IPv6 addresses',
    keywords=['dns'],
    license='Unlicense',
    url=URL,
    download_url=DOWNLOAD_URL.format(VERSION),
    packages=['hostnameomatic'],
)

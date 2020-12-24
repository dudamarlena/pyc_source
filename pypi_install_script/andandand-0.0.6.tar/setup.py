#!/usr/bin/env python

from setuptools import setup

version = '0.0.6'

url = 'https://github.com/matterport/andandand'

setup(
    name='andandand',
    version=version,
    author='Teran McKinney',
    author_email='sega01@go-beyond.org',
    description='HTTP/S health check proxy to test multiple health checks.',
    keywords=['http', 'health'],
    license='Unlicense',
    url=url,
    download_url=url + '/tarball/' + version,
    packages=['andandand'],
    setup_requires=[
        'flake8'
    ]
)

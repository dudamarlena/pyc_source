#!/usr/bin/env python

from setuptools import setup,find_packages

setup(name="leoproj",
    version="0.0.1",
	packages=find_packages(),
    author="goofansu",
    author_email="goofan.su@gmail.com",
    description="Framework under tornado, jinja2 and wtforms",
    url="",
    install_requires=[
        'tornado',
        'jinja2',
        'wtforms',
        'beautifulsoup4',
        'pymongo',
        'redis',
        'poster',
    ]
)

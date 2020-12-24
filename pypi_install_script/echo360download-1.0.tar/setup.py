#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='echo360download',
    version='1.0',

    description="Download Echo 360 files",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Visgean",
    author_email='visgean@gmail.com',
    url='https://github.com/visgean/gimme-echo360',
    packages=[
        'echo',
    ],
    package_dir={'echo': 'echo'},
    license="MIT",
    keywords='exif sql',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'python-dateutil',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'echo360download = echo.main:main'
        ]
    },
)
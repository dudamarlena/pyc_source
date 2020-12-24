#!/usr/bin/env python

#
# [setup.py]
#
# The installer for the Lime language.
# Copyright (C) 2019, Liam Schumm, Andy Merrill
#

from setuptools import setup, find_packages

setup(
    name="lime-lang",
    version="1.4.2",
    description="Lime is an experimental, stack-based, purely functional programming language.",
    long_description=open("README.rst").read(),
    author="Liam Schumm",
    author_email="liamschumm@icloud.com",
    python_requires=">=2.7",
    url="https://limelang.xyz",
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['lime=lime:main'],
    },
    include_package_data=True,
    license='GPL',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
    ]
)

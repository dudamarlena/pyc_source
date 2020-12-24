#!/usr/bin/env python3

"""
    project = S_Logger
    script = setup.py
    author = nkiseev
    date = 8/8/18 5:43 PM
"""

from setuptools import setup, find_packages
from os.path import join, dirname
import s_logger as sl


setup(
    name='S_Logger',
    version=sl.__version__,
    author="Kiseev Nikolay",
    author_email="kiseev.nikolay@gmail.com",
    description="S_Logger",
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nkiseev/S_Logger",
    test_suite='test',
    install_requires=[
        'PyYAML==3.12'
    ],
)


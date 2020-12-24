#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

from django_mix import __version__

setup(
    name='django-mix',
    version=__version__,
    author='Tim Kamanin',
    author_email='tim@timonweb.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/timonweb/django-mix',
    license='MIT',
    description='A Django integration with Laravel Mix.',
    long_description=open('README.md').read(),
    install_requires=[],
)
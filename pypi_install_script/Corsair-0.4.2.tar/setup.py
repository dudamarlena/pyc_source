#!/usr/bin/env python3

from setuptools import setup, find_packages


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='Corsair',
    version='0.4.2',
    author='José Lopes de Oliveira Jr.',
    author_email='2897144+forkd@users.noreply.github.com',
    description='Python wrappers for some NSOC tools.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/forkd/corsair',
    packages=find_packages(exclude=['*.tests.*', "test.*", "tests"]),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

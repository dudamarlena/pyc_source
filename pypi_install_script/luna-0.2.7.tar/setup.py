#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'troposphere',
    'gitpython',
    'awscli',
    'boto3',
    'prettytable',
    'toolz',
    'fabulous'
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Steven Brien",
    author_email='spbrien@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
    description="Simple CloudFormation Templates and Stacks",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='luna',
    name='luna',
    packages=find_packages(include=['luna']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='',
    version='0.2.7',
    zip_safe=False,
)

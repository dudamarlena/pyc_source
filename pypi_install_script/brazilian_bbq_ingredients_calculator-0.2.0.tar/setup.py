#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Rafael Toguko",
    author_email='toguko@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="A calculator to give all ingredients to make a Brazilian BBQ for X people",
    entry_points={
        'console_scripts': [
            'brazilian_bbq_ingredients_calculator=brazilian_bbq_ingredients_calculator.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='brazilian_bbq_ingredients_calculator',
    name='brazilian_bbq_ingredients_calculator',
    packages=find_packages(include=['brazilian_bbq_ingredients_calculator']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/toguko/brazilian_bbq_ingredients_calculator',
    version='0.2.0',
    zip_safe=False,
)

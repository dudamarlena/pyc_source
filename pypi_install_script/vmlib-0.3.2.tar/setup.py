#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click>=6.0',
    'matplotlib',
    'numpy',
    'pandas',
    'segyio',
    'scikit-learn',
    'scipy',
    'squarify',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Valentin Metraux",
    author_email='valentin@valentinmetraux.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Geophysical / GIS toolbox",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    keywords='vmlib',
    name='vmlib',
    packages=find_packages(),
    package_data={'': ['*.jpg', '*.txt']},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/valentinmetraux/vmlib',
    version='0.3.2',
    zip_safe=False,
)

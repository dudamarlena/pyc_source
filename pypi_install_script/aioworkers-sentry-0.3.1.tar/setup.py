#!/usr/bin/env python

import pathlib
import sys

from setuptools import find_packages, setup

version = __import__('aioworkers_sentry').__version__

requirements = [
    'aioworkers>=0.13',
    'sentry_sdk>=0.13.5',
]

if sys.version_info < (3, 7):
    requirements.append('aiocontextvars')

test_requirements = [
    'pytest',
    'pyyaml',
    'pytest-runner',
    'pytest-mock',
    'pytest-aioworkers',
    'pytest-flake8',
    'pytest-isort',
    'pytest-mypy',
]

readme = pathlib.Path('README.rst').read_text()


setup(
    name='aioworkers-sentry',
    version=version,
    description='aioworkers plugin for Sentry',
    long_description=readme,
    author='Alexander Bogushov',
    author_email='abogushov@gmail.com',
    url='https://github.com/aioworkers/aioworkers-sentry',
    packages=[
        i for i in find_packages() if i.startswith('aioworkers_sentry')
    ],
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    keywords='aioworkers sentry',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)

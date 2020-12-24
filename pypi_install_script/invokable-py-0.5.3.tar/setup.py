#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import os
from os.path import join

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

install_requirements = [
    'starfish-py>=0.9.0',
    'flask',
    'flask_swagger',
    'flask_swagger_ui',
    'flask_httpauth',
    'flask_cors',
    'gunicorn',
    'inflection',
]

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'flake8',
    'pytest',
    'isort',
]

dev_requirements = [
    'bumpversion',
    'pkginfo',
]

docs_requirements = [
    'Sphinx',
    'sphinx-rtd-theme',
    'sphinxcontrib-apidoc',
    'sphinxcontrib-plantuml',
    'sphinx-automodapi',
    'pygments',
]

setup(
    author="dex-company",
    author_email='devops@dex.sg',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="inokable-py allows you to add invokable web services to your application.",
    extras_require={
        'test': test_requirements,
        'docs': docs_requirements,
        'dev': dev_requirements + test_requirements + docs_requirements,
    },
    install_requires=install_requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='invokable-py invoke dex',
    name='invokable-py',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/DEX-Company/invokable-py',
    version='0.5.3',
    zip_safe=False,
)

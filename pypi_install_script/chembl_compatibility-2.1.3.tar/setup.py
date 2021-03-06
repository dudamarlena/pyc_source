#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'mnowotka'

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='chembl_compatibility',
    version='2.1.3',
    author='Michal Nowotka',
    platforms=['Linux'],
    author_email='mnowotka@ebi.ac.uk',
    description='Compatibility layer for running webservices from outside ChEMBL',
    url='https://www.ebi.ac.uk/chembl/',
    license='Apache Software License',
    packages=['chembl_compatibility'],
    long_description=open('README.rst').read(),
    install_requires=[
        'chembl-core-model>=0.8.3',
        'chembl-migration-model>=0.8.1'
    ],
    include_package_data=False,
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Scientific/Engineering :: Chemistry'],
    zip_safe=False,
)

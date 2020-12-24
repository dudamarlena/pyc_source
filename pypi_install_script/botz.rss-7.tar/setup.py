#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

from setuptools import setup

def readme():
    return open("README").read()

setup(
    name='botz.rss',
    version=7,
    url='https://bitbucket.org/bthate/botz.rss',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="RSS fetcher for BOTZ",
    long_description=readme(),
    zip_safe=False,
    license='Public Domain',
    install_requires=["feedparser"],
    packages=["botz"],
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Application Frameworks'
                ]
)

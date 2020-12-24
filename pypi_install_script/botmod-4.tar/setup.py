#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

from setuptools import setup

setup(
    name='botmod',
    version='4',
    url='https://bitbucket.org/bthate/botmod',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Timestamped JSON objects",
    long_description=""" Modules for BOTLIB. """,
    license='Public Domain',
    install_requires=["botlib", "feedparser", "dnspython", "pyasn1_modules==0.1.5", "pyasn1==0.3.6", "sleekxmpp==1.3.1"],
    zip_safe=True,
    packages=["mods"],
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python'
                ]
)

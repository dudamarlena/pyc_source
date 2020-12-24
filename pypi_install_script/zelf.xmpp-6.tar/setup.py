#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run ZELF with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='zelf.xmpp',
    version='6',
    url='https://bitbucket.org/bthate/zelf.xmpp',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="xmpp bot for the zelf package",
    long_description="""
ZELF is a pure python3 framework to program bots, provides an IRC bot to use and is extendible by programming your own commands.
ZELF uses a timestamped, type in filename, JSON stringified, files on filesystem backend and has timed based logging capabilities.
ZELF has been placed in the Public Domain and contains no copyright or LICENSE.
    """,
    install_requires=["zelf", "dnspython", "pyasn1_modules==0.1.5", "pyasn1==0.3.6", "sleekxmpp==1.3.1"],
    license='Public Domain',
    zip_safe=False,
    packages=['zelf.xmpp'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

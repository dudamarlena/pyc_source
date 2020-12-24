#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

from setuptools import setup

def readme():
    return open("README").read()

setup(
    name='botz.xmpp',
    version=4,
    url='https://bitbucket.org/bthate/botz.xmpp',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="XMPP bot for BOTZ",
    long_description=readme(),
    zip_safe=False,
    license='Public Domain',
    install_requires=["dnspython", "pyasn1_modules==0.1.5", "pyasn1==0.3.6", "sleekxmpp==1.3.1"],
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

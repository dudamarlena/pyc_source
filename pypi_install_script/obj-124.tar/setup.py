#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" setup.py """

try:
    from setuptools import setup
except ImportError:
    from pkgutils import setup
    
setup(
    name='obj',
    version='124',
    url='https://bitbucket.org/bthate/obj',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Timestamped JSON objects",
    long_description=""" OBJ is a pure python3 framework that allows storage of JSON object to a filestamped file on the disk. 
                         OBJ uses a timestamped, type in filename, JSON stringified, files on filesystem backend and has timed based logging capabilities. 
                         OBJ has been placed in the Public Domain and contains no copyright or LICENSE.
                     """,
    license='Public Domain',
    packages=["obj"],
    zip_safe=True,
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python'
                ]
)

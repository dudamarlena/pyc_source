#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, dist
dist.Distribution(dict(setup_requires=['bob.extension']))

from bob.extension.utils import load_requirements, find_packages
install_requires = load_requirements()


setup(

    name='bob.db.brsu',
    version=open("version.txt").read().rstrip(),
    description="Bob's interface for the BRSU Multispectral Face/Skin Database",

    url='https://gitlab.idiap.ch/bob/bob.db.brsu',
    license='GPLv3',

    # there may be multiple authors (separate entries by comma)
    author='Guillaume Heusch',
    author_email='guillaume.heusch@idiap.ch',

    # there may be a maintainer apart from the author - you decide
    #maintainer='?'
    #maintainer_email='email@example.com'

    # you may add more keywords separating those by commas (a, b, c, ...)
    keywords = "bob",

    long_description=open('README.rst').read(),

    # leave this here, it is pretty standard
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,

    install_requires=install_requires,

    entry_points={
        
        'bob.db': [
          'brsu = bob.db.brsu.driver:Interface',
        ],

      },

    # check classifiers, add and remove as you see fit
    # full list here: https://pypi.org/classifiers/
    # don't remove the Bob framework unless it's not a bob package
    classifiers = [
      'Framework :: Bob',
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Software Development :: Libraries :: Python Modules',
      ],

)

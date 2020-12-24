# encoding: utf-8

"""
Opcvm-sdk distribution setup

@author:        Eric Pieuchot
@copyright:     Copyright 2016 Rubicubix Ltd
@license:       Apache-2.0
@contact:       contact@rubicubix.co.uk
"""

from setuptools import setup, find_packages

# Description
NAME = "opcvm-sdk-python"
DESCRIPTION = "OPCVM360 RESTFul API Wrapper"
README = """
A Python library communicating with OPCVM360 RESTFull API
(http://services.opcvm360.com)
"""
KEYWORDS = "opcvm opcvm360 api sdk"
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries",
]

# Credentials
VERSION = "1.1.7"
LICENSE = "Apache-2.0"
AUTHOR = "Eric Pieuchot"
EMAIL = "eric@rubicubix.co.uk"
URL = "https://github.com/Rubicubix/opcvm-sdk-python"

# Package data
PATH = {'opcvm_sdk': 'opcvm_sdk'}
EXCLUDE = [
    'opcvm_sdk.test',
]

# Dependencies
PLATFORMS = ['Any']
DEPENDENCIES = [
    "pandas==0.19",
    "requests",
    "simplejson",
]

# Make install
setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=README,
      keywords=KEYWORDS,
      classifiers=CLASSIFIERS,
      # Credentials
      author=AUTHOR,
      author_email=EMAIL,
      license=LICENSE,
      url=URL,
      # Package data
      packages=find_packages(exclude=EXCLUDE),
      package_dir=PATH,
      # Dependencies
      platforms=PLATFORMS,
      install_requires=DEPENDENCIES)
